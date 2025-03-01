import json
import os
import threading
from time import sleep
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from utils import get_config, save_config, Logger

logger = Logger(get_config().get("admin_logfile"))
app = FastAPI()

admin_thread = None
camera = Camera()

# Model for config update
class ConfigUpdate(BaseModel):
    new_config: dict

@app.post("/update-config")
async def update_config(update: ConfigUpdate):
    try:
        save_config(update.new_config)
        logger.info("Config updated!")
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_web_server():
    global admin_thread

    if admin_thread and admin_thread.is_alive():
        logger.info("Bot admin is already running.")
        sleep(1)
        return

    admin_thread = threading.Thread(target=run_server, daemon=True)
    admin_thread.start()
    sleep(1)

def is_alive():
    return admin_thread and admin_thread.is_alive()
