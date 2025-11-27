# Инструкция по развертыванию AvtoMat MVP

## Предварительные требования

- Python 3.9+
- PostgreSQL 15+ (или Docker)
- Telegram Bot Token (получить у @BotFather)

## Шаг 1: Установка зависимостей

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Шаг 2: Настройка базы данных

### Вариант A: Использование Docker

```bash
# Запустить PostgreSQL
docker-compose up -d

# Проверить, что контейнер запущен
docker ps
```

### Вариант B: Локальный PostgreSQL

Создайте базу данных:
```sql
CREATE DATABASE avtomat_db;
CREATE USER avtomat_user WITH PASSWORD 'avtomat_password';
GRANT ALL PRIVILEGES ON DATABASE avtomat_db TO avtomat_user;
```

## Шаг 3: Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
SECRET_KEY=your-secret-key-here-generate-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://avtomat_user:avtomat_password@localhost:5432/avtomat_db
TIME_ZONE=Asia/Almaty
```

**Важно**: Замените `TELEGRAM_BOT_TOKEN` на реальный токен от @BotFather!

## Шаг 4: Инициализация базы данных

```bash
# Применить миграции
python manage.py migrate

# Инициализировать города
python manage.py init_cities

# Создать суперпользователя для Django Admin
python manage.py createsuperuser
```

## Шаг 5: Создание тестовых данных (опционально)

В Django Admin (`http://localhost:8000/admin/`):
1. Войдите как суперпользователь
2. Создайте пользователя с ролью "Автошкола"
3. Создайте запись в разделе "Автошколы", связанную с этим пользователем
4. Аналогично создайте инструктора

## Шаг 6: Запуск приложения

### Терминал 1: Django сервер

```bash
python manage.py runserver
```

Сервер будет доступен на `http://localhost:8000`

### Терминал 2: Telegram бот

```bash
python bot/main.py
```

Бот должен запуститься и начать отвечать на команды.

## Проверка работы

1. **Telegram бот**: Откройте бота в Telegram и отправьте `/start`
2. **Веб-CRM для автошкол**: `http://localhost:8000/crm/schools/login/`
3. **Веб-CRM для инструкторов**: `http://localhost:8000/crm/instructors/login/`
4. **Django Admin**: `http://localhost:8000/admin/`

## Структура пользователей

### Создание автошколы через Admin:

1. Создайте пользователя с ролью `school`
2. Создайте запись в "Автошколы", связанную с пользователем
3. Заполните поля: название, город, адрес, WhatsApp, ссылки на оплату

### Создание инструктора через Admin:

1. Создайте пользователя с ролью `instructor`
2. Создайте запись в "Инструкторы", связанную с пользователем
3. Заполните поля: имя, город, тип авто, телефон

## Решение проблем

### Бот не отвечает
- Проверьте, что `TELEGRAM_BOT_TOKEN` правильный
- Убедитесь, что бот запущен (`python bot/main.py`)
- Проверьте логи на наличие ошибок

### Ошибка подключения к БД
- Убедитесь, что PostgreSQL запущен
- Проверьте `DATABASE_URL` в `.env`
- Проверьте права пользователя БД

### Ошибки миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production развертывание

Для production:
1. Установите `DEBUG=False` в `.env`
2. Настройте `ALLOWED_HOSTS` с вашим доменом
3. Используйте веб-сервер (nginx + gunicorn)
4. Настройте SSL сертификаты
5. Используйте переменные окружения сервера вместо `.env` файла

