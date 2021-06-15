
import pytest
import constants

import data
import os


DIR = constants.DIR

@pytest.fixture()
def data_path():
    return DIR

def test_b(data_path):
    print(DIR)
    assert data_path == DIR


def test_load_data_count():
    """
    test the data loaded whether with right number
    """
    aos, dos = data.load_data("R", data_dir = DIR)
    print(len(aos), len(dos))
    print(os.getcwd())
    assert len(aos) == 50
    assert len(dos) == 50