from src.api import HHVacancyApi
from src.parser import HHVacancyBaseModel


def hh_collector(text='Python', area=None, count=50) -> list:
    """
    Получает заданное число вакансий HH
    :param text: Текст для запроса
    :param area: Массив локаций
    :param count: Количество вакансий
    :return: Массив объектов Vacancy
    """

    # Если пользователь хочет больше, чем может API, отдаём максимум 2000
    count = count if 0 < count < 2000 else 2000

    area = area[0] if area else None
    vacancies = []
    page = 0
    hh_api = HHVacancyApi()

    while True:
        raw = hh_api.get({'area': area, 'text': text, 'page': page, 'per_page': 100})
        model = HHVacancyBaseModel.model_validate_json(raw)
        if count <= 100:  # Кол-во меньше "записей на страницу"
            vacancies.extend(model.get_vacancy()[:count])
            break
        elif count > 100:  # Кол-во больше "записей на страницу"
            vacancies.extend(model.get_vacancy())
            count -= 100
            page += 1
        if model.page == model.pages:  # Если следующей страницы нет, выходим
            break

    return vacancies
