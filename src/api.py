import requests
from abc import ABC, abstractmethod


class BaseApi(ABC):
    """
    Базовый класс для классов API
    """
    @abstractmethod
    def __init__(self):
        """
        Параметры self.url: str
        self.headers: dict подлежат обязательному
        определению в потомках.
        """
        self.url = None
        self.headers = None

    def get(self, params_to_search: dict = None) -> str:
        """
        Делает get запрос, бросает исключение если код ответа не 200
        :param params_to_search:
            Параметры запроса для поиска вакансий
        :return:
            Строка данных из ответа api если код ответа 200
        """
        r = requests.get(self.url, headers=self.headers, params=params_to_search)
        if r.status_code == requests.codes.ok:
            data = r.content.decode()
            r.close()
            return data
        r.raise_for_status()


class VacancyApi(BaseApi):
    """Класс получения вакансий средствами api hh.ru"""
    def __init__(self):
        """Адрес api и заголовки для запросов вакансий с hh"""

        self.headers = {
            'User-Agent': 'api-test-agent'
        }

        self.url = 'https://api.hh.ru/vacancies/'


class EmployerApi(BaseApi):
    """Класс получения данных о работодателе"""
    def __init__(self):
        """Адрес api и заголовки для запросов данных о работодателе с hh"""

        self.headers = {
            'User-Agent': 'api-test-agent'
        }

        self.url = 'https://api.hh.ru/employers/'
        self.__employer_id = None

    @property
    def employer_id(self):
        return self.__employer_id

    @employer_id.setter
    def employer_id(self, new: str):
        self.url = 'https://api.hh.ru/employers/' + new + '/'
        self.__employer_id = new
