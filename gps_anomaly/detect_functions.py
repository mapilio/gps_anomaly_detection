from typing import List, Any
import itertools
from itertools import groupby
from config_heading import Angle
from config_distance import Distance
import os

DOWN_RATIO = 0.3
UP_RATIO = 0.9


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def key_func(k):
    return k['SequenceUUID']


class AnomalyConfig:
    down_percent: float = DOWN_RATIO
    up_percent: float = UP_RATIO


class Sequance:

    extracted_seq: List[Any]
    anomaly_points: List[Any]

    def __init__(self, descs):
        self.information = list(descs).pop()
        descs = list(descs)[:-1]
        self.descs = [desc for desc in descs if ("error" not in desc) and ("Heading" in desc)]
        self.sequances = []
        for _, val in groupby(self.descs, key_func):
            self.sequances.append(list(val))
        self.disrubution = []
        self.anomalies = []

    def list_dist(self, zipped, seq, pair_head):
        """
        :param pair_head:
        :param zipped: format (Latitude,Latitude,Longitude,Longitude)
        :param seq: squence
        :return: data with anomalies removed
        """
        extracted_seq = []
        anomaly_points = []
        for i in range(len(zipped)):
            ang = Angle()
            distance = Distance()
            rang = ang.rang(pair_head[i])
            if distance.gps_distance(zipped[i][0], zipped[i][1]) < distance.distance_limit and rang < ang.header_limit:
                dicton = (next(dic for dic in seq if (dic['Latitude'] == zipped[i][0][1])))
                if dicton['Altitude'] > 0:
                    extracted_seq.append(dicton)
                else:
                    anomaly_points.append(dicton)
            else:
                anomaly_points.append(next(dic for dic in seq))
        ratio_seq = len(extracted_seq) / len(seq)

        if ratio_seq < AnomalyConfig.down_percent:
            extracted = []
            anomalies = seq
        elif ratio_seq > AnomalyConfig.up_percent:
            extracted = seq
            anomalies = []
        else:
            extracted = extracted_seq
            anomalies = anomaly_points
        return extracted, anomalies

    def groupy_to_result(self):
        """
        - Group the sequances, remove that has one element sequances.
        - For each series, calculate distance of all points in the sequences.
        - using anomaly/sequence ratio, get the final result sequences extracted anomalies
        :return:
        """

        for sequan in self.sequances:
            latitude = []
            longitude = []
            heading = []
            for seq in sequan:
                latitude.append(seq['Latitude'])
                longitude.append(seq['Longitude'])
                heading.append(seq['Heading'])
            pair_lat, pair_lon, pair_head = pairwise(latitude), pairwise(longitude), pairwise(heading)
            zipped = list(zip(pair_lat, pair_lon))
            self.disrubution.append(self.list_dist(zipped, sequan, pair_head)[0])
            self.anomalies.append(self.list_dist(zipped, sequan, pair_head)[1])
        return self.disrubution, self.information, self.anomalies


class Info:

    def create_list_filename(self, distrubution):
        """
        appends result to one list
        :param distrubution:
        :return:
        """
        file_list = []
        for sequances in distrubution:
            for seq in sequances:
                if type(seq) == dict:
                    file_list.append(os.path.join(seq['filename']))
        return file_list

    def update_info(self, info, file_names):
        info['Information']['processed_images'] = info['Information']['processed_images'] - len(file_names)
        info['Information']['failed_images'] = info['Information']['failed_images'] + len(file_names)
        return info

    def create_json(self, distrubution, info):
        """
        appends result to one list
        :param info:
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