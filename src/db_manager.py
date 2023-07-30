from abc import ABC, abstractmethod
import psycopg2

from src.models import Vacancy, Snippet
from src.constants import HOST, USER, DB


class BaseManager(ABC):
    """
    Абстрактный класс, определяющий методы для работы с бд.
    """
    def __init__(self):
        db_pass = input(f'Введите пароль пользователя {USER}: ')
        self.conn = psycopg2.connect(f'dbname={DB} user={USER} password={db_pass} host={HOST}')
        self.conn.autocommit = True

    def __del__(self):
        if not self.conn.closed:
            self.conn.close()

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

    def create_table(self):
        """Выполняет первые три запроса из queries.sql"""
        cur = self.conn.cursor()
        with open('queries.sql') as file:
            for i in range(3):
                query = ''
                while ';' not in query:
                    query += file.readline()
                query = query.replace('\n', ' ')
                cur.execute(query)
        cur.close()

    def vacancy_to_db(self, vacancies: list[Vacancy]):
        """Загружает вакансии в базу"""
        cur = self.conn.cursor()
        for i in vacancies:

            if not i.employer.id:  # Увы, иногда Api отдаёт странные вещи..
                continue

            cur.execute('INSERT INTO area (id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;',
                        (i.area.id, i.area.name, i.area.url))


            cur.execute('''INSERT INTO employer 
            (id, name, alternate_url, vacancies_url, accredited_it_employer, trusted, url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''',
                        (i.employer.id,
                         i.employer.name,
                         i.employer.alternate_url,
                         i.employer.vacancies_url,
                         i.employer.accredited_it_employer,
                         i.employer.trusted,
                         i.employer.url))

            salary = self.calc_salary(i.salary) if i.salary else 0
            snippet = self.summ_snippet(i.snippet) if i.snippet else ''

            cur.execute('''INSERT INTO vacancy 
            (id, name, alternate_url, created_at, salary, snippet , apply_alternate_url, area_id, employer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''',
                        (i.id,
                         i.name,
                         i.alternate_url,
                         i.created_at,
                         salary,
                         snippet,
                         i.apply_alternate_url,
                         i.area.id,
                         i.employer.id))

    @staticmethod
    def calc_salary(salary: dict) -> int:
        sal_sum = 0
        count = 0
        if salary['from']:
            sal_sum += salary['from']
            count += 1
        if salary['to']:
            sal_sum += salary['to']
            count += 1
        return int(sal_sum / count)

    @staticmethod
    def summ_snippet(snippet: 'Snippet') -> str:
        data = ''
        if snippet.requirement:
            data += snippet.requirement
        if snippet.responsibility:
            data += snippet.responsibility
        return data
