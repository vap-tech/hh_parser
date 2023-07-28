import requests


class AreaSelector:
    """
    Класс выбора местности для сужения ареала поиска вакансий.
    Аргументировано дублированием вакансий в разных городах.
    """
    def __init__(self):
        self.data = requests.get(
            'https://api.hh.ru/areas',
            params={'User-Agent': 'api-test-agent'}
        ).json()

    def get(self):
        return self.get_area_id(self.data)

    def get_area_id(self, data: list):
        """
        Рекурсивный выбор id местности из справочника местности HH
        :param data:
            список местностей соответствующей ответу от api hh структуры
        :return:
            [id выбранной местности, name выбранной местности]
            id используется в HH, name используется с SuperJob
        """

        for i in range(len(data)):  # Выводим список местностей
            print(f'{i+1} {data[i]["name"]}')

        a = int(input('Введите код местности: '))-1

        if not data[a]['areas']:  # Базовый случай
            print(f'Ваш выбор - {data[a]["name"]}')
            return [data[a]['id'], data[a]['name']]
        return self.get_area_id(data[a]['areas'])  # Рекурсия
