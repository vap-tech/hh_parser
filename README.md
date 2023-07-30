# hh_parser
## Сборщик вакансий
Программа позволяет получать информацию о вакансиях с разных платформ,
сохранять ее в файл и удобно работать с ней (добавлять, фильтровать, удалять).
В программе используется виртуальное окружение venv, тестирование средствами pytest
и pip в качестве менеджера зависимостей. 

### Использование
- Клонируйте исходный код
- Установите зависимости из файла pyproject.toml
- В директории src в файле constants.py установите актуальные параметры подключения к бд
- Запустите на выполнение файл main.py, например так: python3 src\main.py

### Тестирование
Используйте следующую команду: coverage run -m pytest; coverage report -m

### Внимание
Перед установкой зависимостей необходимо убедиться в наличии интерфейса PostgreSQL для программирования приложений на языке C

Установить можно например так:

sudo apt install libpq-dev 