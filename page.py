from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from db import Database

app = FastAPI()
db = Database()  

class Reading(BaseModel):
    node: int
    humidity: float

@app.on_event("startup")
def startup_event():
    db.initDataBase()

@app.get("/")
def read_root():
    return {"This shit doesnt work XDDDDD"}

@app.get("/readings")
def read_readings():
    return db.get_all_readings()

@app.post("/readings")
def create_reading(reading: Reading):
    db.writeData({
        "node": reading.node,
        "humidity": reading.humidity
    })
    return {
        "message": "Lectura insertada con éxito",
        "data": reading
    }

if __name__ == "__main__":
    uvicorn.run("page:app", host="127.0.0.1", port=8000, reload=True)