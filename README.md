# Бот - ассистент


## Описание

Телеграм - бот обращается к API сервису Практикум.Домашка и узнаёт статус домашней работы: взята ли домашняя работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Пример ответа бота - ассистента:

```python
{
   "homeworks":[
      {
         "id":123,
         "status":"approved",
         "homework_name":"egorcoders__homework_bot-master.zip",
         "reviewer_comment":"Всё нравится",
         "date_updated":"2021-12-14T14:40:57Z",
         "lesson_name":"Итоговый проект"
      }
   ],
   "current_date":1581804979
}
```

## Установка

1. Клонировать репозиторий:

    ```python
    git clone https://github.com/golenkovyura/homework_bot.git
    ```

2. Перейти в папку с проектом:

    ```
    cd homework_bot
    ```

3. Установить виртуальное окружение для проекта:

    ```
    python -m venv venv
    ```

4. Активировать виртуальное окружение для проекта:

    ```
    source venv/Scripts/activate
    ```

5. Установить зависимости:

    ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

6. Выполнить миграции на уровне проекта:

    ```
    cd yatube
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Зарегистрировать чат-бота в Телеграм

8. Создать в корневой директории файл .env для хранения переменных окружения

    ```python
    PRAKTIKUM_TOKEN = 'xxx'
    TELEGRAM_TOKEN = 'xxx'
    TELEGRAM_CHAT_ID = 'xxx'
    ```

9. Запустить проект локально:

    ```
    python3 homework_bot.py
    ```
