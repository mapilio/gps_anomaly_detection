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
        removed_anomaly_frames, failed_imgs, anomaly_points = mark_points(frames)

        return removed_anomaly_frames, failed_imgs, anomaly_points
