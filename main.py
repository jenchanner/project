import gpxpy
import gpxpy.gpx
import datetime
import matplotlib.pyplot as plt
from geopy import distance
import pandas as pd
import haversine
from math import sqrt, floor

gpx_file = open('gpxfiles/Bournemouth_Half.gpx', 'r')

gpx = gpxpy.parse(gpx_file)
print (len(gpx.tracks))

track = gpx.tracks[0]
segment = track.segments[0]
points = segment.points

# for ex in p.extensions[0]: print('ex' + ex.text)
data = []


for point in points:
    data.append({'long': point.longitude, 'lat': point.latitude, 'elev': point.elevation, 'time': point.time})

df = pd.DataFrame(data=data, columns=['long', 'lat', 'elev', 'time'])

#distance formula: distance_3d = sqrt(distance_2d**2 + (elev2-elev1)**2)

elevDif = [0]
timeDif = [0]
distHav = [0]
distHavNoElev = [0]
distDifHav2D = [0]
#distanceHav2D = [0]
pace = [0]

for index in range(1, len(points)):
    start = points[index-1]
    stop = points[index]

    distanceHav2D = haversine.haversine((start.latitude, start.longitude), (stop.latitude, stop.longitude))*1000

    distDifHav2D.append(distanceHav2D)
    distHavNoElev.append(distHavNoElev[-1] + distanceHav2D)
    elevD = stop.elevation - start.elevation
    elevDif.append(elevD)
    distanceHav3D = sqrt(distanceHav2D**2 + (float(elevD)**2))
    timeDelta = (stop.time - start.time).total_seconds()
    timeDif.append(timeDelta)
    distHav.append(distHav[-1] + distanceHav3D)
    pace.append(16.66667/ (distanceHav3D / timeDelta))


df['distHave2D']= distHavNoElev
df['distHav3D'] = distHav
df['elevDif'] = elevDif
df['timeDif'] = timeDif
df['pace'] = pace

print('Haversine 2D : ', distHavNoElev[-1], 'm')
print('Haversine 3D : ', distHav[-1], 'm')
print('Total time : ', floor(sum(timeDif)/60), 'min', int(sum(timeDif)%60), 'sec')
#print('Pace : ', 16.666667 / pace, 'min/km')

gain = sum([x for x in df['elevDif'] if x>0])
print('Gain = {0}'.format(gain))
#print(df)
plt.plot(df['long'], df['lat'])
plt.title('Plot', fontsize=14)
plt.xlabel('long', fontsize=14)
plt.ylabel('lat', fontsize=14)
plt.grid(False)

plt.savefig('Plot.png')
#plt.show()

plt.plot(df['distHav3D'], df['elev'])
plt.title('Elevation', fontsize=14)
plt.xlabel('Distance', fontsize=14)
plt.ylabel('Elevation', fontsize=14)
plt.grid(False)

plt.savefig('Elevation.png')
#plt.show()

averagePace = sum(df['pace']/ len (df['pace']))
averagePaceMins = floor(averagePace)
averagePaceSecs = int(60 * (averagePace - averagePaceMins))

print('average pace : {0}:{1}min/km'.format(averagePaceMins, averagePaceSecs))