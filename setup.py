import io
import os
import re

import setuptools


def get_long_desc():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding = "utf-8") as f:
        return f.read()

def get_requirements():
    with open("requirements.txt", encoding = "utf-8") as f:
        return f.read().splitlines()


def get_version():
    cwd = os.path.abspath(os.path.dirname(__file__))
    current_version = os.path.join(cwd, "gps_anomaly", "version.py")
    with io.open(current_version, encoding = "utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)

setuptools.setup(
    name = "gps-anomaly-detector",
    version = get_version(),
    author = "Mapilio",
    description = "Gps Anomaly Detector of Mapilio",
    long_description = get_long_desc(),
    long_description_content_type='text/markdown',
    url = "https://github.com/mapilio/gps_anomaly_detection",
    license='MIT License',
    python_requires='>=3.7',
    install_requires = get_requirements(),
)
