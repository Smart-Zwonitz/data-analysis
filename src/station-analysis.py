

import csv
import folium

from select_stations import filter_stations


class station:
    def __init__(self, name, id, lat, lon):
        self.name = name
        self.id = id
        self.lon = float(lon.replace(',','.'))
        self.lat = float(lat.replace(',','.'))

def get_lines_for_station(station_id, lines):
    lines_f_station = filter(lambda x : station_id in x[2], lines)
    list_of_lists = (line[1] for line in lines_f_station)
    return [val for sublist in list_of_lists for val in sublist]

stations = []

with open('../data/haltestellen-zwoenitz.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        stations.append(station(row['Name'], row['DHID'], row['Latitude'], row['Longitude']))

dhids = set(map(lambda x : x.replace('de:14521:','')
            , set(o.id for o in stations)))

line_files = filter_stations(dhids)

print(line_files)

m=folium.Map(
    location=[50.6298, 12.8128],
    zoom_start=10
)


for station in stations:
    print(f'Name={station.name}, Lat={station.lat}, Lon={station.lon}')
    lines = get_lines_for_station(station.id.replace('de:14521:',''), line_files)
    lines_per_station = len(lines)

    color = "#" \
            + hex(255 - (int(255 * lines_per_station / 4))).lstrip("0x").rstrip("L").zfill(2) \
            + hex(int(255 * lines_per_station / 4)).lstrip("0x").rstrip("L").zfill(2) \
            + "00"

    print(color)

    tooltip = f"""
        {station.name}<br/>
        DHID: {station.id}<br/>
        Lines: {','.join(lines)}
    """
    folium.Marker([station.lat, station.lon], popup=station.name, tooltip=tooltip, color=color).add_to(m)
    folium.Circle([station.lat, station.lon], radius=600, color=color).add_to(m)

m.save('stations-zwoenitz.html')

m


