import requests
import collections
import psycopg2
import psycopg2.extras
import twython
from time import sleep
import time
from dateutil import parser

from keys_boro import keys


def get_id_boro():
    '''
    set the id_boro_dict based on the values in the database and create the boro_dict to receive counts for each boro
    '''
    id_boro_dict = collections.defaultdict(str) #dictionary of station ids to boro
    con = psycopg2.connect(database="utility", user="datapolitan", host="utility.c1erymiua9dx.us-east-1.rds.amazonaws.com")
    cur = con.cursor()
    cur.execute(open("query_boro.sql").read()) #read boros from database
    q = cur.fetchall()
    for row in q:
        id_boro_dict[str(row[0])] = row[1]
    con.close()
    return id_boro_dict

def get_cb_dock(id_boro_dict):
    '''
    get the dock status and compute summary statistics for tweeting
    '''
    #need to wrap in try-catch
    r = requests.get('http://www.citibikenyc.com/stations/json')    
    
    ####### process the stations json file
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
       
    ###### publish tweet
    tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro_dict)

    ###### save to database
    execution_time = parser.parse(r.json()['executionTime']) #datetime object from file execution time
    boro_order = ['Manhattan','Brooklyn','Queens','New Jersey']
    boro_bike_list = [] #organize values for each boro
    for b in boro_order:
        if b in boro_dict.keys():
            boro_bike_list.append(str(boro_dict[b]))
        else:
            boro_bike_list.append(None)
    write_status(execution_time,avail_bikes_sum,boro_bike_list)

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

    status_text = ''

    if 'New Jersey' in boro_dict.keys():
        status_text = "%s #Citibikes are available in %s active docks: %s in #Manhattan, %s in #Brooklyn, %s in #Queens, & %s in #NJ" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens']),"{:,.0f}".format(boro_dict['New Jersey']))
    else:
        status_text = "%s #Citibikes are available in %s active docks: %s in #Manhattan, %s in #Brooklyn, and %s in #Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens']))

    ####Should add some length checking to tweet jik
    try:
        twitter.update_status(status=status_text)
    except:
        pass
    # print "%s Citibikes are available in %s active docks, %s in Manhattan, %s in Brooklyn, and %s in Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens']))
    return

def write_status(execution_time,avail_bikes_sum,boro_bike_list):
    # write active bike sums into database

    con = psycopg2.connect(database="utility", user="datapolitan", host="utility.c1erymiua9dx.us-east-1.rds.amazonaws.com")
    cur = con.cursor()
    
    sql = "INSERT INTO public.cb_boro_stats (execution_time, nyc_avail_bikes, mhtn_avail_bikes, brklyn_avail_bikes, qns_avail_bikes,nj_avail_bikes) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql,tuple([execution_time] + [avail_bikes_sum] + boro_bike_list))
    con.commit()
    con.close()
    return

#####program execution starts


def main():
    # id_city_dict = collections.defaultdict(str)
    ibd = get_id_boro()
    get_cb_dock(ibd)

if __name__ == "__main__":
    main()


# get_id_boro() #initialize id_boro_dict and boro_list from database on first run

# while True: #infinite loop 
#     get_cb_dock() #get dock count and tweet
#     sleep(600) #sleep for 10 minutes
