from gps_anomaly.detect_functions import mark_points


class Anomaly:
    """
    Detector anomalies launch class
    """

    @staticmethod
    def anomaly_detector(frames: list) -> list:
        """
        :param frames:
        :return:
        """
        removed_anomaly_frames = None
        anomaly_points = None
        try:
            removed_anomaly_frames, failed_imgs, anomaly_points = mark_points(frames)
        except Exception as e:

            print("exc_type : ", type(e).__name__)
            print("exc_message :", str(e))

        return removed_anomaly_frames, failed_imgs, anomaly_points
