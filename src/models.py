from pydantic import BaseModel
from typing import Optional


class Area(BaseModel):
    """Модель местности с hh"""
    id: int  # id местности
    name: str  # Название
    url: str  # ссылка на данную местность


class EmployerBase(BaseModel):  # Этот класс наверно должен быть абстрактным???
    """Модель данных работодатель"""
    id: str  # Идентификатор работодателя
    name: str  # Название работодателя
    alternate_url: str  # Ссылка на описание работодателя на сайте hh
    vacancies_url: str  # URL для получения поисковой выдачи с вакансиями данного работодателя
    accredited_it_employer: bool  # Флаг, показывающий, прошел ли работодатель IT аккредитацию
    trusted: bool  # Флаг, показывающий, прошел ли работодатель проверку на сайте


class EmployerInVacancy(EmployerBase):
    """Модель данных работодатель в вакансии"""
    url: str  # Адрес для подробного запроса


class EmployerFull(EmployerBase):
    """Модель для подробного запроса по работодателю"""
    type: str  # Тип работодателя (прямой работодатель, кадровое агентство или null, если тип работодателя скрыт)
    description: str  # Описание работодателя в виде строки с кодом HTML
    site_url: str  # Адрес сайта работодателя
    area: Area  # Информация о регионе работодателя
    industries: list  # Список отраслей работодателя. Элементы справочника индустрий hh
    open_vacancies: int  # Количество открытых вакансий у работодателя


class Vacancy(BaseModel):
    """Модель данных Вакансия"""
    id: int  # id вакансии
    name: str  # Название
    alternate_url: Optional[str] = None  # URL вакансии
    area: Area  # Место расположения
    created_at: str  # Дата и время публикации вакансии
    salary: Optional[dict] = None  # Зарплата
    snippet: Optional[dict] = None  # Фрагмент описания
    employer: Optional[EmployerInVacancy]  # Работодатель
    apply_alternate_url: str  # Ссылка для отклика


class VacancyBase(BaseModel):
    """Базовая модель данных ответа от HH на запрос вакансий"""
    items: list[Vacancy]  # Список сокращенных представлений резюме
    found: int  # Найдено результатов
    page: int  # Номер страницы
    pages: int  # Всего страниц
    per_page: int  # Результатов на странице
    hidden_on_page: Optional[int] = None  # Количество удаленных или скрытых соискателями резюме на странице
