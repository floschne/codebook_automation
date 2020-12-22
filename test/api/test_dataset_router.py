import os
import sys

import pytest
from starlette import status

sys.path.append(str(os.getcwd()))
from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse, DatasetMetadata


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def cb_name() -> str:
    return "ProductTypeTest1"


@pytest.fixture
def dsv() -> str:
    return "TestingDS1"


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


@pytest.mark.run(order=3)
def test_dataset_metadata_is_available(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/metadata/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(DatasetMetadata.parse_obj(response.json()), DatasetMetadata)


@pytest.mark.run(order=4)
def test_dataset_list(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/list/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    dataset_list = [DatasetMetadata.parse_obj(item) for item in response.json()]
    assert len(dataset_list) == 1
    assert isinstance(dataset_list[0], DatasetMetadata)


@pytest.mark.run(order=5)
def test_dataset_remove(cb_name: str, dsv: str, client: TestClient):
    response = client.delete("/dataset/remove/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=6)
def test_dataset_is_not_available(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/available/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=False)


@pytest.mark.run(order=7)
def test_dataset_list_empty(cb_name: str, dsv: str, client: TestClient):
    response = client.get("/dataset/list/", params={"cb_name": cb_name, "dataset_version": dsv})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
