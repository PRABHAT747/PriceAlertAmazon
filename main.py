from fastapi import FastAPI
from db.database import Base, engine
from routes import subscriptions, history
import threading
import time
from services.tracking_service.tracker_service import run_tracker

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(subscriptions.router)
app.include_router(history.router)


def scheduler():
    while True:
        print("Running tracker...")
        run_tracker()
        time.sleep(120)

@app.get("/")
def root():
    return {
        "message": "Amazon Price Tracker API is running....",
        "docs": "/docs"
    }
@app.on_event("startup")
def start_scheduler():
    thread = threading.Thread(target=scheduler, daemon=True)
    thread.start()