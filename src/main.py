from src.functions import collector, input_source
from src.area_selector import AreaSelector


def main():

    src = input_source()  # Получаем источники вакансий
    count = int(input('Сколько вакансий загрузить из каждого источника? '))   # Запросили кол-во вакансий
    area = AreaSelector().get() if src not in [0, 4] else None  # Получаем город
    key_word = input('Введите ключевое слово для поиска: ') if src not in [0, 4] else None  # Получаем ключевое слово

    vacancies_list = collector(key_word, area, src, count)  # Получаем вакансии из источников

    print('\nВакансии загружены\nОчистить Json?\n')

    jc = JsonConnector(FILENAME)  # Объект для работы с файлом Json

    user_input = input('Enter - нет, y/д - да ')
    if user_input != '':
        jc.clear()
        print('Json файл очищен')

    print('Отсортировать полученные вакансии по заработной плате?')

    user_input = input('Enter - да, n/н - нет ')
    if user_input == '':
        vacancies_list.sort(reverse=True)
        print('Вакансии отсортированы')

    display = 0
    json_only = 1 if src in [0, 4] else None
    while src:
        if src & 1:
            display += count
        src = src >> 1

    print(display)
    print('Сколько вакансий вывести на экран?')

    while True:
        user_input = input(f'от 0 до {display} ')
        try:
            user_input = int(user_input)
        except ValueError:
            print('Неправильный ввод')
            continue
        else:
            if 0 <= user_input <= display:
                display = user_input
                break
        print('Неправильный ввод')

    for i in vacancies_list[:display]:
        print(i)

    if not json_only:
        jc.add(vacancies_list)
        print('\nВсе вакансии добавлены в файл Json')
        print('При следующем запуске можно работать с ними без обращения к API')


if __name__ == '__main__':
    main()
