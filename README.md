# GPS anomaly detection

```bash
pip install gps-anomaly
``` 

### Usage
```python
from gps_anomaly.detector import Anomaly

anomaly = Anomaly()
points = [{
        "Latitude": 22.32689719997222,
        "Longitude": 11.49237269997222,
        "CaptureTime": "2021_11_18_15_22_52_000",
        "Altitude": 7.386,
        "SequenceUUID": "1490d87b-d5ba-4df3-b354-c01e7acaae29",
        "Heading": 195.9560290711052,
        "Orientation": 3,
        "DeviceMake": "GoPro Max",
        "DeviceModel": "GOPRO",
        "ImageSize": "2704x2028",
        "FoV": 100.4,
        "PhotoUUID": "21887915-e624-4246-b7e9-695b44fb6442",
        "filename": "GPAG8025.JPG",
        "path": ""
    },
    {
        "Latitude": 22.32654149997222,
        "Longitude": 11.4922393,
        "CaptureTime": "2021_11_18_15_22_53_000",
        "Altitude": 6.029,
        "SequenceUUID": "1490d87b-d5ba-4df3-b354-c01e7acaae29",
        "Orientation": 3,
        "DeviceMake": "GoPro Max",
        "DeviceModel": "GOPRO",
        "ImageSize": "2704x2028",
        "FoV": 100.4,
        "PhotoUUID": "ff612ec5-9479-473a-925b-8336af0b1e1f",
        "filename": "GPAG8026.JPG",
        "path": ""
    },
    {
        "Information": {
            "total_images": 2,
            "processed_images": 2,
            "failed_images": 0,
            "duplicated_images": 0,
            "id": "8323ff0a01fe49d1b55e610279f62828"
        }
    }
]
print(anomaly.anomaly_detector(frames=points))
```

### Output
```bash
[
    {
        "Information": {
            "total_images": 2,
            "processed_images": 2,
            "failed_images": 0,
            "duplicated_images": 0,
            "id": "8323ff0a01fe49d1b55e610279f62828"
        }
    }
]
```