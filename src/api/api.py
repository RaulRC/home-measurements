import uvicorn
from fastapi import FastAPI

from src.db.db_connector import DB
from src.domain.measurement import Measurement


app = FastAPI()


@app.post("/sensor-data/")
async def receive_sensor_data(data: Measurement):
    try:
        DB().store_measurement(data)
        return {"message": "Sensor data saved successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
