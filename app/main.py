#app/main.py
from fastapi import FastAPI
from api.schedule import router as schedule_router

app = FastAPI()

app.include_router(schedule_router, prefix="/api/v1/schedules")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
