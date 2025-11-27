# Быстрый деплой на сервер

## Сервер
- **IP**: 194.110.54.230
- **User**: ubuntu
- **Password**: LPrMf+G+9F3JcwFxntRLIHE=

## Способ 1: Через WinSCP (Windows)

1. Скачайте и установите WinSCP
2. Создайте новое соединение:
   - Host: 194.110.54.230
   - User: ubuntu
   - Password: LPrMf+G+9F3JcwFxntRLIHE=
3. Подключитесь
4. Загрузите всю папку `avtomat` в `/home/ubuntu/avtomat`

## Способ 2: Через SSH команды

### С Windows (используя Git Bash или WSL):

```bash
# Загрузить файлы
scp -r C:\Users\Umar\Desktop\avtomat ubuntu@194.110.54.230:~/avtomat

# Подключиться к серверу
ssh ubuntu@194.110.54.230
```

### На сервере:

```bash
cd ~/avtomat

# Создать .env.production
nano .env.production
# Заполните:
# SECRET_KEY=<generate-with-openssl-rand-hex-32>
# DEBUG=False
# ALLOWED_HOSTS=194.110.54.230,localhost
# POSTGRES_PASSWORD=<strong-password>
# TELEGRAM_BOT_TOKEN=<your-token>
# MINI_APP_URL=https://194.110.54.230

# Запустить деплой
chmod +x remote_deploy.sh
./remote_deploy.sh
```

## Способ 3: Автоматический (если есть SSH ключ)

```bash
# С локальной машины
ssh ubuntu@194.110.54.230 "mkdir -p ~/avtomat"
scp -r * ubuntu@194.110.54.230:~/avtomat/
ssh ubuntu@194.110.54.230 "cd ~/avtomat && chmod +x remote_deploy.sh && ./remote_deploy.sh"
```

## После деплоя

1. Проверьте работу:
   - http://194.110.54.230/ - Frontend
   - http://194.110.54.230/api/cities/ - API
   - http://194.110.54.230/admin/ - Admin

2. Настройте BotFather:
   - Откройте @BotFather
   - `/newapp`
   - URL: `https://194.110.54.230`

## Просмотр логов

```bash
ssh ubuntu@194.110.54.230
cd ~/avtomat
docker-compose -f docker-compose.prod.yml logs -f
```

