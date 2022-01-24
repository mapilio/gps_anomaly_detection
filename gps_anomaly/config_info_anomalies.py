class Anomaly_index:

    def info_anomalies(self,extracted_or_anomalies, points=bool):
        if points is True:
            for res in extracted_or_anomalies:
                res['anomalies'] = 1
        else:
            for res in extracted_or_anomalies:
                res['anomalies'] = 0
        return extracted_or_anomalies