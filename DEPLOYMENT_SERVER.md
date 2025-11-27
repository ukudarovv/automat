# Деплой на Ubuntu сервер

## Информация о сервере

- **IP**: 194.110.54.230
- **OS**: Ubuntu 24.04 LTS
- **User**: ubuntu
- **Resources**: 1 CPU, 1 GB RAM, 20 GB Disk

## Шаг 1: Подключение к серверу

```bash
ssh ubuntu@194.110.54.230
# Password: LPrMf+G+9F3JcwFxntRLIHE=
```

## Шаг 2: Настройка сервера

После подключения выполните:

```bash
# Загрузите setup_server.sh на сервер
chmod +x setup_server.sh
./setup_server.sh
```

Или выполните команды вручную:

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

## Шаг 3: Загрузка проекта на сервер

### Вариант A: Через Git

```bash
cd ~
git clone <your-repo-url> avtomat
cd avtomat
```

### Вариант B: Через SCP (с локальной машины)

```bash
# С локальной машины
scp -r C:\Users\Umar\Desktop\avtomat ubuntu@194.110.54.230:~/avtomat
```

## Шаг 4: Настройка переменных окружения

```bash
cd ~/avtomat
cp .env.production.example .env.production
nano .env.production
```

Заполните:
```
SECRET_KEY=<generate-with-openssl-rand-hex-32>
DEBUG=False
ALLOWED_HOSTS=194.110.54.230,localhost
POSTGRES_PASSWORD=<strong-password>
TELEGRAM_BOT_TOKEN=<your-token>
MINI_APP_URL=https://194.110.54.230
```

## Шаг 5: Сборка React приложения

```bash
cd frontend
npm install
npm run build
cd ..
```

## Шаг 6: Деплой

```bash
chmod +x deploy.sh
./deploy.sh
```

## Шаг 7: Настройка BotFather

1. Откройте @BotFather в Telegram
2. Выберите вашего бота
3. Отправьте `/newapp`
4. Введите URL: `https://194.110.54.230`
5. Сохраните изменения

## Проверка работы

- API: http://194.110.54.230/api/cities/
- Frontend: http://194.110.54.230/
- Admin: http://194.110.54.230/admin/

## Управление

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Остановка
docker-compose -f docker-compose.prod.yml down

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Обновление
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

