# Деплой Telegram Mini App

## Локальная разработка

### 1. Запуск Django Backend

```bash
python manage.py runserver 0.0.0.0:8001
```

### 2. Запуск React Frontend

```bash
cd frontend
npm install
npm start
```

Приложение будет доступно на `http://localhost:3000`

## Продакшн деплой

### Вариант 1: Статический хостинг (Vercel/Netlify)

1. Соберите React приложение:
```bash
cd frontend
npm run build
```

2. Загрузите папку `build` на Vercel или Netlify

3. Настройте переменные окружения:
   - `REACT_APP_API_URL` - URL вашего Django API

4. Обновите `MINI_APP_URL` в `.env` бота на URL вашего хостинга

### Вариант 2: Django Static Files

1. Соберите React приложение:
```bash
cd frontend
npm run build
```

2. Скопируйте содержимое `frontend/build` в `staticfiles/`

3. Django будет обслуживать статические файлы

## Настройка в BotFather

1. Откройте @BotFather в Telegram
2. Выберите вашего бота
3. Отправьте `/newapp`
4. Выберите бота
5. Введите название приложения
6. Введите описание
7. Загрузите иконку (512x512px)
8. Введите URL вашего Mini App (например: `https://your-domain.com`)
9. Сохраните изменения

## Обновление URL в коде

Обновите `MINI_APP_URL` в `.env`:
```
MINI_APP_URL=https://your-production-url.com
```

