import requests
import psycopg2
from _collections import defaultdict
import datetime
from dateutil import parser
from time import sleep

# water_st_docks = [ 259, 260, 315, 337, 351, 415, 427, 534 ]

def retrieve_upload_cb_dock():
    r = requests.get('http://www.citibikenyc.com/stations/json')

    con = psycopg2.connect(database="waterstreetcb", user="datapolitan", host="waterstreet-cb.c3y68wob3ar5.us-east-1.rds.amazonaws.com")
    cur = con.cursor()

    station_dict = defaultdict(int)
    for i in r.json()['stationBeanList']:
        if i['id'] in water_st_docks:
            station_dict[i['id']] = i['availableBikes']

    #parse datetime object
    exec_time = parser.parse(r.json()['executionTime'])
    #construct value string
    val_list = []
    for val in water_st_docks:
        val_list.append(station_dict[val])
    

    #execute the insert
    cur.execute("INSERT INTO water_st.cb_dock (access_time, station_259, station_260, station_315, station_337, station_351, station_415, station_427, station_534, exec_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(datetime.datetime.now(),val_list[0], val_list[1], val_list[2], val_list[3], val_list[4], val_list[5], val_list[6], val_list[7], exec_time))
    #commit the transaction at the end of the processing
    con.commit()
    con.close()

while True:
    retrieve_upload_cb_dock()
    sleep(60)