![example workflow](https://github.com/32aleksey32/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# yamdb-final - спринт №16 в Яндекс.Практикум
## Спринт 16 - CI и CD проекта api_yamdb

### ip сервера
51.250.17.126

### Стек технологий использованный в проекте:
- Python 3.7
- Django 2.2.16
- DRF
- JWT
- Docker

### Как запустить проект:
#### Требования

- Регистрация на Docker Hub
- Настроенный SSH доступ к серверу по ключу с паролем
- Регистрация на GitHub
- Выделенный сервер Linux Ubuntu 20.04 с с публичным IP адресом

#### Настройка GitHub Secrets
Клонируйте репозиторий и настройте переменные GitHub secrets согласно Вашему окружению

- DOCKER_USERNAME   #логин от аккаунта на Docker Hub
- DOCKER_PASSWORD   #пароль от аккаунта на Docker Hub
- HOST              #публичный адрес сервера для доступа по SSH
- USER  
- SSH_KEY #скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу: cat ~/.ssh/id_rsa
- SSH_PASSWORD
- TELEGRAM_TOKEN #токен вашего бота. Получить этот токен можно у бота @BotFather
- TELEGRAM_TO #id того кто будет получать сообщение от бота. Узнать свой ID можно у бота @userinfobot
- DB_ENGINE пример django.db.backends.postgresql
- DB_NAME #имя образа docker-compose с базой - db
- DB_POSTGRES_USER
- DB_POSTGRES_PASSWORD
- DB_HOST
- DB_PORT

#### Инструкции для развертывания и запуска приложения
- Зайдите на сервер
- Установите docker 
```
sudo apt install docker.io
```

- Установиите docker-compose на сервер:
```
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

- Остановите службу nginx командой
```
sudo systemctl stop nginx
```

- Скопируйте файлы из директории infra в домашную папку пользователя:
```
docker-compose.yaml
nginx - сохраняя стурктуру и название папок
```
  
