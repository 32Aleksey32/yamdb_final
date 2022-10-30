![example workflow](https://github.com/32aleksey32/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# yamdb-final - спринт №16 в Яндекс.Практикум
## Спринт 16 - CI и CD проекта api_yamdb

### адрес сервера:
- http://84.201.165.7
- http://osipov32.ddns.net/

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

#### Инструкции для развертывания и запуска приложения
- Зайдите на удаленный сервер
- Установите docker 
  ```bash
  sudo apt install docker.io
  ```

- Установите docker-compose на сервер:
  ```bash
  curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  ```

- Остановите службу nginx командой
  ```bash
  sudo systemctl stop nginx
  ```

- Локально отредактируйте файл infra/nginx.conf, обязательно в строке server_name вписать IP-адрес сервера
- Скопируйте файлы docker-compose.yml и default.conf из директории infra на сервер, также создав папку nginx:
  ```bash
  scp .\infra\docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
  scp .\infra\nginx\default.conf <username>@<host>:/home/<username>/nginx/default.conf
  ```
- Для работы с Workflow добавитьте в Secrets GitHub переменные окружения для работы:
  ```
  - DOCKER_USERNAME=<логин от аккаунта на Docker Hub>
  - DOCKER_PASSWORD=<пароль от аккаунта на Docker Hub>

  - HOST=<публичный адрес сервера для доступа по SSH>
  - USER=<username для подключения к серверу> 
  - SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
  - PASSPHRASE=<пароль для сервера, если он установлен>

  - DB_ENGINE=<django.db.backends.postgresql>
  - DB_NAME=<имя базы данных postgres>
  - DB_POSTGRES_USER=<пользователь бд>
  - DB_POSTGRES_PASSWORD=<пароль>
  - DB_HOST=<db>
  - DB_PORT=<5432>

  - TELEGRAM_TOKEN=<токен вашего бота>. Получить этот токен можно у бота @BotFather
  - TELEGRAM_TO=<ID чата, в который придет сообщение>. Узнать свой ID можно у бота @userinfobot
  ```
  Workflow состоит из четырёх шагов:
    - Проверка кода на соответствие PEP8
    - Сборка и публикация образа бекенда на DockerHub.
    - Автоматический деплой на удаленный сервер.
    - Отправка уведомления в телеграм-чат.
     
- Соберите и запустите контейнеры на сервере:
  ```bash
  docker-compose up -d --build
  ```
- После успешной сборки выполните следующие действия (только при первом деплое):
    * проведите миграции внутри контейнеров:
      ```bash
      docker-compose exec web python manage.py makemigrations reviews
      docker-compose exec web python manage.py migrate
      ```
    * соберите статику проекта:
      ```bash
      docker-compose exec web python manage.py collectstatic --no-input
      ```  
    * Создайте суперпользователя Django, после запроса от терминала введите логин и пароль для суперпользователя:
      ```bash
      docker-compose exec web python manage.py createsuperuser
      ```

### Команды для заполнения базы данными
- Заполните базу данными
- Создайте резервную копию данных:
  ```bash
  docker-compose exec web python manage.py dumpdata > fixtures.json
  ```
