import requests
import collections
import psycopg2
import psycopg2.extras
import twython
from time import sleep

from keys_boro import keys

id_boro_dict = collections.defaultdict(str) #dictionary of station ids to boro
boro_dict = collections.defaultdict(int) #dictionary of values for each boro

def get_id_boro():
    #boro list setup
    con = psycopg2.connect(database="utility", user="datapolitan", host="utility.c1erymiua9dx.us-east-1.rds.amazonaws.com")
    cur = con.cursor()
    cur.execute(open("query_boro.sql").read()) #read boros from database
    q = cur.fetchall()
    for row in q:
        id_boro_dict[str(row[0])] = row[1]
        if row[1] not in boro_dict.keys():
            boro_dict[row[1] = 0
    con.close()
    return

def get_cb_dock(boro):
    '''
    get the dock status and compute summary statistics for tweeting
    '''
    #need to wrap in try-catch
    r = requests.get('http://www.citibikenyc.com/stations/json')
    totalDocks_sum = 0
    avail_bikes_sum = 0
    in_service_station_sum = 0
    for station in r.json()['stationBeanList']:
        if station['statusKey'] == 1 and id_boro_dict[str(station['id'])] == boro:
            totalDocks_sum += station['totalDocks']
            avail_bikes_sum += station['availableBikes']
            in_service_station_sum += 1
    tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro)
    # print "%s Citibikes, or %s%% of dock capacity, are available across %s active docking stations in #%s" % ("{:,.0f}".format(avail_bikes_sum),"%.2f" % (round(avail_bikes_sum/float(totalDocks_sum),4) * 100),in_service_station_sum,boro)
    return

def tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro):
    '''
    a function to tweet the input values
    '''
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    totalDocks_percent = 0
    if totalDocks_sum > 0:
        totalDocks_percent = round(avail_bikes_sum/float(totalDocks_sum),4) * 100
    twitter.update_status(status="%s Citibikes, or %s%% of dock capacity, are available across %s active docking stations in #%s" % ("{:,.0f}".format(avail_bikes_sum),"%.2f" % (totalDocks_percent),in_service_station_sum,boro))
    return


get_id_boro() #initialize id_boro_dict and boro_list from database on first run

while True: #infinite loop 
    for boro in boro_list: #iterate through boro_list to check each boro
        get_cb_dock(boro) #get dock count for boro
        sleep(900) #sleep for 15 minutes
