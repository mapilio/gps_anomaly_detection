class Anomaly_index:
    """
    marker of the detected points
    that anomaly or non-anomaly
    """

    def info_anomalies(self, extracted_or_anomalies, points=bool):
        if points is True:
            for res in extracted_or_anomalies:
                res['anomaly'] = 1
        else:
            for res in extracted_or_anomalies:
                res['anomaly'] = 0
        return extracted_or_anomalies

    def update_info(self, mark, detect=bool):
        if detect is True:
            mark['anomaly'] = 1
        else:
            mark['anomaly'] = 0
        return mark
