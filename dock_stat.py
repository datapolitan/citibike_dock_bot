import requests
from collections import defaultdict
from time import sleep

def get_cb_dock():
    '''
    get the dock status and compute summary statistics for tweeting
    '''
    #need to wrap in try-catch
    r = requests.get('http://www.citibikenyc.com/stations/json')

    totalDocks_sum = 0
    avail_bikes_sum = 0
    in_service_station_sum = 0
    for station in r.json()['stationBeanList']:
        if station['statusKey'] == 1:
            totalDocks_sum += station['totalDocks']
            avail_bikes_sum += station['availableBikes']
            in_service_station_sum += 1
    tweet_status(avail_bikes_sum,totalDocks_sum)
    return


def tweet_status(avail_bikes_sum,totalDocks_sum):
    '''
    a function to tweet the input values
    '''
    print "There are currently %s Citibikes available in NYC out of a total %s docks for %s%% availability" % (avail_bikes_sum,totalDocks_sum,"%.2f" % (round(avail_bikes_sum/float(totalDocks_sum),4) * 100))

while True:
    get_cb_dock()
    sleep(60)