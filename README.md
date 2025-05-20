# 🚀 Task Manager Bot - Управление задачами в Telegram

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.x-red)

Многофункциональный бот для управления задачами с веб-панелью администратора и умными уведомлениями.

## 🌟 Основные возможности

### 🤖 Telegram-бот
- ✅ Добавление задач с дедлайнами
- 📝 Редактирование существующих задач
- 📅 Умные напоминания о дедлайнах
- 📱 Интуитивно понятный интерфейс

### 💻 Веб-панель
- 👨‍💻 Администрирование задач
- 📊 Аналитика продуктивности
- 🎨 Адаптивный дизайн

## 🛠 Технологический стек

| Компонент       | Технологии                          |
|-----------------|-------------------------------------|
| Бекенд          | Python 3.8, Aiogram 3.x, FastAPI    |
| База данных     | PostgreSQL, SQLAlchemy 2.0          |
| Фронтенд        | Jinja2, Tailwind CSS, Alpine.js     |

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/ryazd/task_manager_bot.git
cd task-manager-bot
```

### 2. Создайте файл .env и заполните его
```
BOT_TOKEN=ваш_токен
DB_URL=postgresql+asyncpg://user:password@localhost:5432/task_bot_db
```

### 3. Установите зависимости и запустите
```bash
pip install requirements.txt    # установка зависимостей
python bot/main.py              # запуск бота
uvicorn web.main:app --reload   # запуск веб-панели
```


## 🚀 Пример работы бота

### 1. Добавление задач
![Добавление задач](README/add_tasks.gif)

### 2. Просмотр задач
![Список задач](README/list.gif)

### 3. Уведомление о дедлайне
 Каждые 30 минут происходит проверка дедлайнов у всех задач и если осталось меньше 1 часа, то бот присылает уведомление

<img src="README/deadline.jpg" alt="Уведомление о дедлайне" width='500' height='500'/>

## 🚀 Доступ к веб-панели

### 1. После запуска откройте в браузере
```
http://localhost:8000/admin/tasks
```
![Админка](README/admin.jpg)

