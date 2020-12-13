import os
import sys

import pytest
from starlette import status

from backend import ModelManager

sys.path.append(str(os.getcwd()))
from fastapi.testclient import TestClient

from main import app
from api.model import BooleanResponse, CodebookModel, ModelConfig, TrainingRequest


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def cb() -> CodebookModel:
    return CodebookModel(name="ProductTypeTest1", tags=["pet_supplies",
                                                        "health_personal_care",
                                                        "grocery_gourmet_food",
                                                        "toys_games",
                                                        "beauty",
                                                        "baby_products"
                                                        ])


@pytest.fixture
def model_conf() -> ModelConfig:
    return ModelConfig(embedding_type="https://tfhub.dev/google/universal-sentence-encoder/2",
                       hidden_units=[32, 64, 16],
                       dropout=.2,
                       optimizer="Adam",
                       early_stopping=False,
                       activation_fn="relu")


@pytest.fixture
def dsv() -> str:
    return "TestingDS1"


@pytest.fixture
def mv() -> str:
    return "TestingModel1"


@pytest.fixture
def train_req(cb: CodebookModel, model_conf: ModelConfig, mv: str, dsv: str) -> TrainingRequest:
    return TrainingRequest(cb=cb,
                           model_config=model_conf,
                           model_version=mv,
                           dataset_version=dsv,
                           batch_size_train=32,
                           batch_size_test=32,
                           max_steps_train=100,
                           max_steps_test=100)


@pytest.mark.run(order=1)
def test_dataset_upload(cb: CodebookModel, dsv: str, client: TestClient):
    # TODO redundant code

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
def test_train(train_req: TrainingRequest, client: TestClient):
    # TODO how to test the background task? -> unit test could test core functionality but not API
    response = client.post('/training/train/', json=train_req.dict())

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"model_id": ModelManager.get_model_id(train_req.cb,
                                                                     train_req.model_version,
                                                                     train_req.dataset_version)}
