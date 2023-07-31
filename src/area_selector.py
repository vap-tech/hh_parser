from src.api import AreaApi


class AreaSelector:
    """Класс выбора местности для поиска вакансий."""
    def __init__(self):
        self.data = AreaApi().get_request().json()

    def get(self):
        return self.__get_area_id(self.data)

    def __get_area_id(self, data: list):
        """
        Рекурсивный выбор id местности из справочника местности HH
        :param data:
            список местностей соответствующей ответу от api hh структуры
        :return:
            id выбранной местности
        """

        for i in range(len(data)):  # Выводим список местностей
            print(f'{i+1} {data[i]["name"]}')

        a = int(input('Введите код местности: '))-1

        if not data[a]['areas']:  # Базовый случай
            print(f'Ваш выбор - {data[a]["name"]}')
            return int(data[a]['id'])
        return self.__get_area_id(data[a]['areas'])  # Рекурсия
