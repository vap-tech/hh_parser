from src.functions import vacancy_collector
from src.api import VacancyApi, EmployerApi
from src.models import EmployerFull
from src.db_manager import DBManager


def api():
    hh = VacancyApi()
    data = vacancy_collector(hh, text='Python', area_id=1, count=1570)

    return data


def api2():
    hh = EmployerApi()
    hh.employer_id = '4768936'

    data = hh.get()

    data2 = EmployerFull.model_validate_json(data)
    for i in data2:
        print(i)


dat = api()
man = DBManager()
man.create_table()
input()
man.vacancy_to_db(dat)
