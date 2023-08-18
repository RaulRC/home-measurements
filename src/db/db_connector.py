from datetime import datetime
import mysql.connector
import os
# MySQL configuration
db_config = {
    "host": os.environ['DB_HOST'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASSWORD'],
    "database": os.environ['DB_NAME'],
}


class DB:
    def __init__(self):
        self._connect()

    def get_measurements(self):
        # Fetch all measurements from the database
        query = "SELECT * FROM measurements"
        return self._execute(query)

    def store_measurement(self, data):
        # Insert data into the database
        insert_query = (
            "INSERT INTO measurements (temperature, humidity, place, room, timestamp) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        insert_data = (data.temperature, data.humidity, data.place, data.room, data.timestamp)
        self._store(insert_query, insert_data)

    def _connect(self):
        self.db = mysql.connector.connect(**db_config)

    def _store(self, query, data):
        cursor = self.db.cursor()
        cursor.execute(query, data)
        self.db.commit()
        self._close()

    def _execute(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def _close(self):
        self.db.close()