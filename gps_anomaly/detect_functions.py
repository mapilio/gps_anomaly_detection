from .one_sequence import Sequence
import os
import re
from gps_anomaly.config.distance import Distance


def first_point(anomaly_points, extracted_seq, seq):
    """
    First points of sequences has marked as anomaly or
    not anomaly, with comparing second point.
    """
    if len(extracted_seq) > 1 and seq[1] in extracted_seq:
        extracted_seq.append(seq[0])
    else:
        anomaly_points.append(seq[0])
    return extracted_seq, anomaly_points


class Info:
    """
    Notices failure sequence UUID,
    anomaly points' image names.
    """

    def create_list_filename(self, distrubution):
        """
        appends result to one list
        :param distrubution:
        :return:
        """
        file_list = []
        for sequences in distrubution:
            for seq in sequences:
                if type(seq) == dict:
                    file_list.append(os.path.join(seq['filename']))
        return file_list

    def check_distance_from_desc(self, desc):
        """
        Checks the distance between images, marks as failed or duplicate.
        """
        if 'anomaly_reason' in desc:
            reason = desc['anomaly_reason']
            match = re.search(r'The distance:\s*([-+]?[0-9]*\.?[0-9]+)', reason)
            if match:
                distance = float(match.group(1))
                if distance < Distance.distance_low_limit:
                    return "duplicate"
                else:
                    return "failed"

        return None

    def update_info(self, descs, info, uud):
        for desc in descs:
            if self.check_distance_from_desc(desc) == "duplicate":
                info["Information"]["duplicated_images"] += 1
                info["Information"]["processed_images"] -= 1
            elif self.check_distance_from_desc(desc) == "failed":
                info["Information"]["failed_images"] += 1
                info["Information"]["processed_images"] -= 1
        uud = [lis for lis in uud if lis != []]
        info['Information']['anomaly_sequences'] = uud
        return info

    def create_json(self, distrubution, info):
        """
        appends result to one list
        :param info:
        :param distrubution:
        :return:
        """
        united_sequences = []
        for sequences in distrubution:
            for seq in sequences:
                if type(seq) == dict:
                    united_sequences.append(seq)
        united_sequences.append(info)
        return united_sequences


def mark_points(desc):
    """
        - Group the sequences, remove that has one element sequences.
        - For each series, calculate distance of all points in the sequence.
        - using length anomaly/sequence ratio, get the final result sequences extracted anomalies
    """
    data_all = Sequence(desc)
    info = Info()
    extracted, information, anomaly, uud, with_anomaly, order_seq = data_all.groupy_to_result()
    filenames_list = info.create_list_filename(anomaly)
    information = info.update_info(desc, information, uud)
    order_seq = info.create_json(order_seq, information)
    anomaly_points = info.create_json(anomaly, information)
    return order_seq, filenames_list, anomaly_points
