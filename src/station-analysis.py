

import csv
import folium

class station:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lon = float(lon.replace(',','.'))
        self.lat = float(lat.replace(',','.'))

stations = []

with open('../data/haltestellen-zwoenitz.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        stations.append(station(row['Name'],row['Latitude'], row['Longitude']))

m=folium.Map(
    location=[50.6298, 12.8128],
    zoom_start=10
)


for station in stations:
    print(f'Name={station.name}, Lat={station.lat}, Lon={station.lon}')
    folium.Marker([station.lat, station.lon], popup=station.name, tooltip=station.name).add_to(m)
    folium.Circle([station.lat, station.lon], radius=600).add_to(m)

m.save('stations-zwoenitz.html')

m
