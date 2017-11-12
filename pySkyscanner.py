from client import *
from secrets import API_KEY

__author__ = "Nick Lee"
__copyright__ = "Copyright (C) 2015 Nick Lee"
__license__ = "MIT License"


# Testing code
def demo():
    # noinspection PyPep8
    banner = '  /$$$$$$                                                    /$$           /$$       /$$        /$$$$$$  /$$$$$$$  /$$$$$$\n /$$__  $$                                                  | $$          |__/      | $$       /$$__  $$| $$__  $$|_  $$_/\n| $$  \\__/  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$ | $$  /$$$$$$  /$$  /$$$$$$$      | $$  \\ $$| $$  \\ $$  | $$  \n|  $$$$$$  /$$__  $$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$| $$ /$$__  $$| $$ /$$__  $$      | $$$$$$$$| $$$$$$$/  | $$  \n \\____  $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\ $$| $$| $$  \\ $$| $$| $$  | $$      | $$__  $$| $$____/   | $$  \n /$$  \\ $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$| $$  | $$| $$| $$  | $$      | $$  | $$| $$        | $$  \n|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$/| $$|  $$$$$$/| $$|  $$$$$$$      | $$  | $$| $$       /$$$$$$\n \\______/ | $$____/  \\______/ |__/  |__/ \\____  $$ \\______/ |__/ \\______/ |__/ \\_______/      |__/  |__/|__/      |______/\n          | $$                           /$$  \\ $$                                                                        \n          | $$                          |  $$$$$$/                                                                        \n          |__/                           \\______/                                                                         '
    print banner
    # Fun fact: If the airport code doesn't exist, this app crashes
    # VPNResultSet(query)

    client = SkyscannerClient(API_KEY)

    res = client.init_search_session("DE", "EUR", "HAM", "PHL", "2018-03-07", "2018-03-14", "Economy")
    itins = get_itineraries(res)

    # Non-Object Oriented
    for i in itins:
        price = get_itinerary_cost(i)
        if price is not None and client.print_flight_segments(i):
            print "Trip Cost: " + u"\u20AC" + str(get_itinerary_cost(i)) + "\n"

demo()
