import os
import sys

import pytest
from starlette import status

sys.path.append(str(os.getcwd()))
from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse, CodebookDTO, DatasetRequest


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def cb() -> CodebookDTO:
    return CodebookDTO(name="ProductTypeTest1", tags=["pet_supplies",
                                                        "health_personal_care",
                                                        "grocery_gourmet_food",
                                                        "toys_games",
                                                        "beauty",
                                                        "baby_products"
                                                      ])


@pytest.fixture
def dsv() -> str:
    return "TestingDS1"


@pytest.fixture
def ds_req(cb: CodebookDTO, dsv: str) -> DatasetRequest:
    return DatasetRequest(cb=cb, dataset_version=dsv)


@pytest.mark.run(order=1)
def test_dataset_upload(cb: CodebookDTO, dsv: str, client: TestClient):
    with open(os.getcwd() + '/test/resources/product_type_ds.zip', "rb") as f:
        archive = f.read()
        response = client.put('/dataset/upload/',
                              data={"codebook_name": cb.name,
                                    "codebook_tag_list": ",".join(cb.tags),
                                    "dataset_version": dsv},
                              files={"dataset_archive": ("product_type_ds.zip", archive)})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=2)
def test_dataset_is_available(ds_req: DatasetRequest, client: TestClient):
    response = client.post("/dataset/available/", json=ds_req.dict())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=3)
def test_dataset_remove(ds_req: DatasetRequest, client: TestClient):
    response = client.delete("/dataset/remove/", json=ds_req.dict())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=True)


@pytest.mark.run(order=4)
def test_dataset_is_not_available(ds_req: DatasetRequest, client: TestClient):
    response = client.post("/dataset/available/", json=ds_req.dict())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BooleanResponse(value=False)
