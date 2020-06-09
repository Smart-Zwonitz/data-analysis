from xml.sax import make_parser, handler
from os import listdir
import netex_analysis

PATH = "../data/vms_RV2"


def removeStopCode(str):
    return str.replace('DE::StopPlace:','').replace('_vms::','')

def transform_station_id(stopPlaces):
    return list(map(removeStopCode, stopPlaces))

def get_stations():

    files = listdir(PATH)

    parser = make_parser()

    line_files = list()

    for file in files:
        q = netex_analysis.StopPositionHandler()
        print(f"processing {file}")
        parser.setContentHandler(q)
        parser.parse(PATH + "/" + file)
        params = (file, q.lines, transform_station_id(q.stopPlaces), q.stopPlaces, q.parents)
        line_files.append(params)

    return line_files

def filter_stations(stations):
    lines = get_stations()
    line_files = list()
    for line in lines:
        if any(x in stations for x in line[2]):
            line_files.append(line)
    return line_files
