from typing import List, Any
from itertools import groupby
from .config.heading import Angle
from .config.info_anomalies import Anomaly_index
from .config.distance import Distance
import itertools

DOWN_RATIO = 0.2
SEQUENCE_LIMIT = 10
ALTITUDE_LOWER = 0    ##removed this condition, can be added on line71
ALTITUDE_UPPER = 1500


class AnomalyConfig:
    down_percent: float = DOWN_RATIO
    sequence_limit: int = SEQUENCE_LIMIT
    altitude_lower: int = ALTITUDE_LOWER
    altitude_upper: int = ALTITUDE_UPPER


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def key_func(k):
    return k['sequenceUuid']


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
        self.descs = [desc for desc in descs if ("error" not in desc) and ("heading" in desc)]
        self.sequences = []
        self.distribution = []
        self.anomalies = []
        self.withanomalies = []
        self.uud = []
        self.order_seq = []


    def list_dist(self, zipped, seq, pair_head):
        """
        :param pair_head:
        :param zipped: format (latitude,latitude,longitude,longitude)
        :param seq: squence
        :return: data with anomalies removed
        """
        extracted_seq = []
        anomaly_points = []
        ai = Anomaly_index()
        ang = Angle()
        distance = Distance()
        if len(seq) < AnomalyConfig.sequence_limit:
            anomaly_points = seq
        else:
            for i in range(len(zipped)):
                rang = ang.rang(pair_head[i])
                reasons = []
                dis=distance.gps_distance(zipped[i][0],zipped[i][1])
                # Check distance condition
                if not (distance.distance_low_limit < dis < distance.distance_limit):
                    reasons.append(f"Distance condition not met. The distance: {dis}")

                # Check range condition
                if rang >= ang.header_limit:
                    reasons.append("Range condition not met")

                dicton = next(dic for dic in seq if dic['latitude'] == zipped[i][0][1])

                # Check altitude condition
                if AnomalyConfig.altitude_upper <= dicton['altitude']:
                    reasons.append("Altitude above upper limit")

                # If any reason is present, handle as anomaly
                if reasons:
                    anomaly_points.append(dicton)
                    reason_text = ", ".join(reasons)
                    seq[i] = ai.update_info(seq[i], detect=True, reason=reason_text)
                    if i == len(zipped) - 1:  # Adjusted to avoid index out of range error
                        seq[i] = ai.update_info(seq[i], detect=True, reason=reason_text)
                        seq[i + 1] = ai.update_info(seq[i + 1], detect=True, reason=reason_text)
                else:
                    # If no anomaly, handle normally
                    extracted_seq.append(dicton)
                    seq[i] = ai.update_info(seq[i], detect=False)
                    if i == len(zipped) - 1:  # Adjusted to avoid index out of range error
                        seq[i] = ai.update_info(seq[i], detect=False)
                        seq[i + 1] = ai.update_info(seq[i + 1], detect=False)

        # extracted_seq, anomaly_points = first_point(anomaly_points,extracted_seq,seq)
        ratio_seq = len(extracted_seq) / (len(extracted_seq) + len(anomaly_points))

        if ratio_seq < AnomalyConfig.down_percent or len(extracted_seq) < 5:
            extracted = []
            seq = ai.info_anomalies(seq, True)
            anomalies = seq
            uuud = (anomalies[0]['sequenceUuid'])

        else:
            extracted = extracted_seq
            anomalies = anomaly_points
            uuud = []

        extracted = ai.info_anomalies(extracted, False)
        anomalies = ai.info_anomalies(anomalies, True)
        withanomaly = extracted + anomalies
        # withanomaly.sort(key=lambda x: x['CaptureTime'])

        return extracted, anomalies, uuud, withanomaly, seq

    def groupy_to_result(self):
        """
        - Group the sequences, remove that has one element sequences.
        - For each series, calculate distance of all points in the sequences.
        - using anomaly/sequence ratio, get the final result sequences extracted anomalies
        :return:
        """
        self.descs = sorted(self.descs, key=key_func)
        for _, val in groupby(self.descs, key_func):
            self.sequences.append(list(val))
        for sequen in self.sequences:
            latitude = []
            longitude = []
            heading = []
            for seq in sequen:
                latitude.append(seq['latitude'])
                longitude.append(seq['longitude'])
                heading.append(seq['heading'])
            pair_lat, pair_lon, pair_head = pairwise(latitude), pairwise(longitude), pairwise(heading)
            zipped = list(zip(pair_lat, pair_lon))
            extracted, anomalies, uuud, withanomaly, orderseq = self.list_dist(zipped, sequen, pair_head)
            self.distribution.append(extracted)
            self.anomalies.append(anomalies)
            self.uud.append(uuud)
            self.withanomalies.append(withanomaly)
            self.order_seq.append(orderseq)

        return self.distribution, self.information, self.anomalies, self.uud, self.withanomalies, self.order_seq
