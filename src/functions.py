from src.api import VacancyApi
from src.models import VacancyBase


def vacancy_collector(api: 'VacancyApi', text='Python', area_id=None, count=20) -> list:
    """
        Получает заданное число вакансий HH
        :param api: объект класса api hh
        :param text: Текст для запроса
        :param area_id: Массив локаций
        :param count: Количество вакансий
        :return: Массив объектов Vacancy
        """

    vacancies = []
    page = 0
    not_end = True

    while count > 100:  # Если хотим много вакансий
        raw = api.get({'area': area_id, 'text': text, 'page': page, 'per_page': 100})
        model = VacancyBase.model_validate_json(raw)
        vacancies.extend(model.items)
        count -= 100
        page += 1
        if model.page == model.pages:
            not_end = False
            break

    if count and not_end:  # Добираем остаток или если хотели меньше 100
        raw = api.get({'area': area_id, 'text': text, 'page': page, 'per_page': count})
        model = VacancyBase.model_validate_json(raw)
        vacancies.extend(model.items)

    return vacancies
