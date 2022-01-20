from typing import Tuple, Optional, Any

from gps_anomaly.anomaly_detect import extract_result


class Anomaly:
    """
    Detector anomalies launch class
    """

    @staticmethod
    def anomaly_detector(frames: list) -> Tuple[Optional[Any], Optional[Any], Optional[Any]]:
        """
        :param frames:
        :return:
        """
        removed_anomaly_frames, failed_imgs, anomaly_points = None, None, None
        try:
            removed_anomaly_frames, failed_imgs, anomaly_points = extract_result(frames)
        except Exception as e:

            print("exc_type : ", type(e).__name__)
            print("exc_message :", str(e))

        return removed_anomaly_frames, failed_imgs, anomaly_points

