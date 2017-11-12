import requests
import urlparse
import time

BASE_API_URL = "http://partners.api.skyscanner.net"
DIRECTIONALITY_OUTBOUND = 'Outbound'
DIRECTIONALITY_INBOUND = 'Inbound'

airport_cache = {}
airline_cache = {}


def get_airport_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid]


def get_airline_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid]


def get_iata_airport_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid].iataCode


def get_iata_airline_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].iataCode


def get_airline_logo_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].carrierLogoURL


def get_airline_name_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].colloquialName


def get_airport_name_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid].iataCode


class FlightSegment:
    def __init__(self,
                 arrival_datetime,
                 carrier,
                 departure_datetime,
                 destination_rnid,
                 directionality,
                 duration,
                 flight_number,
                 operating_carrier,
                 origin_rnid
                 ):
        self.arrivalDateTime = arrival_datetime
        self.departureDateTime = departure_datetime
        self.carrier = carrier
        self.destinationRNID = destination_rnid
        self.originRNID = origin_rnid
        self.directionality = directionality
        self.duration = duration
        self.flightnumber = flight_number
        self.operatingcarrier = operating_carrier

    def __str__(self, client):
        try:
            outstr = "".join(
                ["[", self.directionality, "] ", airline_cache[self.carrier].iataCode, str(self.flightnumber),
                 ", Duration ", str(self.duration), " minutes from ", airport_cache[self.originRNID].iataCode, " to ",
                 airport_cache[self.destinationRNID].iataCode])
            return outstr
        except:
            return "err"


class FlightSet:
    def __init__(
            self,
            flight_segments,
            cost,
            currency,
            deeplink
    ):
        self.flightSegments = flight_segments
        self.cost = round(cost, 2)
        self.currency = currency
        self.deeplink = deeplink

    def __str__(self):
        outstr = ""
        for s in self.flightSegments:
            if str(s) != "err":
                outstr += (str(s) + "\n")
        outstr += "Trip Cost: " + self.currency + " " + str(self.cost)
        return outstr


class Airport:
    def __init__(self, code, nid, cname, ctype):
        self.iataCode = code
        self.rnid = nid
        self.colloquialName = cname
        self.contentType = ctype


class Airline:
    def __init__(self, code, dcode, nid, logo, cname):
        self.iataCode = code
        self.displayCode = dcode
        self.rnid = nid
        self.carrierLogoURL = logo
        self.colloquialName = cname


class SkyscannerClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_flight_routes(self, query_data):
        tries = 0
        r = requests.post("{}/apiservices/pricing/v1.0/?apikey={}".format(BASE_API_URL, self.api_key),
                          data=query_data)
        try:
            results = requests.get('{}?apiKey={}'.format(r.headers['Location'], self.api_key)).json()
        except:
            results = dict()
            results['Status'] = "err"
        while results['Status'] != "UpdatesComplete" and tries < 30:
            try:
                results = requests.get(r.headers['Location'] + "?apiKey=" + self.api_key).json()
            except:
                results['Status'] = "err"
            tries += 1
            time.sleep(1)
        return results

    def print_flight_segments(self, itinerary):
        details = itinerary['BookingDetailsLink']
        r = requests.put('{}{}?apiKey={}'.format(BASE_API_URL, details['Uri'], self.api_key),
                         data=urlparse.parse_qs("&" + details['Body']))
        if r.status_code == 201:
            results = requests.get(r.headers['Location'] + "?apiKey=" + self.api_key).json()
            segments = results['Segments']
            for s in segments:
                try:
                    if s['Directionality'] == DIRECTIONALITY_OUTBOUND:
                        print "=> Flight", airline_cache[s['Carrier']].iataCode, s['FlightNumber'], "Lasting", s[
                            'Duration'], "minutes from", airport_cache[s['OriginStation']].iataCode, "to", \
                            airport_cache[
                                s['DestinationStation']].iataCode
                    else:
                        print "<= Flight", airline_cache[s['Carrier']].iataCode, s['FlightNumber'], "Lasting", s[
                            'Duration'], "minutes from", airport_cache[s['OriginStation']].iataCode, "to", \
                            airport_cache[
                                s['DestinationStation']].iataCode
                except:
                    print "\n"
                    return False
            return True

    def get_flight_segments(self, itinerary):
        details = itinerary['BookingDetailsLink']
        r = requests.put(BASE_API_URL + details['Uri'] + "?apiKey=" + self.api_key,
                         data=urlparse.parse_qs("&" + details['Body']))
        if r.status_code == 201:
            results = requests.get(r.headers['Location'] + "?apiKey=" + self.api_key).json()
            segments = results['Segments']
            flight_group = []
            for s in segments:
                try:
                    if s['Directionality'] == DIRECTIONALITY_OUTBOUND:
                        fs = FlightSegment(s['ArrivalDateTime'], s['Carrier'], s['DepartureDateTime'],
                                           s['DestinationStation'], DIRECTIONALITY_OUTBOUND, s['Duration'],
                                           s['FlightNumber'],
                                           s['OperatingCarrier'], s['OriginStation'])
                        flight_group.append(fs)
                    else:
                        fs = FlightSegment(s['ArrivalDateTime'], s['Carrier'], s['DepartureDateTime'],
                                           s['DestinationStation'], DIRECTIONALITY_INBOUND, s['Duration'],
                                           s['FlightNumber'],
                                           s['OperatingCarrier'], s['OriginStation'])
                        flight_group.append(fs)
                except:
                    return False
            return flight_group

    def init_search_session(self, country, currency, dep, dest, outdate, indate, cabin):
        query = build_query_data(country, currency, dep, dest, outdate, indate, cabin)
        res = self.get_flight_routes(query)
        populate_airport_cache(res)
        populate_airline_cache(res)
        return res


def add_airport_to_cache(airport):
    airport_cache[airport.rnid] = airport


def add_airline_to_cache(airline):
    airline_cache[airline.rnid] = airline


def populate_airport_cache(results):
    airports = results['Places']
    for c in airports:
        a = Airport(c['Code'], c['Id'], c['Name'], c['Type'])
        add_airport_to_cache(a)


def populate_airline_cache(results):
    carriers = results['Carriers']
    for c in carriers:
        a = Airline(c['Code'], c['DisplayCode'], c['Id'], c['ImageUrl'], c['Name'])
        add_airline_to_cache(a)


# Note: Postman is a nice extension

# Country is ISO code
# Currency is ISO code
# Departure is IATA code
# Destination is IATA code
# Date is YYYY-MM-DD
# Cabin is "Economy", "PremiumEconomy", "Business", "First"
def build_query_data(country, currency, dep, dest, outdate, indate, cabin):
    data = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "country": country,
        "currency": currency,
        "locale": "en-GB",
        "locationSchema": "iata",
        "grouppricing": "false",
        "originplace": dep,
        "destinationplace": dest,
        "outbounddate": outdate,
        "inbounddate": indate,
        "adults": "1",
        "children": "0",
        "infants": "0",
        "cabinclass": cabin}
    return data


def get_itinerary_cost(itinerary):
    prices = itinerary['PricingOptions']
    price_sum = 0.0
    count = 0
    for i in prices:
        price_sum += i['Price']
        count += 1
    return round(price_sum / count, 2)
    # print itinerary['OutboundLegId'],itinerary['PricingOptions']


# Add Endpoint to retrieve DeepLinks
# Return first DL
def get_deeplink(itinerary):
    for p in itinerary['PricingOptions']:
        # print "Debug:" + p['DeeplinkUrl']
        return p['DeeplinkUrl']


def get_itineraries(result_object):
    r = result_object['Itineraries']
    return r
