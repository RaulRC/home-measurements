# home-measurements
Little project to measure temp &amp; humidity using Raspberry Pi and sensors

```commandline
docker build -t measurements-api .
docker run -d --name meas-api -p 8000:8000 \
 -e DB_HOST=<yourhost> \
 -e DB_USER=<youruser> \
 -e DB_PASSWORD=<yourpassword> \
 -e DB_NAME=<yourpassword> 
 measurements-api:latest
```

# MySQL

```commandline
docker run --name mysql-home-iot -p 3306:3306 \
 -e MYSQL_ROOT_PASSWORD=<password> \
 -e MYSQL_DATABASE=<db> \
 -e MYSQL_USER=<user> \
 -e MYSQL_PASSWORD=<password> \
 -d \
 mysql:latest
```

# PG

```commandline
docker run -p 5432:5432 --name home-iot-pg -e POSTGRES_PASSWORD=<your_password> -e POSTGRES_USER=<your_user> -d postgres:latest
```