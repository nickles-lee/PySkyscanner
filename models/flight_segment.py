from airport import airport_cache
from airline import airline_cache


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
