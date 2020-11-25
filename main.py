import gpxpy
import gpxpy.gpx
import datetime
import matplotlib.pyplot as plt
from geopy import distance
import numpy as np
import pandas as pd
import chart_studio.plotly as py
import haversine

gpx_file = open('gpxfiles/Bournemouth_Half.gpx', 'r')

gpx = gpxpy.parse(gpx_file)
print (len(gpx.tracks))

track = gpx.tracks[0]
segment = track.segments[0]
points = segment.points


#for p in points:
 #   data.append((p.longitude, p.latitude, p.elevation, p.time))

df = pd.DataFrame(columns=['long', 'lat', 'elev', 'time'])

for point in points:
    df = df.append({'long': point.longitude, 'lat': point.latitude, 'elev': point.elevation, 'time': point.time}, ignore_index=True)

#print (df)

#plotting data

plot= plt.plot(df['long'], df['lat'])
print (dir(plot))




#distance formula: distance_3d = sqrt(distance_2d**2 + (elev2-elev1)**2)

elevDif = [0]
timeDif = [0]
distVin = [0]
distHav = [0]
distVinNoElev = [0]
distHavNoAlt = [0]
distDifHav2D = [0]
distDifVin2D = [0]

for index in range(len(points)):
    if index == 0:
        pass
    else:
        start = points[index-1]
        stop = points[index]
        distanceVin2D = 