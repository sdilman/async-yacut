### О проекте Yacut:

Проект yacut позволяет загружать файлы в Яндекс-облако и создавать для них короткие ссылки

Расположение проекта: https://github.com/sdilman/async-yacut

Автор: https://github.com/sdilman

Технологии:

| Категория       | Технологии                          |
|-----------------|-------------------------------------|
| Backend         | Python 3.9+, Flask 2.0+             |
| База данных     | SQLite (с Alembic для миграций)     |
| Хранилище       | Яндекс.Диск (через REST API)        |
| Асинхронность   | aiohttp, asyncio                    |


### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:sdilman/async-yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с переменными окружения:

```
FLASK_APP=yacut
DATABASE_URI='sqlite:///db.sqlite3'
SECRET_KEY='17268wt1782187t2871et8t387te'
DISK_TOKEN='<ваш токен>'
API_HOST='https://cloud-api.yandex.net/'
API_VERSION='v1'
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```

Примеры запросов к API:

POST /api/id

{
  "url": "string",
  "custom_id": "string"
}

GET /api/id/{short_link}