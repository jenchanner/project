import gpxpy
import gpxpy.gpx
import datetime
import matplotlib.pyplot as plt
from geopy import distance
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import haversine

gpx_file = open('gpxfiles/Bournemouth_Half.gpx', 'r')

gpx = gpxpy.parse(gpx_file)
print (len(gpx.tracks))

track = gpx.tracks[0]
segment = track.segments[0]
points = segment.points

data = []
for p in points:
    data.append((p.longitude, p.latitude, p.elevation, p.time))

print(data)