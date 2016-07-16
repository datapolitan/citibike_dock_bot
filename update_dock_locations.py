'''
A script to update the citibike ids and locations 
'''

import collections
import requests
import psycopg2
from pgconnect import pgconnect

db = pgconnect['db']
user = pgconnect['user']
host = pgconnect['host']

con = psycopg2.connect(database=db, user=user, host=host, port=5432)
cur = con.cursor()

r = requests.get('http://www.citibikenyc.com/stations/json')

loc_dict = collections.defaultdict(list)
for station in r.json()['stationBeanList']:
    loc_dict[station['id']] = [station['latitude'],station['longitude']]

#delete rows in the table
cur.execute(open("create_dock_location.sql",'r').read())
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