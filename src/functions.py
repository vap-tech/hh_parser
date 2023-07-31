from src.api import VacancyApi
from src.models import VacancyBase
from src.area_selector import AreaSelector


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


def load_api():
    """Загружает данные из Api"""
    area_id_ = None

    if not input('Задать местность для поиска Enter-да/0-нет '):
        area_id_ = AreaSelector().get()

    word = input('Введите ключевое слово для поиска: ')

    while 1:

        count_vac = input('Введите количество вакансий от 1 до 2000')

        if not count_vac.isdigit():
            print('Некорректный ввод')
            continue
        count_vac = int(count_vac)

        if not 0 < count_vac <= 2000:
            print('Некорректный ввод')
            continue

        break

    return vacancy_collector(VacancyApi(), word, area_id_, count_vac)
