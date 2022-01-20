import math
import itertools
import os.path
from itertools import groupby
import json

DOWN_RATIO = 0.3
UP_RATIO = 0.7


class AnomalyConfig:
    down_percent: float = DOWN_RATIO
    up_percent: float = UP_RATIO


def key_func(k):
    return k['SequenceUUID']


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def ecef_from_lla(lat, lon, alt):
    """
    Compute ECEF XYZ from latitude, longitude and altitude.

    All using the WGS94 model.
    Altitude is the distance to the WGS94 ellipsoid.
    Check results here http://www.oc.nps.edu/oc2902w/coord/llhxyz.ht
    """
    WGS84_a = 6378137.0
    WGS84_b = 6356752.314245
    a2 = WGS84_a ** 2
    b2 = WGS84_b ** 2
    lat = math.radians(lat)
    lon = math.radians(lon)
    L = 1.0 / math.sqrt(a2 * math.cos(lat) ** 2 + b2 * math.sin(lat) ** 2)
    x = (a2 * L + alt) * math.cos(lat) * math.cos(lon)
    y = (a2 * L + alt) * math.cos(lat) * math.sin(lon)
    z = (b2 * L + alt) * math.sin(lat)
    return x, y, z


def gps_distance(latlon_1, latlon_2):
    """
    :param latlon_1: 2 Latitude points
    :param latlon_2: 2 Longitude points
    :return:
    """
    x1, y1, z1 = ecef_from_lla(latlon_1[0], latlon_2[0], 0.0)
    x2, y2, z2 = ecef_from_lla(latlon_1[1], latlon_2[1], 0.0)
    dis = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return dis


def list_dist(zipped, seq):
    """
    :param zipped: format (Latitude,Latitude,Longitude,Longitude)
    :param seq: squence
    :return: data with anomalies removed
    """
    extracted_seq = []
    anomaly_points = []
    for i in range(len(zipped)):
        if not (gps_distance(zipped[i][0], zipped[i][1])) > 50:
            extracted_seq.append(next(dic for dic in seq if dic['Latitude'] == zipped[i][0][1]))
        else:
            anomaly_points.append(next(dic for dic in seq))
    ratio_seq = len(extracted_seq) / len(seq)
    if ratio_seq < AnomalyConfig.up_percent:
        extracted = []
        anomalies = seq
    elif ratio_seq > AnomalyConfig.down_percent:
        extracted = seq
        anomalies = []
    else:
        extracted = extracted_seq
        anomalies = anomaly_points
    return extracted, anomalies


def groupy_to_result(descs):
    """
    - Group the sequances, remove that has one element sequances.
    - For each series, calculate distance of all points in the sequences.
    - using anomaly/sequence ratio, get the final result sequences extracted anomalies
    :param descs: json file of gps
    :return:
    """
    information = list(descs).pop()
    descs = list(descs)[:-1]
    descs = [desc for desc in descs if ("error" not in desc) and (("Heading" in desc))]
    sequances = []
    for _, val in groupby(descs, key_func):
        sequances.append(list(val))
    disrubution = []
    filenames = []
    for sequance in sequances:
        latitude = []
        longitude = []
        for seq in sequance:
            latitude.append(seq['Latitude'])
            longitude.append(seq['Longitude'])
        pair_lat = pairwise(latitude)
        pair_lon = pairwise(longitude)
        zipped = list(zip(pair_lat, pair_lon))
        disrubution.append(list_dist(zipped, sequance)[0])
        filenames.append(list_dist(zipped, sequance)[1])
    return disrubution, information, filenames


def create_json(distrubution, info):
    """
    appends result to one list
    :param distrubution:
    :return:
    """
    united_sequances = []
    for sequances in distrubution:
        for seq in sequances:
            if type(seq) == dict:
                united_sequances.append(seq)

    united_sequances.append(info)
    return united_sequances


def filename_list(distrubution):
    """
    appends result to one list
    :param distrubution:
    :return:
    """
    united_sequances = []
    for sequances in distrubution:
        for seq in sequances:
            if type(seq) == dict:
                united_sequances.append(os.path.join(seq['filename']))
    return united_sequances


def extract_result(decs):
    extracted, info, filenames = groupy_to_result(decs)
    extracted = create_json(extracted, info)
    filenames = filename_list(filenames)
    return extracted, filenames
