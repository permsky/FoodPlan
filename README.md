# FoodPlan

Сервис FoodPlan - кладезь рецептов на все случаи жизни. Сторонник классических рецептов? А может вам по душе кето-диета? Огромное количество рецептов не оставит равнодушным никого. Регистрируйтесь в боте, выбирайте предпочтения в блюдах, отмечайте продукты на которые у вас аллергия и получайте пошаговые рецепты приготовления блюд.

### Подготовительные действия
Создайте бота и получите токен. В этом вам поможет [BotFather](https://telegram.me/BotFather), для этого необходимо
ввести `/start` и следовать инструкции.

### Как запустить
1. Склонируйте код из репозитория
2. Настройте окружение. Для этого выполните следующие действия:
  - установите Python3.x;
  - создайте виртуальное окружение [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта и активируйте его.
  - установите необходимые зависимости:
    ```
    pip install -r requirements.txt
    ```
  - Создайте файл .env в корне проекта. Сохраните настройки django и telegram-бота в следующих переменных окружения:
    ```
    SECRET_KEY='секретный ключ django-проекта'
    DEBUG=True или False
    ALLOWED_HOSTS=localhost, HOST
    TG_TOKEN='Ваш токен telegram-бота'
    ```
3. Создайте файл базы данных и сразу примените все миграции командой:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
4. Создайте суперпользователя:
  ```bash
  python manage.py createsuperuser
  ```
5. Запустите создание записей в бд из recipe.json (получен с помощью скрипта parse_recipes.py):
  ```bash
  python manage.py load_from_json
  ```
6. Запустите сервер командой:
  ```bash
  python manage.py runserver
  ```
7. Перейдите по адресу localhost/admin. Используя данные суперпользователя, зайдите в админку. Создайте объекты "Аллегрии" и настройте их, прикрепив соответствующие категории блюд.
8. Запустите бота командой:
  ```bash
  python manage.py tg_bot
  ```
