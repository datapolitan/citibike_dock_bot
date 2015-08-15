import requests
from collections import defaultdict
from time import sleep
import twython

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
    tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum)
    return

def tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum):
    '''
    a function to tweet the input values
    '''
    consumer_key = "bprCbLVbyzVsgtcdzqHKFWQFM"
    consumer_secret = "FbgaE0dtAZrfDG5gLNBxIhktTN8zeNqNsLNCBJSnUJ1TDVYD1w"
    access_token = "3424772890-3iuUUxgOciP54iLN33BJe3ym0Izc7MgFelkltg6"
    access_token_secret = "97DFnUpcwOs6Ovv3uB3V6E35ht6ZbJpdKMO7grTtgaXLs"
    twitter = twython.Twython(consumer_key,consumer_secret,access_token,access_token_secret)
    twitter.update_status(status="%s, or %s%% of #NYC Citibikes are available for rent across %s active stations" % ("{:,.0f}".format(avail_bikes_sum), "%.2f" % (round(avail_bikes_sum/float(totalDocks_sum),4) * 100),in_service_station_sum))

while True:
    get_cb_dock()
    sleep(1800)