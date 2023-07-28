from functools import total_ordering


@total_ordering  # Декоратор, генерирует недостающие методы сравнения
class Vacancy:
    """Общий класс для вакансий"""
    def __init__(
            self,
            id_: int,
            name: str,
            url,
            area: str,
            salary: int,
            descr: str
    ):
        """
        :param id_: Ид
        :param name: Имя
        :param url: Ссылка
        :param area: Местоположение вакансии
        :param salary: Зарплата
        :param descr: Краткое описание или фрагмент
        """
        self.id = id_
        self.name = name
        self.url = url
        self.area = area
        self.salary = salary
        self.descr = descr

    def __str__(self) -> str:
        return f'{self.name}, {self.salary} руб. {self.url}'

    def __lt__(self, other):
        return self.salary < other.salary

    def __eq__(self, other):
        return self.salary == other.salary

    @property
    def all_to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url': str(self.url),
            'area': self.area,
            'salary': self.salary,
            'descr': self.descr
        }

    @property
    def all_for_print(self) -> str:
        data = [
            f'\nid вакансии: {self.id}',
            f'\nНазвание вакансии: {self.name}',
            f'\nСсылка: {str(self.url)}',
            f'\nМестоположение: {self.area}',
            f'\nЗаработная плата от: {self.salary}',
            f'\nОписание: {self.descr}'
        ]
        return "".join(data)
