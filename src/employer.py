class Employer:
    """Общий класс для работодателя"""
    def __init__(
            self,
            id_: int,
            name: str,
            url,
            area: str,
            salary: int,
            descr: str,
            employer_id: str
    ):
        """
        :param id_: Ид
        :param name: Имя
        :param url: Ссылка
        :param area: Местоположение вакансии
        :param salary: Зарплата
        :param descr: Краткое описание или фрагмент
        :param employer_id: id работодателя
        """
        self.id = id_
        self.name = name
        self.url = url
        self.area = area
        self.salary = salary
        self.descr = descr
        self.employer_id = employer_id

    def __str__(self) -> str:
        return f'{self.name}, {self.salary} руб. {self.url}'

    @property
    def all_to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url': str(self.url),
            'area': self.area,
            'salary': self.salary,
            'descr': self.descr,
            'employer': self.employer_id
        }

    @property
    def all_for_print(self) -> str:
        data = [
            f'\nid вакансии: {self.id}',
            f'\nНазвание вакансии: {self.name}',
            f'\nСсылка: {str(self.url)}',
            f'\nМестоположение: {self.area}',
            f'\nЗаработная плата от: {self.salary}',
            f'\nОписание: {self.descr}',
            f'\nid работодателя: {self.employer_id}'
        ]
        return "".join(data)