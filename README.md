# home-measurements
Little project to measure temp &amp; humidity using Raspberry Pi and sensors

```commandline
docker build -t measurements-api .
docker run -d --name meas-api -p 8000:8000 fastapi-app \
 -e DB_HOST=<yourhost> \
 -e DB_USER=<youruser> \
 -e DB_PASSWORD=<yourpassword> \
 -e DB_NAME=<yourpassword 
 measurements-api:latest
```