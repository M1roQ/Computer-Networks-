### Создание сети `my-network`
```
docker network create my-network
```

### Запуск контейнера с PostgreSQL
```
docker run --name my-postgres --network my-network -p 5433:5432 -e POSTGRES_USER=miro_q -e POSTGRES_PASSWORD=qwerty -e POSTGRES_DB=dockerdb -d postgres
```

`docker run` — команда для запуска нового контейнера.

`--name my-postgres` — задаёт имя контейнера.

`--network my-network` — подключает контейнер к сети Docker с именем my-network.

`-p 5433:5432` — пробрасывает порты. Порт 5433 на хосте будет связан с портом 5432 внутри контейнера.

`-e POSTGRES_USER=miro_q` — задаёт имя пользователя для PostgreSQL. 

`-e POSTGRES_PASSWORD=qwerty` — задаёт пароль для пользователя miro_q.

`-e POSTGRES_DB=dockerdb` — задаёт имя базы данных, которая будет создана при старте контейнера.

`-d` — запускает контейнер в фоновом режиме (detached mode). 

`postgres` — это образ Docker, который будет использоваться для создания контейнера.

### Запустить существующий контейнер `my-postgres`
```
docker start my-postgres
```

### Копирование `init.sql` в контейнер
```
docker cp init.sql my-postgres:/init.sql
```

### Выполнить SQL-скрипт внутри контейнера, подключаясь к базе данных PostgreSQL.
```
docker exec -it my-postgres psql -U miro_q -d dockerdb -f /init.sql
```

`docker exec` - Запускает команду внутри уже работающего контейнера.

`-it` - Флаги для интерактивного режима.

`my-postgres` - Имя контейнера, внутри которого нужно выполнить команду.

`psql` - Это PostgreSQL-клиент — командная утилита для работы с PostgreSQL. Она позволяет подключаться к базе и выполнять SQL-команды.

`-U miro_q` - Имя пользователя, под которым будет выполняться подключение к PostgreSQL.

`-d dockerdb` - Имя базы данных, к которой будет подключаться psql.

`-f /init.sql` - Флаг -f указывает, что нужно выполнить SQL-команды из файла. В данном случае файл находится внутри контейнера по пути /init.sql.

### Создание Docker-образа приложения
```
docker build -t my-app .
```

### Запуск собранного контейнера
```
docker run --name my-app --network my-network -p 5001:5001 -e DATABASE_URL=postgresql://miro_q:qwerty@my-postgres:5432/dockerdb -d my-app

```
`5001` — это порт, на котором работает Flask-приложение внутри контейнера.

`5555` — это порт, на котором можно обращаться к приложению снаружи.

### Запустить существующий контейнер `my-app`
```
docker start my-app
```

### Создание и настройка контейнера с Nginx
Перейдите в папку `nginx` и соберите образ для Nginx:
```
docker build -t my-nginx .
```

### Запуск контейнера
```
docker run --name my-nginx --network my-network -p 80:80 -d my-nginx
```

### Проверка работы

Добавить URL:
```
curl -X POST "http://localhost:/api/add_url?url=https://example.com"

```
Получить все URL:
```
curl "http://localhost:/api/urls"

```

### Пример вывода
\>```bash curl -X POST "http://localhost:/api/add_url?url=https://example.com" ```

\>```URL <https://example.com> added ```

\>```curl "http://localhost:/api/urls" ```

\>```[{"id":1,"url":"https://example.com"}] ```

### Остановить все контейнеры
```
docker stop $(docker ps -q)
```