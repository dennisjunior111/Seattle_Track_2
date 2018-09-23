import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin

raw = pd.read_csv('../data/AIS_ASCII_by_UTM_Month/2017/AIS_2017_01_Zone01.csv')

def euclideanDistance(shipA, shipB):
    return np.linalg.norm(np.array([shipA.LAT,shipA.LON])-np.array([shipB.LAT,shipB.LON]))

def haversineDistance(shipA, shipB):
    # "the great circle arc length based on a spherical Earth"
    # courtesy of https://rosettacode.org/wiki/Haversine_formula
    R = 6372.8 # Earth radius in kilometers
    # Does this mean output is in kilometers?
    lat1 = shipA.LAT; lon1 = shipA.LON;
    lat2 = shipB.LAT; lon2 = shipB.LON;
    dLat = radians(lat2 - lat1);
    dLon = radians(lon2 - lon1);
    lat1 = radians(lat1); lat2 = radians(lat2);
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2;
    c = 2*asin(sqrt(a));
    return R * c

def predictInteractions(df, distanceFn, distanceThreshold):
    ships = {}
    ship_ids = [None]
    interactions = []
    df = df.sort_values(by="BaseDateTime")
    # for each AIS datapoint
    for x in df.iterrows():
        record = x[1]
        # update status of this vessel
        ships[record.MMSI] = record
        # and if the previous record was a different ship...
        if ship_ids[-1] != record.MMSI:
            if record.MMSI in ship_ids:
                # find the ships that have reported since this ship last reported
                last_index_of_this_ship = len(ship_ids) - 1 - ship_ids[::-1].index(record.MMSI)
                potential_interaction_ships = ship_ids[last_index_of_this_ship + 1:]
                # and evaluate their distances
                for vessel in potential_interaction_ships:
                    calculatedDistance = distanceFn(ships[vessel], ships[record.MMSI]);
                    if(calculatedDistance < distanceThreshold):
                        interactions.append({ \
                            "time": record.BaseDateTime, \
                            "shipA": ships[vessel], \
                            "shipB":record, \
                            "distance": calculatedDistance \
                        })
                        # TODO: Compare distance to existing interactions
                            # If new_dist > old_dist, interaction has ended
                            # Else update interaction record with new Distance

            else:
                ship_ids.append(record.MMSI)

    print(len(interactions))
    for i in range(0,5):
        print(interactions[i])
        print()

    return interactions

# predictInteractions(raw, euclideanDistance, 2.0)
