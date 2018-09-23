import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import datetime


def loadData(FILENAME):
    return pd.read_csv('../data/AIS_ASCII_by_UTM_Month/2017/'+FILENAME)

def haversineDistance(shipA, shipB):
    # "the great circle arc length based on a spherical Earth"
    # courtesy of https://rosettacode.org/wiki/Haversine_formula
    R = 6372.8 # Earth radius in kilometers
    # Does this mean output is in kilometers?
    lat1 = shipA[0]; lon1 = shipA[1];
    lat2 = shipB[0]; lon2 = shipB[1];
    dLat = radians(lat2 - lat1);
    dLon = radians(lon2 - lon1);
    lat1 = radians(lat1); lat2 = radians(lat2);
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2;
    c = 2*asin(sqrt(a));
    return R * c

DISTANCE_THRESHOLD = 7408
# 7408M == 4 nautical miles

def findInteractions(dataframe, distanceFn, threshold):
    df = dataframe.sort_values(by='BaseDateTime')
    df['BaseDateTime'] = pd.to_datetime(df.BaseDateTime)
    vessel_status = {}
    interactions = {}
    counter = 0
    ONE_HOUR = datetime.timedelta(hours=1)
    for row in df.iterrows():
        counter = counter + 1
        if counter % 100 == 0:
            print(str(round(counter * 100/len(df), 2))+"% complete");
        record = row[1]
        if record.MMSI not in vessel_status:
             vessel_status[record.MMSI] = { \
                'locations': [(record.LAT, record.LON)], \
                'firstUpdate': str(record.BaseDateTime), \
                'lastUpdate': str(record.BaseDateTime), \
                'MMSI': record.MMSI \
            }
        vessel_status[record.MMSI]['lastUpdate'] = str(record.BaseDateTime)
        vessel_status[record.MMSI]['locations'].append((record.LAT, record.LON))
        distances_to_other_vessels = {}
        for ship in vessel_status.keys():
            if ship != record.MMSI:
                other_ship = vessel_status[ship]
                other_ship_location = other_ship['locations'][-1]
                distances_to_other_vessels[ship] = distanceFn((record.LAT, record.LON), other_ship_location)
                if distances_to_other_vessels[ship] <= threshold:
                    if (ship*record.MMSI) not in interactions:
                        timeDelta = record.BaseDateTime - pd.to_datetime(other_ship['lastUpdate'])
                        if timeDelta < ONE_HOUR:
                            interactions[ship*record.MMSI] = { \
                                record.MMSI: vessel_status[record.MMSI], \
                                ship:other_ship, \
                                "time": str(record.BaseDateTime), \
                                # "distance": distances_to_other_vessels[ship], \
                                "timeDelta": timeDelta.total_seconds \
                            }
        # vessel_status[record.MMSI]['currentDistances'] = distances_to_other_vessels

    return {"vessels": vessel_status, "interactions": interactions}


def findSimpleInteractions(dataframe, distanceFn, threshold):
    df = dataframe.sort_values(by='BaseDateTime')
    df['BaseDateTime'] = pd.to_datetime(df.BaseDateTime)
    vessel_status = {}
    interactions = {}
    counter = 0
    ONE_HOUR = datetime.timedelta(hours=1)
    for row in df.iterrows():
        counter = counter + 1
        if counter % 100 == 0:
            print(str(round(counter * 100/len(df), 2))+"% complete");
        record = row[1]
        if record.MMSI not in vessel_status:
             vessel_status[record.MMSI] = { \
                'locations': [(record.LAT, record.LON)], \
                'firstUpdate': str(record.BaseDateTime), \
                'lastUpdate': str(record.BaseDateTime), \
                'MMSI': record.MMSI \
            }
        vessel_status[record.MMSI]['lastUpdate'] = str(record.BaseDateTime)
        vessel_status[record.MMSI]['locations'].append((record.LAT, record.LON))
        distances_to_other_vessels = {}
        for ship in vessel_status.keys():
            if ship != record.MMSI:
                other_ship = vessel_status[ship]
                other_ship_location = other_ship['locations'][-1]
                distances_to_other_vessels[ship] = distanceFn((record.LAT, record.LON), other_ship_location)
                if distances_to_other_vessels[ship] <= threshold:
                    if (ship*record.MMSI) not in interactions:
                        timeDelta = record.BaseDateTime - pd.to_datetime(other_ship['lastUpdate'])
                        if timeDelta < ONE_HOUR:
                            interactions[ship*record.MMSI] = { \
                                "shipA": record.MMSI, \
                                "shipATime": str(record.BaseDateTime), \
                                "shipB": ship, \
                                "shipBTime": str(other_ship['lastUpdate']), \
                                #"startTime": str(record.BaseDateTime),
                                "startTime": str(other_ship['lastUpdate']), \
                                "distance": distances_to_other_vessels[ship], \
                                "timeDelta": timeDelta.total_seconds() \
                            }
                    else:
                        timeDelta = record.BaseDateTime - pd.to_datetime(other_ship['lastUpdate'])
                        if timeDelta < ONE_HOUR:
                            interactions[ship*record.MMSI]['endTime'] = str(record.BaseDateTime);
    return {"vessels": vessel_status, "interactions": interactions}

def exportSimpleInteractions(interactions, FILENAME):
    z = pd.DataFrame(interactions).T;
    z.rename(columns={"Unnamed: 0": "UUID"})
    z.to_csv("Interactions_"+FILENAME)


def doItAll(FILENAME):
    a = loadData(FILENAME)
    z = findSimpleInteractions(a, haversineDistance, DISTANCE_THRESHOLD)
    return exportSimpleInteractions(z['interactions'], FILENAME)
