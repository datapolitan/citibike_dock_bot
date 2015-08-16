import requests
import collections
import psycopg2
import psycopg2.extras
import twython
from time import sleep

from keys_boro import keys

id_boro_dict = collections.defaultdict(str) #dictionary of station ids to boro
# boro_dict = collections.defaultdict(int) #dictionary of active bikes for each boro

def get_id_boro():
    '''
    set the id_boro_dict based on the values in the database and create the boro_dict to receive counts for each boro
    '''
    con = psycopg2.connect(database="utility", user="datapolitan", host="utility.c1erymiua9dx.us-east-1.rds.amazonaws.com")
    cur = con.cursor()
    cur.execute(open("query_boro.sql").read()) #read boros from database
    q = cur.fetchall()
    for row in q:
        id_boro_dict[str(row[0])] = row[1]
#         if row[1] not in boro_dict.keys():
#             boro_dict[row[1]] = 0
    con.close()
    return

def get_cb_dock():
    '''
    get the dock status and compute summary statistics for tweeting
    '''
    #need to wrap in try-catch
    r = requests.get('http://www.citibikenyc.com/stations/json')
    totalDocks_sum = 0
    avail_bikes_sum = 0
    in_service_station_sum = 0
    #re-initialize the boro_dict to reset values
    boro_dict = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        if station['statusKey'] == 1:
            totalDocks_sum += station['totalDocks']
            avail_bikes_sum += station['availableBikes']
            in_service_station_sum += 1
            #update the boro dict with the number of available bikes in that boro
            boro_dict[id_boro_dict[str(station['id'])]] += station['availableBikes']
    tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro_dict)
    return

def tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro_dict):
    '''
    a function to tweet the input values
    '''
    #####authenticate the Twitter account
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    #######

    #######for calculating percents
    # totalDocks_percent = 0
    # if totalDocks_sum > 0:
    #     totalDocks_percent = round(avail_bikes_sum/float(totalDocks_sum),4) * 100
    #######

    ####Should add some length checking to tweet jik
    twitter.update_status(status="%s Citibikes are available in %s active docks, %s in #Manhattan, %s in #Brooklyn, and %s in #Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens'])))
    #print "%s Citibikes are available in %s active docks, %s in Manhattan, %s in Brooklyn, and %s in Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens']))
    return

#####program execution starts

get_id_boro() #initialize id_boro_dict and boro_list from database on first run

while True: #infinite loop 
    get_cb_dock() #get dock count and tweet
    sleep(600) #sleep for 10 minutes
