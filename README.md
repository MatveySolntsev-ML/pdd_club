# Серверное приложение для общения изучающих ПДД

Веб-сервис для курсовой работы (дисциплина «Интеграция и управление
приложениями на удаленном сервере», РЭУ им. Г.В. Плеханова). Реализован на
Django + Django REST Framework по спецификации из курсовой (главы 1–2):
модели, REST API, веб-интерфейс форума на Django-шаблонах, контейнерная
архитектура (nginx + backend + PostgreSQL).

## Запуск через Docker Compose

```
cp .env.example .env    # поправить SECRET_KEY/пароли
docker compose up -d --build
docker compose exec backend python manage.py createsuperuser
```

Сайт (форум) — `http://localhost/`, API — `http://localhost/api/`, админка — `http://localhost/admin/`.

## Запуск локально без Docker (для разработки)

```
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Без переменной `POSTGRES_DB` в окружении используется локальный `sqlite3`.

## Структура

- `users` — модель пользователя, аутентификация (JWT)
- `questions` — вопросы, темы ПДД, комментарии
- `favorites` — избранное и список на повторение
- `subscriptions` — подписки пользователей
- `core` — общие базовые классы и разрешения
- `api` — сериализаторы, вьюсеты, роутеры REST API (эндпоинты — см. Таблицу 2 курсовой работы)
- `frontend` — веб-интерфейс форума (Django-шаблоны): лента вопросов, темы, комментарии, избранное, список на повторение, лента подписок, профиль, вход/регистрация

Логотип и статика фронтенда — `frontend/static/frontend/images/`.
