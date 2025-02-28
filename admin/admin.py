import json
import os
import threading
from time import sleep
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from utils import get_config, save_config, Logger
from hardware.camera import Camera

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

@app.post("/start-camera")
async def start_camera():
    try:
        camera.start_preview()
        return {"message": "Camera started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop-camera")
async def stop_camera():
    try:
        camera.stop_preview()
        return {"message": "Camera stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream")
async def stream():
    def generate():
        while camera.is_recording:
            frame = camera.capture_continuous()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def index():
    html_content = """
    <html>
        <head>
            <title>Seu Bot Admin Interface</title>
        </head>
        <body>
            <h1>Seu Bot Admin Interface</h1>
            <h2>Camera Stream</h2>
            <img src="/stream" width="640" height="480">
            <form action="/start-camera" method="post">
                <button type="submit">Start Camera</button>
            </form>
            <form action="/stop-camera" method="post">
                <button type="submit">Stop Camera</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
