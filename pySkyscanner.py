from client import *
from secrets import API_KEY

__author__ = "Nick Lee"
__copyright__ = "Copyright (C) 2015 Nick Lee"
__license__ = "MIT License"


# Test code
def demo():
    # Fun fact: If the airport code doesn't exist, this app crashes


    client = SkyscannerClient(API_KEY)

    res = client.init_search_session("DE", "EUR", "HAM", "PHL", "2018-03-07", "2018-03-14", "Economy")
    itins = client.get_itineraries(res)

    for i in itins:
        price = client.get_itinerary_cost(i)
        if price is not None and client.print_flight_segments(i):
            print "Trip Cost: " + u"\u20AC" + str(client.get_itinerary_cost(i)) + "\n"

demo()
