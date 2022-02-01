from processes_per_sequance import *
import json
from itertools import groupby
from configs import *

def key_func(k):
    return k['SequenceUUID']


class AllSequence:

    def __init__(self, descs):
        self.information = list(descs).pop()
        descs = list(descs)[:-1]
        self.descs = [desc for desc in descs if ("error" not in desc) and ("Heading" in desc)]
        self.sequences = []
        self.information['Information']['anomaly_sequences'] = []


    def all_to_one_list(self, distrubution):
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
        return united_sequences

    def create_json(self):
        results = []
        for _, val in groupby(self.descs, key_func):
            self.sequences.append(list(val))
        limits= LimitValues()
        for sequence in self.sequences:
            process = ProcessSeq(sequence)
            if len(sequence) > limits.sequence_limit:
                result, failure_sequence = process.add_column()
                if failure_sequence == True:
                    self.information['Information']['anomaly_sequences'].append(sequence[0]['SequenceUUID'])
            else:
                result = process.lower_sequence()
                self.information['Information']['anomaly_sequences'].append(sequence[0]['SequenceUUID'])
            results.append(result)
        results = self.all_to_one_list(results)
        results.append(self.information)
        return results


with open('/home/izzet/Downloads/3_1_2022_pendik.json') as fp:
    descs = json.load(fp)

all = AllSequence(descs)
final = all.create_json()

with open("/home/izzet/Desktop/projects/plot-anomaly-mapilio/gpsv2.json", "w") as outfile:
    outfile.write(json.dumps(final, indent=4))