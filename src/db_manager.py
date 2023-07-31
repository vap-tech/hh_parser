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
    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”."""


class DBManager(BaseManager):
    """
    Работа с БД Postgres
    """

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий
        у каждой компании."""
        cur = self.conn.cursor()
        cur.execute('''SELECT employer.name, COUNT(vacancy.name) 
        FROM employer JOIN vacancy USING (employer_id)
        GROUP BY employer.name
        ORDER BY employer.name ASC''')
        return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия
        вакансии и зарплаты и ссылки на вакансию."""
        cur = self.conn.cursor()
        cur.execute('''SELECT employer.name, vacancy.name, vacancy.salary, vacancy.alternate_url 
        FROM employer JOIN vacancy USING (employer_id)
        ORDER BY employer.name ASC''')
        data = cur.fetchall()
        cur.close()
        return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        cur = self.conn.cursor()
        cur.execute('''SELECT AVG(salary)
        FROM vacancy WHERE salary <> 0''')
        data = cur.fetchall()
        cur.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем
        вакансиям."""
        cur = self.conn.cursor()
        cur.execute('''SELECT name, salary, alternate_url FROM vacancy
        WHERE salary > (SELECT AVG(salary) FROM vacancy WHERE salary <> 0)''')
        data = cur.fetchall()
        cur.close()
        return data

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные
        в метод слова, например “python”."""
        word = '%' + word + '%'
        cur = self.conn.cursor()
        cur.execute("""SELECT name, salary, alternate_url
        FROM vacancy WHERE name ILIKE %s""", (word,))
        data = cur.fetchall()
        cur.close()
        return data

    def create_table(self):
        """Выполняет первые три запроса из queries.sql, тем самым создает таблицы"""
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
        area_id = []
        employer_id = []
        for i in vacancies:

            if not i.employer.id:  # Увы, иногда Api отдаёт странные вещи...
                continue

            if i.area.id not in area_id:  # Чтобы не делать лишних запросов
                area_id.append(i.area.id)

                cur.execute('INSERT INTO area (area_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;',
                            (i.area.id, i.area.name, i.area.url))

            if i.employer.id not in employer_id:  # Чтобы не делать лишних запросов
                employer_id.append(i.employer.id)

                cur.execute('''INSERT INTO employer 
                (employer_id, name, alternate_url, vacancies_url, accredited_it_employer, trusted, url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''',
                            (i.employer.id,
                             i.employer.name,
                             i.employer.alternate_url,
                             i.employer.vacancies_url,
                             i.employer.accredited_it_employer,
                             i.employer.trusted,
                             i.employer.url))

            salary = self.calc_salary(i.salary) if i.salary else 0
            snippet = self.join_snippet(i.snippet) if i.snippet else ''

            cur.execute('''INSERT INTO vacancy 
            (vacancy_id, name, alternate_url, created_at, salary, snippet , apply_alternate_url, area_id, employer_id)
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
        cur.close()

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
    def join_snippet(snippet: 'Snippet') -> str:
        data = ''
        if snippet.requirement:
            data += snippet.requirement
        if snippet.responsibility:
            data += snippet.responsibility
        return data
