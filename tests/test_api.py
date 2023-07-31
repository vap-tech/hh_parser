from src.api import VacancyApi, BaseApi
import pytest


def test_hh_api():
    """Test HH Api"""

    # Case #1
    hh = VacancyApi()
    data = hh.get()
    assert data is not None

    # case #2
    hh.url = 'https://v-petrenko.ru/none/'
    with pytest.raises(Exception):
        hh.get()


def test_base_api():
    class Tmp(BaseApi):
        def __init__(self):
            super().__init__()

    tmp = Tmp()
    assert tmp.url is None
    assert tmp.headers is None
