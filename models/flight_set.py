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
