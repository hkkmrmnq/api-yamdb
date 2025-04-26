# api_yamdb

### Описание:
Учебный проект в рамках курса "Python-разработчик" от Яндекс.Практикум.
Реализует backend-часть и API приложения YaMDb.

Возможности API:
Пользователи. Самостоятельная регистрация. Отзывы на произведения, оценик произведениям. Комментирование к отзывам. Редактирование/удаление своих отзывов/комментариев.
Модераторы. Редактирование/удаление любых отзывов/комментариев.
Администраторы. Редактирование/удаление любых отзывов/комментариев. Добавление/редактирование/удаление произвеедений, жанров и категорий. Добавление/редактирование/удаление пользователей.

Полная [документация (Redoc)](http://127.0.0.1:8000/redoc/#tag/USERS/operation/%D0%94%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F).

### Технологии:

- Python 3.13.2
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

Запустить проект:

```shell
py manage.py runserver
```
