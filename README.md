# hh_parser
## Сборщик вакансий
Программа позволяет получать информацию о вакансиях с разных платформ,
сохранять ее в файл и удобно работать с ней (добавлять, фильтровать, удалять).
В программе используется виртуальное окружение venv, тестирование средствами pytest
и pip в качестве менеджера зависимостей. 

### Использование
- Клонируйте исходный код
- Установите зависимости из файла requirements.txt
- В директории src в файле constants.py установите актуальное имя переменной окружения с ключом доступа SuperJob и имя файла для выходных данных
- Запустите на выполнение файл main.py, например так: python3 src\main.py

### Тестирование
Используйте следующую команду: coverage run -m pytest; coverage report -m
