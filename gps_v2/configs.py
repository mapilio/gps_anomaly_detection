import math

DOWN_RATIO = 0.5
SEQUENCE_LIMIT = 10
ALTITUDE_LOWER = 0
ALTITUDE_UPPER = 1500


class Angle:
    """
    The length of the "heading" values between two
    points gives the difference between the "heading".
    The values that remain above the parameter that,
    "header_limit" will be marked as an anomaly.
    """
    header_limit = 15

    def __init__(self):
        self.upper_angle = int
        self.lower_angle = int

    def rang(self, pair_head: list) -> int:
        self.upper_angle = int(max(pair_head[0], pair_head[1]))
        self.lower_angle = int(min(pair_head[0], pair_head[1]))
        range_angle = range(self.lower_angle, self.upper_angle)
        range_angle = [a % 360 if a >= 360 else a for a in range_angle]
        return len(range_angle)


class Distance:
    """
    the distance between two GPS points dec calculated
    using latitude and longitude information.
    the distances remaining above the "distance_limit"
    parameter will be marked as the anomaly point.
    """
    distance_limit = 50

    def __init__(self):
        self.WGS84_a = 6378137.0
        self.WGS84_b = 6356752.314245

    def ecef_from_lla(self, lat, lon, alt):
        """
        Compute ecef XYZ from latitude, longitude and altitude.

        All using the WGS94 model.
        Altitude is the distance to the WGS94 ellipsoid.
        Check results here https://www.oc.nps.edu/oc2902w/coord/llhxyz.ht
        """
        a2 = self.WGS84_a ** 2
        b2 = self.WGS84_b ** 2
        lat = math.radians(lat)
        lon = math.radians(lon)
        ll = 1.0 / math.sqrt(a2 * math.cos(lat) ** 2 + b2 * math.sin(lat) ** 2)
        x = (a2 * ll + alt) * math.cos(lat) * math.cos(lon)
        y = (a2 * ll + alt) * math.cos(lat) * math.sin(lon)
        z = (b2 * ll + alt) * math.sin(lat)
        return x, y, z

    def gps_distance(self, latlon_1, latlon_2):
        """
        :param latlon_1: 2 Latitude points
        :param latlon_2: 2 Longitude points
        :return:
        """
        x1, y1, z1 = self.ecef_from_lla(float(latlon_1[0]), float(latlon_2[0]), 0.0)
        x2, y2, z2 = self.ecef_from_lla(float(latlon_1[1]), float(latlon_2[1]), 0.0)
        dis = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        return dis


class Anomaly_index:
    """
    marker of the detected points
    that anomaly or non-anomaly
    """

    def info_anomalies(self,extracted_or_anomalies, points=bool):
        if points is True:
            for res in extracted_or_anomalies:
                res['anomaly'] = 1
        else:
            for res in extracted_or_anomalies:
                res['anomaly'] = 0
        return extracted_or_anomalies


class LimitValues:
    down_percent: float = DOWN_RATIO
    sequence_limit: int = SEQUENCE_LIMIT
    altitude_lower: int = ALTITUDE_LOWER
    altitude_upper: int = ALTITUDE_UPPER