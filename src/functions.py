from src.api import VacancyApi
from src.models import VacancyBase


def hh_collector(text='Python', area_id=None, count=50) -> list:
    """
    Получает заданное число вакансий HH
    :param text: Текст для запроса
    :param area_id: Массив локаций
    :param count: Количество вакансий
    :return: Массив объектов Vacancy
    """

    # Если пользователь хочет больше, чем может API, отдаём максимум 2000
    count = count if 0 < count < 2000 else 2000

    vacancies = []
    page = 0
    hh_api = VacancyApi()

    while True:
        raw = hh_api.get({'area': area_id, 'text': text, 'page': page, 'per_page': 100})
        model = VacancyBase.model_validate_json(raw)
        if count <= 100:  # Кол-во меньше "записей на страницу"
            vacancies.extend(model.items[:count])
            break
        elif count > 100:  # Кол-во больше "записей на страницу"
            vacancies.extend(model.items)
            count -= 100
            page += 1
        if model.page == model.pages:  # Если следующей страницы нет, выходим
            break

    return vacancies


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

    while count > 100: # Если хотим много вакансий
        raw = api.get({'area': area_id, 'text': text, 'page': page, 'per_page': 100})
        model = VacancyBase.model_validate_json(raw)
        vacancies.extend(model.items)
        count -= 100
        page += 1

    if count:  # Добираем остаток или если хотели меньше 100
        raw = api.get({'area': area_id, 'text': text, 'page': page, 'per_page': count})
        model = VacancyBase.model_validate_json(raw)
        vacancies.extend(model.items)

    return vacancies
