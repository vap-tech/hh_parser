from src.api import SJApi, HHApi
from src.parser import SJBaseModel, HHBaseModel
from src.file_connector import JsonConnector
from src.constants import FILENAME


def sj_collector(text: str, area: list, count: int) -> list:
    """
    Получает заданное число вакансий SuperJob
    :param text: Текст для запроса
    :param area: Массив локаций
    :param count: Количество вакансий
    :return: Массив объектов Vacancy
    """

    # Если пользователь хочет больше, чем может API, отдаём максимум 500
    count = count if 0 < count < 500 else 500

    area = area[1] if area else None
    vacancies = []
    page = 0
    sj_api = SJApi()

    while True:
        # keyword - ключевое слово, town - город, page - страница, count - записей на страницу
        raw = sj_api.get_vacancies({'keyword': text, 'town': area, 'page': page, 'count': 100})
        model = SJBaseModel.model_validate_json(raw)
        if count <= 100:  # Кол-во меньше "записей на страницу"
            vacancies.extend(model.get_vacancy()[:count])
            break
        elif count > 100:  # Кол-во больше "записей на страницу"
            vacancies.extend(model.get_vacancy())
            count -= 100
            page += 1
        if not model.more:  # Если на следующей странице пусто, выходим
            break

    return vacancies


def hh_collector(text: str, area: list, count: int) -> list:
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
    hh_api = HHApi()

    while True:
        raw = hh_api.get_vacancies({'area': area, 'text': text, 'page': page, 'per_page': 100})
        model = HHBaseModel.model_validate_json(raw)
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


def json_collector(count: int) -> list:
    """
    Получает заданное число вакансий из файла json
    :param count: Количество вакансий
    :return: Массив объектов Vacancy
    """
    data = JsonConnector(FILENAME).get()
    return data[:count]


def collector(text='Python', area=None, source=0b011, count=50) -> list:
    """
    Собирает вакансии из различных источников
    :param text: Текст запроса
    :param area: Массив с локацией для поиска
    :param source: Источники вакансий
    :param count: Количество вакансий из каждого источника
    :return: Массив объектов класса вакансия
    """
    vacancies = []
    if source & 1:  # SuperJob
        vacancies.extend(sj_collector(text, area, count))
    source = source >> 1
    if source & 1:  # HH
        vacancies.extend(hh_collector(text, area, count))
    source = source >> 1
    if source & 1:  # Json
        vacancies.extend(json_collector(count))

    return vacancies


def input_source() -> int:
    """
    Опрашивает пользователя из каких источников загружать данные
    На основании выбора пользователя подготавливает число,
    и возвращает его.
    """
    sources = 0
    sources_info = [
        'Нужно ли загружать вакансии из файла json? ',
        'Нужно ли загружать вакансии из API HH? ',
        'Нужно ли загружать вакансии из API SuperJob? '
    ]
    for src in sources_info:
        sources = sources << 1
        print(src)
        while True:
            user_input = int(input('1 - Да, 0 - Нет: '))
            if user_input == 1 or user_input == 0:
                break
            print('Некорректный ввод, повторите')
        sources += user_input

    return sources
