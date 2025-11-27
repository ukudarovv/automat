# AvtoMat MVP

Telegram Mini App для записи учеников в автошколы и к инструкторам с веб-CRM панелью.

## Технологический стек

- **Frontend**: React + TypeScript (Telegram Mini App)
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Bot**: aiogram 3.x
- **Deployment**: Docker + Docker Compose + Nginx

## Быстрый старт

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ukudarovv/automat.git
cd automat
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

3. Настройте переменные окружения:
```bash
cp .env.production.example .env
# Отредактируйте .env и добавьте TELEGRAM_BOT_TOKEN
```

4. Запустите миграции:
```bash
python manage.py migrate
python manage.py init_cities
python manage.py create_test_data
```

5. Запустите серверы:
```bash
# Терминал 1: Django
python manage.py runserver 0.0.0.0:8001

# Терминал 2: React
cd frontend && npm start

# Терминал 3: Bot
python run_bot.py
```

### Деплой на сервер

1. Клонируйте на сервере:
```bash
git clone https://github.com/ukudarovv/automat.git
cd automat
```

2. Создайте `.env.production`:
```bash
cp .env.production.example .env.production
nano .env.production
```

3. Запустите деплой:
```bash
chmod +x remote_deploy.sh
./remote_deploy.sh
```

## Структура проекта

```
avtomat/
├── api/              # Django REST API
├── bot/              # Telegram Bot
├── core/             # Django core
├── crm/              # CRM модули
├── frontend/          # React Mini App
├── templates/         # Django templates
├── Dockerfile         # Backend Dockerfile
├── docker-compose.prod.yml  # Production compose
└── nginx.conf        # Nginx configuration
```

## API Endpoints

- `GET /api/cities/` - список городов
- `GET /api/schools/?city={city}` - школы по городу
- `GET /api/instructors/?city={city}&auto_type={type}` - инструкторы
- `POST /api/applications/` - создание заявки
- `POST /api/auth/telegram/` - авторизация через Telegram

## Документация

- `DEPLOYMENT_SERVER.md` - подробная инструкция по деплою
- `QUICK_DEPLOY.md` - быстрый деплой
- `MINIAPP_README.md` - документация Mini App

## Лицензия

MIT
