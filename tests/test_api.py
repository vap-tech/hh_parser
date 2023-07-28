from src.api import HHApi, BaseApi
import pytest


def test_hh_api():
    """Test HH Api"""

    # Case #1
    hh = HHApi()
    data = hh.get_vacancies()
    assert data is not None

    # case #2
    hh.url = 'https://v-petrenko.ru/none/'
    with pytest.raises(Exception):
        hh.get_vacancies()


def test_base_api():
    class Tmp(BaseApi):
        def __init__(self):
            super().__init__()

    tmp = Tmp()
    assert tmp.url is None
    assert tmp.headers is None
