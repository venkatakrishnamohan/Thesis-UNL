import mysql.connector
import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
connection = mysql.connector.connect(host='localhost',
                            user='root',
                            passwd='pass123',
                            db='twitter_research',
                            charset='ascii',
                            use_unicode= True)
cursor = connection.cursor()
df = pd.read_sql("SELECT Text, PyBoolean, Latitude, Longitude from TWITTERMAPS;", con=connection)


map = folium.Map(location=[22.365, 79.344], zoom_start=5)
'''
for index, row in df.iterrows():

    folium.CircleMarker([row['Latitude'], row['Longitude']],
                        radius=5,
                        fill_color="#3db7e4", # divvy color
                       ).add_to(map)
'''

heat_data = [[row['Latitude'],row['Longitude']] for index, row in df.iterrows()]

HeatMap(heat_data).add_to(map)



map.save(outfile='keyword_map.html')
