Task Tracker API

 

📖 Описание

Приложение Task Tracker — это простой сервис для управления задачами с авторизацией через JWT и фоновой обработкой с помощью Celery.

Основные возможности:

Регистрация и аутентификация пользователей (JWT).

CRUD-операции над задачами (каждый пользователь видит только свои задачи).

Фоновые задачи через Celery + Redis (отправка e-mail, retry, отслеживание статуса).

Миграции схемы БД через Alembic.

Контейнеризация Docker Compose.

Покрытие тестами (unit, integration, e2e) + CI через GitHub Actions.

🛠 Технологии и компоненты

FastAPI — веб-фреймворк.

SQLAlchemy 2.0 — ORM с асинхронной поддержкой.

Pydantic v2 — валидация и сериализация.

PostgreSQL — основная база данных.

Alembic — управление миграциями.

Celery + Redis — фоновые задачи.

Docker & Docker Compose — контейнеризация.

pytest, pytest-asyncio, httpx, testcontainers — тестирование.

GitHub Actions — CI/CD.

📦 Быстрый старт

1. Клонирование репозитория

git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>

2. Создание .env

Скопируйте файл-пример и заполните переменные:

cp .env.example .env
# Откройте .env и укажите свои значения

3. Генерация requirements.txt

Если вы используете Poetry и плагин export:

poetry self add poetry-plugin-export
poetry export --format requirements.txt --output requirements.txt --without-hashes

Или без плагина:

poetry install --no-dev
pip freeze > requirements.txt

4. Запуск через Docker Compose

docker compose up --build -d

После этого:

API доступно по http://localhost:8000

Swagger UI — http://localhost:8000/docs

Celery воркер в логах контейнера worker.

🔧 Миграции

При первом старте (или при обновлении моделей) Alembic выполнит миграции:

# при сборке контейнера через entrypoint
# либо вручную:
alembic upgrade head

🚀 Пример использования

Регистрация

curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"bob","email":"bob@example.com","password":"pass123"}'

Логин

curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"bob@example.com","password":"pass123"}'

Ответ: { "access_token": "...", "token_type": "bearer" }

Получить профиль

curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <TOKEN>"

Создать задачу

curl -X POST http://localhost:8000/tasks/ \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title":"Test","description":"Desc"}'

Запустить фоновую задачу

curl http://localhost:8000/ping/send-test-email

Возвращает task_id, статус можно проверить:

curl http://localhost:8000/ping/task-status/<TASK_ID>

🧪 Тестирование

Все тесты запускаются через pytest в контейнере CI или локально:

pytest --cov=app --cov-report=xml

📈 CI/CD

Настроен GitHub Actions (.github/workflows/ci.yml):

Поднимает Postgres и Redis

Запускает миграции

Запускает Celery воркер

Прогоняет тесты и собирает покрытие

📜 Лицензия

MIT ©Phoblas