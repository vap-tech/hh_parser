from abc import ABC, abstractmethod
import psycopg2


class BaseManager(ABC):
    """
    Абстрактный класс, определяющий методы для работы с бд.
    """
    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий
        у каждой компании."""
    @abstractmethod
    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия
        вакансии и зарплаты и ссылки на вакансию."""
    @abstractmethod
    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем
        вакансиям."""
    @abstractmethod
    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”."""


class DBManager(BaseManager):
    """
    Класс, который подключается к БД Postgres
    """

    def __init__(self):
        self.conn = psycopg2.connect("dbname=test user=postgres")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий
        у каждой компании."""

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия
        вакансии и зарплаты и ссылки на вакансию."""

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем
        вакансиям."""

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”."""
