# AvtoMat MVP

Telegram-бот для записи учеников в автошколы и к инструкторам с веб-CRM панелью.

## Технологический стек

- **Telegram Bot**: aiogram 3.x
- **Web CRM**: Django 4.2
- **База данных**: PostgreSQL 15

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
Создайте файл `.env` со следующим содержимым:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://avtomat_user:avtomat_password@localhost:5432/avtomat_db
TIME_ZONE=Asia/Almaty
```

5. Запустите PostgreSQL (через Docker):
```bash
docker-compose up -d
```

6. Выполните миграции Django:
```bash
python manage.py migrate
```

7. Инициализируйте города:
```bash
python manage.py init_cities
```

8. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

9. Запустите Django сервер:
```bash
python manage.py runserver
```

10. Запустите Telegram бота (в отдельном терминале):
```bash
python bot/main.py
```

## Структура проекта

```
avtomat/
├── bot/                    # Telegram бот
│   ├── handlers/          # Обработчики команд
│   ├── keyboards/         # Клавиатуры
│   ├── services/          # Бизнес-логика
│   └── main.py            # Точка входа
├── crm/                   # Django веб-CRM
│   ├── schools/           # CRM для автошкол
│   ├── instructors/       # CRM для инструкторов
│   ├── applications/      # Управление заявками
│   └── analytics/         # Аналитика
├── core/                  # Общие модели и настройки
└── manage.py             # Django управление
```

## Основные функции

### Для учеников:
- Запись в автошколы (выбор города, категории, формата)
- Запись к инструкторам (выбор города, типа авто, времени)
- Автоматические ответы с данными школы/инструктора
- Ссылки на оплату (Kaspi/HalykPay)
- WhatsApp Deep Links для связи

### Для автошкол:
- Веб-CRM панель для управления заявками
- Изменение статусов заявок
- Отправка автоответов студентам
- Просмотр статистики
- Индекс доверия (автоматический расчет)

### Для инструкторов:
- Веб-CRM панель для управления заявками
- Принятие/отклонение заявок
- Отметка уроков как проведенных
- Просмотр статистики

## Пользовательские потоки

1. **Flow 1**: Нет прав → Выбор города → Категория → Формат → Список школ → Заявка
2. **Flow 2**: Есть права → Выбор города → Тип авто → Список инструкторов → Время → Заявка
3. **Flow 3**: Есть сертификат → Выбор опции (практика/полный курс/тесты)

## Аналитика

Система автоматически отслеживает:
- Индекс дисциплины студента (время между шагами, возвраты, задержки)
- Индекс доверия автошколы (скорость ответа, % подтверждений, % оплат)

## Интеграции

- **WhatsApp Deep Links**: `https://wa.me/7XXXXXXXXXX?text=...`
- **Telegram Deep Links**: для перехода в бота с параметрами
- **Платежные ссылки**: Kaspi Pay и HalykPay (пока ручные ссылки)

## Доступ к CRM

- Автошколы: `http://localhost:8000/crm/schools/login/`
- Инструкторы: `http://localhost:8000/crm/instructors/login/`
- Django Admin: `http://localhost:8000/admin/`

