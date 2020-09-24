# Codebook Automation API

This is a simple python-based REST API to facilitate using state-of-the-art NLP models in CodeAnno.

## How to run locally

```
pip install -r requirements.txt

uvicorn api.controller:api --reload
```


## How to run with docker

```
CBA_API_PORT=8081 docker-compose up -d
```