#-------------------------------------------------------------------------#
# This program takes latitude and longitude from selection of
# the twitter database and returns physical address, including
# country code.
#
#  Author: Timothy Grant Clark
#  Date Created: May 25th 2018
#  Python Version: 3.6
#------------------------------------------------------------------------#
import mysql.connector
import pandas as pd
from geopy.geocoders import Nominatim
connection = mysql.connector.connect(host='localhost',
                            user='root',
                            passwd='pass123',
                            db='twitter_research',
                            charset='ascii',
                            use_unicode= True)
cursor = connection.cursor()
df = pd.read_sql("SELECT id, PyBoolean, Latitude, Longitude from TWEETS WHERE Important=1;", con=connection)

#print(df)

f = open('results.txt', mode='w+', encoding='utf-8')

geoLocator = Nominatim()
for (index, row) in df.iterrows():
    lat = str(df.at[index, 'Latitude'])
    lon = str(df.at[index, 'Longitude'])
    coord = (lat+ ", "+lon)
    id = str(df.at[index, 'id'])
    loc = geoLocator.reverse(coord, language='en')
    print(loc.raw['address'], file=f)
