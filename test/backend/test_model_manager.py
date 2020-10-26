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
                  f"DummyTag{i}{i + 3}",
                  f"DummyTag{i}{i + 4}",
                  f"DummyTag{i}{i + 5}"]))
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

    # shuffle the tags
    while cb1.tags == cb2.tags:
        cb1.tags.shuffle()
    # compute new id
    cb1_id_2 = mm.compute_model_id(cb1)
    # shuffling the tags must not change the id!
    assert cb1_id_2 == cb1_id
