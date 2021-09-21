import os
import sys
import time

import pytest
from starlette import status

from backend import ModelManager

sys.path.append(str(os.getcwd()))
from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse, DatasetMetadata, TrainingRequest, ModelConfig, TrainingResponse, TrainingStatus, \
    TrainingState


def pytest_configure():
    pytest.train_resp = TrainingResponse(model_id="None")


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def cb_name() -> str:
    return "ProductTypeTraining"


@pytest.fixture(scope="module")
def dsv() -> str:
    return "ProductTypeTrainingDataset"


@pytest.fixture(scope="module")
def mv() -> str:
    return "ProductTypeTrainingModel"


@pytest.fixture(scope="module")
def mconf() -> ModelConfig:
    return ModelConfig()


@pytest.fixture(scope="module")
def train_req(cb_name: str, dsv: str, mv: str, mconf: ModelConfig) -> TrainingRequest:
    return TrainingRequest(cb_name=cb_name, model_version=mv, dataset_version=dsv, model_config=mconf)


@pytest.mark.run(order=1)
def test_dataset_upload(cb_name: str, dsv: str, client: TestClient):
    with open(os.getcwd() + '/test/resources/product_type_ds.zip', "rb") as f:
        archive = f.read()
        response = client.put('/dataset/upload/',
                              data={"cb_name": cb_name,
                                    "dataset_version": dsv},
                              files={"dataset_archive": ("product_type_ds.zip", archive)})

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(DatasetMetadata.parse_obj(response.json()), DatasetMetadata)


@pytest.mark.run(order=2)
def test_dataset_is_available(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/available/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=4)
def test_start_training(train_req: TrainingRequest, client: TestClient):
    response = client.post("/training/train/", json=train_req.dict(), headers={"Content Type": "application/json"})
    assert response.status_code == status.HTTP_200_OK
    resp = TrainingResponse.parse_obj(response.json())
    assert isinstance(resp, TrainingResponse)
    pytest.train_resp = resp


@pytest.mark.run(order=5)
def test_training_status_running(client: TestClient):
    train_resp = pytest.train_resp
    response = client.post("/training/status/", json=train_resp.dict())
    assert response.status_code == status.HTTP_200_OK
    stat = TrainingStatus.parse_obj(response.json())
    assert stat.state == TrainingState.preparing or stat.state == TrainingState.training


@pytest.mark.run(order=6)
def test_wait_for_training_finish(client: TestClient):
    train_resp = pytest.train_resp
    response = client.post("/training/status/", json=train_resp.dict())
    assert response.status_code == status.HTTP_200_OK
    stat = TrainingStatus.parse_obj(response.json())
    max_seconds = 120
    start = time.time()
    while stat.state != TrainingState.finished:
        response = client.post("/training/status/", json=train_resp.dict())
        assert response.status_code == status.HTTP_200_OK
        stat = TrainingStatus.parse_obj(response.json())
        assert stat.state != TrainingState.error and stat.state != TrainingState.unknown, "Training was erroneous!"
        assert time.time() - start <= max_seconds, "Training took too long!"
        time.sleep(1)

    assert stat.state == TrainingState.finished and stat.process_status != "error"


@pytest.mark.run(order=7)
def test_remove_model(cb_name: str, mv: str):
    # only remove if the model exists i.e. if the training was successful
    if ModelManager().is_available(cb_name=cb_name, model_version=mv, complete_check=True):
        assert ModelManager().remove(cb_name=cb_name, model_version=mv)
        assert not ModelManager().is_available(cb_name=cb_name, model_version=mv, complete_check=True)


@pytest.mark.run(order=8)
def test_dataset_remove(cb_name: str, dsv: str, client: TestClient):
    response = client.delete("/dataset/remove/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=9)
def test_dataset_is_not_available(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/available/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=False)
