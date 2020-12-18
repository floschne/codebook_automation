import os
import sys

sys.path.append(str(os.getcwd()))

from test.utils import create_dummy_codebook_models


def test_codebook_model_id():
    cb1, cb2 = create_dummy_codebook_models(2)

    cb1_id = cb1.id
    cb2_id = cb2.id

    assert cb1_id is not None
    assert cb2_id is not None

    assert len(cb1_id) == len(cb2_id)
    assert cb1_id != cb2_id

    # shuffle the tags
    while cb1.tags == cb2.tags:
        cb1.tags.shuffle()
    # compute new handle
    cb1_id_2 = cb1.id
    # shuffling the tags must not change the id!
    assert cb1_id_2 == cb1_id
