![Travis (.org)](https://img.shields.io/travis/floschne/codebook_automation)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/p0w3r/codebook_automation)
![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/p0w3r/codebook_automation)

# Codebook Automation API

This is a simple python-based REST API to facilitate using state-of-the-art NLP models in WebAnno.

## How to add models
Coming soon...

## How to run locally

_Assuming that your in the root folder of this repository_
```
pip install -r requirements.txt
DATA_BASE_PATH=/your/custom/data/path uvicorn main:app --host 0.0.0.0 --port 8081
```


## How to run with docker
```
docker-compose up -d
```
Docker image will be pulled from docker-hub if not available on the system.
To manually and locally build the image run
```
docker build -t p0w3r/codebook_automation:latest .
```

## How to run tests

_Assuming that_
 - _$PWD is root folder of this repository_
 - _config.backend.data_base_path_env_var == "DATA_BASE_PATH"_
```
PYTHONPATH=${PWD} DATA_BASE_PATH=/your/custom/data/path pytest
```
