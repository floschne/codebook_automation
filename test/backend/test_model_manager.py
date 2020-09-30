import os

import pytest

from api.model import CodebookModel
from backend.model_manager import ModelManager


@pytest.fixture
def mm():
    return ModelManager()


def create_dummy_codebook_models(num: int):
    dummies = list()
    for i in range(num):
        dummies.append(CodebookModel(
            name=f"DummyCodebookModel{i}",
            tags=[f"DummyTag{i}{i + 1}",
                  f"DummyTag{i}{i + 2}",
                  f"DummyTag{i}{i + 3}"]))
    if num == 1:
        return dummies[0]
    return dummies


def test_compute_model_id(mm: ModelManager):
    cb1, cb2 = create_dummy_codebook_models(2)
    cb1_id = mm.compute_model_id(cb1)
    cb2_id = mm.compute_model_id(cb2)
    assert len(cb1_id) == len(cb2_id)
    assert cb1_id != cb2_id
    assert cb1_id == mm.compute_model_id(cb1)


def test_model_is_available(mm: ModelManager):
    cb1 = create_dummy_codebook_models(1)
    assert not mm.model_is_available(cb1)

    # create the model directory!
    m_path = mm._create_model_directory(cb1)
    assert mm.model_is_available(cb1)

    # delete it again
    os.rmdir(m_path)
    assert not mm.model_is_available(cb1)
