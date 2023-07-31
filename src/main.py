from src.functions import load_api
from src.db_manager import DBManager

data = ['1 - Загрузить данные из hh в БД',
        '2 - Вывести все компании и количество их вакансий',
        '3 - Вывести список всех вакансий',
        '4 - Вывести среднюю зарплату по вакансиям',
        '5 - Вывести вакансии, у которых зарплата выше средней',
        '6 - Вывести из БД вакансии по ключевому слову',
        '7 - Проинициализировать БД (если первый запуск)',
        '10 - выйти из программы',
        'Введите число: ']

manager = DBManager()

while 1:
    action = input('\n'.join(data))

    if action == '1':
        vacs = load_api()
        manager.vacancy_to_db(vacs)
        print('OK')

    if action == '2':
        data = manager.get_companies_and_vacancies_count()
        for i in data:
            print(*i)

    if action == '3':
        data = manager.get_all_vacancies()
        for i in data:
            print(*i)

    if action == '4':
        data = manager.get_avg_salary()
        for i in data:
            print(*i)

    if action == '5':
        data = manager.get_vacancies_with_higher_salary()
        for i in data:
            print(*i)

    if action == '6':
        data = manager.get_vacancies_with_keyword(input('Слово: '))
        for i in data:
            print(*i)

    if action == '7':
        data = manager.create_table()

    if action == '10':
        break

