from typing import List, Any
import itertools
from itertools import groupby
from .config_heading import Angle
from .config_distance import Distance
from .config_info_anomalies import Anomaly_index
import os

DOWN_RATIO = 0.5
SEQUENCE_LIMIT = 10
ALTITUDE_LOWER = 0
ALTITUDE_UPPER = 1500


def first_point(anomaly_points, extracted_seq, seq):
    """
    First points of sequences has marked as anomaly or
    not anomaly, with comparing second point.
    """
    if len(extracted_seq) > 1 and seq[1] in extracted_seq:
        extracted_seq.append(seq[0])
    else:
        anomaly_points.append(seq[0])
    return extracted_seq, anomaly_points


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def key_func(k):
    return k['SequenceUUID']


class AnomalyConfig:
    down_percent: float = DOWN_RATIO
    sequence_limit: int = SEQUENCE_LIMIT
    altitude_lower: int = ALTITUDE_LOWER
    altitude_upper: int = ALTITUDE_UPPER


class Sequence:
    """
    sequence based anomaly
    detects and returns anomaly points
    """

    extracted_seq: List[Any]
    anomaly_points: List[Any]

    def __init__(self, descs):
        self.information = list(descs).pop()
        descs = list(descs)[:-1]
        self.descs = [desc for desc in descs if ("error" not in desc) and ("Heading" in desc)]
        self.sequences = []
        self.distribution = []
        self.anomalies = []
        self.withanomalies = []

    def list_dist(self, zipped, seq, pair_head):
        """
        :param pair_head:
        :param zipped: format (Latitude,Latitude,Longitude,Longitude)
        :param seq: squence
        :return: data with anomalies removed
        """
        extracted_seq = []
        anomaly_points = []
        if len(seq) < AnomalyConfig.sequence_limit:
            anomaly_points = seq
        else:
            for i in range(len(zipped)):
                ang = Angle()
                distance = Distance()
                rang = ang.rang(pair_head[i])
                if distance.gps_distance(zipped[i][0], zipped[i][1]) < distance.distance_limit and\
                        rang < ang.header_limit:

                    dicton = (next(dic for dic in seq if (dic['Latitude'] == zipped[i][0][1])))
                    if dicton['Altitude'] < AnomalyConfig.altitude_upper:
                        extracted_seq.append(dicton)
                    else:
                        anomaly_points.append(dicton)
                else:
                    out_range = (next(dic for dic in seq if (dic['Latitude'] == zipped[i][0][1])))
                    anomaly_points.append(out_range)

        # extracted_seq, anomaly_points = first_point(anomaly_points,extracted_seq,seq)
        ratio_seq = len(extracted_seq) / (len(extracted_seq) + len(anomaly_points))

        if ratio_seq < AnomalyConfig.down_percent:
            extracted = []
            anomalies = seq
            uuud = (anomalies[0]['SequenceUUID'])

        else:
            extracted = extracted_seq
            anomalies = anomaly_points
            uuud = []

        ai = Anomaly_index()
        extracted = ai.info_anomalies(extracted, False)
        anomalies = ai.info_anomalies(anomalies, True)
        withanomaly = extracted + anomalies

        return extracted, anomalies, uuud, withanomaly

    def groupy_to_result(self):
        """
        - Group the sequences, remove that has one element sequences.
        - For each series, calculate distance of all points in the sequences.
        - using anomaly/sequence ratio, get the final result sequences extracted anomalies
        :return:
        """
        uud = []
        for _, val in groupby(self.descs, key_func):
            self.sequences.append(list(val))
        for sequen in self.sequences:
            latitude = []
            longitude = []
            heading = []
            for seq in sequen:
                latitude.append(seq['Latitude'])
                longitude.append(seq['Longitude'])
                heading.append(seq['Heading'])
            pair_lat, pair_lon, pair_head = pairwise(latitude), pairwise(longitude), pairwise(heading)
            zipped = list(zip(pair_lat, pair_lon))
            extracted, anomalies, uuud, withanomaly = self.list_dist(zipped, sequen, pair_head)
            self.distribution.append(extracted)
            self.anomalies.append(anomalies)
            uud.append(uuud)
            self.withanomalies.append(withanomaly)

        return self.distribution, self.information, self.anomalies, uud, self.withanomalies


class Info:
    """
    Notices failure sequence UUID,
    anomaly points' image names.
    """

    def create_list_filename(self, distrubution):
        """
        appends result to one list
        :param distrubution:
        :return:
        """
        file_list = []
        for sequences in distrubution:
            for seq in sequences:
                if type(seq) == dict:
                    file_list.append(os.path.join(seq['filename']))
        return file_list

    def update_info(self, info, file_names, uud):
        info['Information']['processed_images'] = info['Information']['processed_images'] - len(file_names)
        info['Information']['failed_images'] = info['Information']['failed_images'] + len(file_names)
        uud = [lis for lis in uud if lis != []]
        info['Information']['anomaly_sequences'] = uud
        return info

    def create_json(self, distrubution, info):
        """
        appends result to one list
        :param info:
        :param distrubution:
        :return:
        """
        united_sequences = []
        for sequences in distrubution:
            for seq in sequences:
                if type(seq) == dict:
                    united_sequences.append(seq)
        united_sequences.append(info)
        return united_sequences


def mark_points(decs):

    """
        - Group the sequences, remove that has one element sequences.
        - For each series, calculate distance of all points in the sequence.
        - using length anomaly/sequence ratio, get the final result sequences extracted anomalies
    """
    data_all = Sequence(decs)
    info = Info()
    extracted, information, anomaly, uud, withanomaly = data_all.groupy_to_result()
    filenames_list = info.create_list_filename(anomaly)
    information = info.update_info(information, filenames_list, uud)
    extracted = info.create_json(withanomaly, information)
    anomaly_points = info.create_json(anomaly, information)
    return extracted, filenames_list, anomaly_points
