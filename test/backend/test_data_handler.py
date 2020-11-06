import pytest

from api.model import CodebookModel
from backend.data_handler import DataHandler


@pytest.fixture
def dh():
    return DataHandler()


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


def test_get_data_handle(dh: DataHandler):
    cb1, cb2 = create_dummy_codebook_models(2)

    cb1_id = dh.get_data_handle(cb1)
    cb2_id = dh.get_data_handle(cb2)

    assert len(cb1_id) == len(cb2_id)
    assert cb1_id != cb2_id
    assert cb1_id == dh.get_data_handle(cb1)

    # shuffle the tags
    while cb1.tags == cb2.tags:
        cb1.tags.shuffle()
    # compute new handle
    cb1_id_2 = dh.get_data_handle(cb1)
    # shuffling the tags must not change the id!
    assert cb1_id_2 == cb1_id
