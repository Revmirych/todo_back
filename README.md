# FastAPI TODO Backend

## Описание

Этот проект — серверная часть приложения для управления задачами (TODO), написанная на FastAPI.

### Основные возможности:
- Регистрация и аутентификация пользователей
- CRUD-операции для задач (создание, просмотр, изменение, удаление)
- Категории задач
- Приоритеты, статусы, дедлайны
- JWT-токены для авторизации
- Докеризация (Dockerfile и docker-compose)

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```sh
   git clone https://github.com/Revmirych/todo_back.git
   cd todo_back
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # или
   source venv/bin/activate  # Linux/Mac
   ```
3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Запустите сервер:**
   ```sh
   uvicorn app.main:app --reload
   ```
5. **Документация API:**
   Откройте [http://localhost:8000/docs](http://localhost:8000/docs)

## Запуск через Docker

```sh
docker build -t todo_back .
docker run -p 8000:8000 todo_back
```

## Переменные окружения
- DATABASE_URL — строка подключения к базе данных PostgreSQL (по умолчанию используется встроенная)

## Структура проекта
- `app/` — основной код приложения
- `alembic/` — миграции базы данных
- `tests/` — тесты

---

**Автор:** [Revmirych](https://github.com/Revmirych)
