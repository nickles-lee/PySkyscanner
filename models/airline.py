airline_cache = {}


class Airline:
    def __init__(self, code, dcode, nid, logo, cname):
        self.iataCode = code
        self.displayCode = dcode
        self.rnid = nid
        self.carrierLogoURL = logo
        self.colloquialName = cname


def get_airline_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid]


def get_iata_airline_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].iataCode


def get_airline_logo_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].carrierLogoURL


def get_airline_name_by_rnid(rnid):
    if rnid in airline_cache:
        return airline_cache[rnid].colloquialName


def add_airline_to_cache(airline):
    airline_cache[airline.rnid] = airline


def populate_airline_cache(results):
    carriers = results['Carriers']
    for c in carriers:
        a = Airline(c['Code'], c['DisplayCode'], c['Id'], c['ImageUrl'], c['Name'])
        add_airline_to_cache(a)
