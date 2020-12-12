import os
import sys

sys.path.append(str(os.getcwd()))

import pytest

from test.utils import create_dummy_codebook_models
from backend.data_handler import DataHandler
from backend.exceptions import NoDataForCodebookException


@pytest.fixture
def dh():
    return DataHandler()


def test_get_and_purge_data_directory(dh: DataHandler):
    cb1, cb2 = create_dummy_codebook_models(2)

    # raise exception of the data dirs don't exist
    with pytest.raises(NoDataForCodebookException):
        dh._get_data_directory(cb1, create=False)
        dh._get_data_directory(cb2, create=False)

    # create the dirs
    cb1_dir = dh._get_data_directory(cb1, create=True)
    cb2_dir = dh._get_data_directory(cb2, create=True)
    assert cb1_dir != cb2_dir
    assert cb1_dir.exists()
    assert cb2_dir.exists()

    # remove the dirs again
    dh._purge_data(cb1)
    dh._purge_data(cb2)
    assert not cb1_dir.exists()
    assert not cb2_dir.exists()
