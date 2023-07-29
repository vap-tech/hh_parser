from pydantic import BaseModel, HttpUrl
from typing import Optional
import bleach

from src.vacancy import Vacancy


class Area(BaseModel):
    """Модель местности с hh"""
    id: int  # id местности
    name: str  # Название
    url: str  # ссылка на данную местность


class EmployerBaseModel(BaseModel):  # Этот класс наверно должен быть абстрактным???
    """Модель данных работодатель"""
    id: str  # Идентификатор работодателя
    name: str  # Название работодателя
    alternate_url: str  # Ссылка на описание работодателя на сайте hh
    vacancies_url: str  # URL для получения поисковой выдачи с вакансиями данного работодателя
    accredited_it_employer: bool  # Флаг, показывающий, прошел ли работодатель IT аккредитацию
    trusted: bool  # Флаг, показывающий, прошел ли работодатель проверку на сайте


class EmployerVacancyModel(EmployerBaseModel):
    """Модель данных работодатель в вакансии"""
    url: str  # Адрес для подробного запроса


class EmployerFullModel(EmployerBaseModel):
    """Модель для подробного запроса по работодателю"""
    type: str  # Тип работодателя (прямой работодатель, кадровое агентство или null, если тип работодателя скрыт)
    description: str  # Описание работодателя в виде строки с кодом HTML
    site_url: str  # Адрес сайта работодателя
    area: Area  # Информация о регионе работодателя
    industries: list  # Список отраслей работодателя. Элементы справочника индустрий hh
    open_vacancies: int  # Количество открытых вакансий у работодателя


class HHVacancyModel(BaseModel):
    """Модель данных Вакансия"""
    id: int  # id вакансии
    name: str  # Название
    alternate_url: Optional[HttpUrl] = None  # URL вакансии
    area: dict  # Место расположения
    created_at: str  # Дата и время публикации вакансии
    salary: Optional[dict] = None  # Зарплата
    snippet: Optional[dict] = None  # Фрагмент описания
    employer: Optional[dict]  # Работодатель

    def to_vacancy(self):
        """
        :return: Объект класса Vacancy
        """
        # Ищем непустую зарплату
        pay = 0
        if self.salary:
            if self.salary['from']:
                pay = self.salary['from']
            elif self.salary['to']:
                pay = self.salary['to']

        des = "".join([i for i in self.snippet.values() if i])
        des = bleach.clean(des,  tags=[], strip=True)
        url_ = self.alternate_url if self.alternate_url else "Нет Url'а"
        emp_id = self.employer['id']

        return Vacancy(self.id, self.name, url_, self.area['name'], pay, des, emp_id)


class HHVacancyBaseModel(BaseModel):
    """Базовая модель данных ответа от HH на запрос вакансий"""
    items: list[HHVacancyModel]  # Список сокращенных представлений резюме
    found: int  # Найдено результатов
    page: int  # Номер страницы
    pages: int  # Всего страниц
    per_page: int  # Результатов на странице
    hidden_on_page: Optional[int] = None  # Количество удаленных или скрытых соискателями резюме на странице

    def get_vacancy(self):
        """
        :return: Список из объектов Vacancy
        """
        return [vac.to_vacancy() for vac in self.items]


