# api_yamdb

### Описание:
Учебный проект в рамках курса "Python-разработчик" от Яндекс.Практикум.
Реализует backend-часть и API приложения YaMDb.

Возможности API:
Пользователи. Самостоятельная регистрация. Отзывы на произведения, оценки произведениям. Комментирование к отзывам. Редактирование/удаление своих отзывов/комментариев.
Модераторы. Редактирование/удаление любых отзывов/комментариев.
Администраторы. Редактирование/удаление любых отзывов/комментариев. Добавление/редактирование/удаление произвеедений, жанров и категорий. Добавление/редактирование/удаление пользователей.

Полная [документация (Redoc)](http://127.0.0.1:8000/redoc/).

### Технологии:

- Python 3.10.0
- Django
- Django REST Framework
- SimpleJWT

### Команда: [Вадим Белясов](https://github.com/hkkmrmnq), [Юлия Тлеубердина](https://github.com/Tleuberdina), [Ярослав Крюков](https://github.com/yaralk).

### Как запустить проект:

Клонировать репозиторий:

```shell
git clone git@github.com:hkkmrmnq/api-yamdb.git
```

Перейти в его директорию:

```shell
cd api-yamdb
```

Cоздать виртуальное окружение:

```shell
py -m venv venv
```

Активировать виртуальное окружение:

```shell
venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```shell
py -m pip install --upgrade pip
```

```shell
py -m pip install -r requirements.txt
```

Перейти в корневое приложение yatube_api:

```shell
cd api_yamdb
```

Выполнить миграции:

```shell
py manage.py migrate
```

Опционально. Импортировать тестовые данные:

```shell
py manage.py import_data_from_csv
```

Запустить проект:

```shell
py manage.py runserver
```
