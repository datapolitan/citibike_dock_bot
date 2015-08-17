import requests
import collections
import psycopg2
import psycopg2.extras
import twython
from time import sleep

from keys_boro import keys

id_boro_dict = collections.defaultdict(str) #dictionary of station ids to boro
process_date = None
daily_stat = collections.defaultdict(list) # dictionary of stats keyed on timestamp, value = list[total,Mnhtn,brkyln,qns]


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
    global process_date
    
    curr_date = r.json()['executionTime'][:10] 
    access_time = ts = parser.parse(r.json()['executionTime'][11:]).strftime("%H:%M")
    
    # check if processing date is null
    if process_date is None:
        process_date = curr_date
#    elif process_date != curr_date:
        #flush out report
#        with open('%s_output.csv' % process_date) as outputFile:
#            for k,v in daily_stat.iteritems():
    # Check the curr date against the processing date
    
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
    tweet_status(avail_bikes_sum,totalDocks_sum,in_service_station_sum,boro_dict)   
    
    #update the daily stats
    boro_order = ['Manhattan','Brooklyn','Queens']
    boro_bike_list = []
    for b in boro_order:
        boro_bike_list.append(str(boro_dict[b]))
    daily_stat[access_time] = [str(avail_bikes_sum)] + boro_bike_list
    return daily_stat

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
    #twitter.update_status(status="%s #Citibikes are available in %s active docks, %s in #Manhattan, %s in #Brooklyn, and %s in #Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens'])))
    print "%s Citibikes are available in %s active docks, %s in Manhattan, %s in Brooklyn, and %s in Queens" % ("{:,.0f}".format(avail_bikes_sum),"{:,.0f}".format(totalDocks_sum),"{:,.0f}".format(boro_dict['Manhattan']),"{:,.0f}".format(boro_dict['Brooklyn']),"{:,.0f}".format(boro_dict['Queens']))
    return

#####program execution starts

get_id_boro() #initialize id_boro_dict and boro_list from database on first run

while True: #infinite loop 
    get_cb_dock() #get dock count and tweet
    sleep(600) #sleep for 10 minutes
