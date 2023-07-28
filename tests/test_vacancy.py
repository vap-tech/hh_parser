from src.vacancy import Vacancy


def test_vacancy():
    vac = Vacancy(13, 'Python Dev', 'https://yrl.ru', 'Voronezh', 130000, 'Description')
    assert vac.id == 13
    assert vac.salary == 130000
    assert vac.__str__() == 'Python Dev, 130000 руб. https://yrl.ru'
    assert vac.all_for_print is not None
    assert vac.all_to_dict is not None

    # Case 2
    vac2 = Vacancy(14, 'Java Dev', 'https://yrl3.ru', 'Sochi', 120000, 'Not descr')
    assert vac > vac2
    assert not vac < vac2
    assert not vac == vac2
