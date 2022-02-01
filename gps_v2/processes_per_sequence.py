from configs import *
import itertools


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))




class ProcessSeq:

    def __init__(self, sequence):
        self.lats, self.longs, self.heads, self.alts = [], [], [], []
        self.sequence = sequence

    def create_parameters(self):
        self.lats = [a_dict['Latitude'] for a_dict in self.sequence]
        self.longs = [a_dict['Longitude'] for a_dict in self.sequence]
        self.heads = [a_dict['Heading'] for a_dict in self.sequence]
        self.alts = [a_dict['Altitude'] for a_dict in self.sequence]
        self.pair_lat, self.pair_lon, self.pair_head, self.pair_altitude = list(pairwise(self.lats)), \
                                                list(pairwise(self.longs)), list(pairwise(self.heads)),list(pairwise(self.alts))
        self.pair_latlon = list(zip(self.pair_lat, self.pair_lon))


    def add_column(self):
        self.create_parameters()
        distance = Distance()
        angle = Angle()
        limits = LimitValues()
        non_anomaly_points = []
        anomaly_points = []
        filenames = []
        failure_sequence = False
        for i in range(len(self.pair_latlon)):
            cond_distance = distance.gps_distance(self.pair_latlon[i][0], self.pair_latlon[i][1]) < distance.distance_limit
            cond_angle = angle.rang(self.pair_head[i]) < angle.header_limit
            cond_altitude = limits.altitude_upper > self.alts[i] > limits.altitude_lower
            conditions = [cond_distance, cond_angle, cond_altitude]
            if all(conditions) == True:
                non_anomaly_points.append(self.sequence[i+1])
                self.sequence[i + 1]['anomaly'] = 0
            else:
                anomaly_points.append(self.sequence[i+1])
                self.sequence[i + 1]['anomaly'] = 1
                filenames.append(self.sequence[i + 1]['filename'])
        ratio = len(non_anomaly_points) / len(self.sequence)
        if ratio < limits.down_percent:
            self.sequence = [dict(item, anomaly=1) for item in self.sequence]
            failure_sequence = True
        self.sequence[0]['anomaly'] = self.sequence[1]['anomaly']
        return self.sequence, failure_sequence

    def lower_sequence(self):
        for i in range(len(self.sequence)):
            self.sequence[i]['anomaly'] = 1
        return self.sequence