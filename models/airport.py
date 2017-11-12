airport_cache = {}


class Airport:
    def __init__(self, code, nid, cname, ctype):
        self.iataCode = code
        self.rnid = nid
        self.colloquialName = cname
        self.contentType = ctype


def get_airport_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid]


def get_iata_airport_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid].iataCode


def get_airport_name_by_rnid(rnid):
    if rnid in airport_cache:
        return airport_cache[rnid].iataCode


def add_airport_to_cache(airport):
    airport_cache[airport.rnid] = airport


def populate_airport_cache(results):
    airports = results['Places']
    for c in airports:
        a = Airport(c['Code'], c['Id'], c['Name'], c['Type'])
        add_airport_to_cache(a)
