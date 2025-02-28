import os
from picamera import PiCamera
from time import sleep

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.is_recording = False

    def start_recording(self, filepath):
        if not self.is_recording:
            self.camera.start_recording(filepath)
            self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            self.camera.stop_recording()
            self.is_recording = False

    def take_picture(self, filepath):
        self.camera.capture(filepath)

    def start_preview(self):
        self.camera.start_preview()

    def stop_preview(self):
        self.camera.stop_preview()

    def close(self):
        self.camera.close()