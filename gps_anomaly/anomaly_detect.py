import json
from detect_functions import Sequance,Info

def extract_result(decs):
    data_all = Sequance(decs)
    info = Info()
    extracted, information, anomaly = data_all.groupy_to_result()
    filenames_list = info.create_list_filename(anomaly)
    information = info.update_info(information, filenames_list)
    extracted = info.create_json(extracted, information)
    anomaly_points = info.create_json(anomaly, information)
    return extracted, filenames_list, anomaly_points