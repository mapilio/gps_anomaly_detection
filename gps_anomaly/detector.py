from anomaly_detect import extract_result


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
        try:
            removed_anomaly_frames = extract_result(frames)
        except Exception as e:

            print("exc_type : ", type(e).__name__)
            print("exc_message :", str(e))

        return removed_anomaly_frames