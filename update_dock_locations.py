'''
A script to update the citibike ids and locations 
'''

import collections
import requests
import psycopg2

con = psycopg2.connect(database="utility", user="datapolitan", host="utility.c1erymiua9dx.us-east-1.rds.amazonaws.com")
cur = con.cursor()

r = requests.get('http://www.citibikenyc.com/stations/json')

loc_dict = collections.defaultdict(list)
for station in r.json()['stationBeanList']:
    loc_dict[station['id']] = [station['latitude'],station['longitude']]

#delete rows in the table
cur.execute("DELETE FROM citibikedock.dock_location")
con.commit()

#write new rows to table
sql = "INSERT INTO citibikedock.dock_location (id,latitude,longitude) VALUES (%s,%s,%s)"
for k,v in loc_dict.iteritems():
    cur.execute(sql,(k,v[0],v[1]))
con.commit()

#set geometry based on points
cur.execute("UPDATE citibikedock.dock_location SET geom = ST_SetSRID(ST_MAKEPOINT(longitude,latitude),4326)")
con.commit()

con.close()