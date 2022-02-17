import urllib.request
import json
from gps_anomaly.detector import Anomaly

res = urllib.request.urlopen(
    'https://raw.githubusercontent.com/mapilio/mapilio-kit/master/schema/image_description_schema.json')
res_body = res.read()

# https://docs.python.org/3/library/json.html
json_file = json.loads(res_body.decode("utf-8"))

inforrmation = {"Information":
    {
        "total_images": 7,
        "processed_images": 7,
        "failed_images": 0,
        "duplicated_images": 0,
    }
}

json_file.append(inforrmation)
anomaly = Anomaly()
result, failure_images, _ = anomaly.anomaly_detector(frames=json_file)

with open(file="image_description_schema_export.json", mode="w") as f:
    json.dump(result, f, indent=4)
