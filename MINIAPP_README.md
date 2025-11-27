# Telegram Mini App - AvtoMat

## Реализовано

### Backend (Django REST API)
- ✅ Django REST Framework настроен
- ✅ CORS настроен для Telegram Web App
- ✅ API endpoints:
  - `GET /api/cities/` - список городов
  - `GET /api/schools/?city={city}` - школы по городу
  - `GET /api/instructors/?city={city}&auto_type={type}` - инструкторы
  - `POST /api/applications/` - создание заявки
  - `GET /api/applications/{id}/` - детали заявки
  - `POST /api/auth/telegram/` - авторизация через Telegram

### Frontend (React + TypeScript)
- ✅ React приложение создано
- ✅ Telegram Web App интеграция (useTelegram hook)
- ✅ Все потоки реализованы:
  - SchoolFlow - запись в автошколу
  - InstructorFlow - запись к инструктору
  - CertificateFlow - выбор опции с сертификатом
- ✅ API клиент с axios
- ✅ TypeScript типы для всех моделей
- ✅ Стилизация по Telegram Design Guidelines

### Bot Integration
- ✅ Бот обновлен с Web App кнопкой
- ✅ Команда /start показывает кнопку "Открыть приложение"

## Запуск

### 1. Установка зависимостей

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Запуск серверов

**Терминал 1 - Django:**
```bash
python manage.py runserver 0.0.0.0:8001
```

**Терминал 2 - React:**
```bash
cd frontend
npm start
```

### 3. Настройка бота

1. Откройте @BotFather в Telegram
2. Выберите вашего бота
3. Отправьте `/newapp`
4. Введите URL: `http://localhost:3000` (для разработки)
5. Для продакшна используйте ваш домен

### 4. Тестирование

1. Откройте бота в Telegram
2. Отправьте `/start`
3. Нажмите "🚀 Открыть приложение"
4. Mini App откроется внутри Telegram

## Структура проекта

```
avtomat/
├── api/                    # Django REST API
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # API routes
│   └── telegram_auth.py    # Telegram auth validation
├── frontend/               # React Mini App
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы (StartPage, SchoolFlow, etc.)
│   │   ├── services/       # API клиент
│   │   ├── hooks/          # useTelegram hook
│   │   ├── types/          # TypeScript типы
│   │   └── App.tsx         # Главный компонент
│   └── package.json
└── bot/                    # Telegram Bot (упрощен)
    └── handlers/
        └── start.py        # Web App кнопка
```

## Переменные окружения

Добавьте в `.env`:
```
MINI_APP_URL=http://localhost:3000  # Для разработки
# MINI_APP_URL=https://your-domain.com  # Для продакшна
```

## Деплой

См. `DEPLOYMENT_MINIAPP.md` для инструкций по деплою.

