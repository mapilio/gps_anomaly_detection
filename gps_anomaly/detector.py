from gps_anomaly.detect_functions import mark_points


class Anomaly:
    """
    Detector anomalies launch class
    """

    @staticmethod
    def anomaly_detector(frames):
        """
        :param frames:
        :return:
        """
        result, failed_imgs, _ = mark_points(frames)

        return result, failed_imgs, _
