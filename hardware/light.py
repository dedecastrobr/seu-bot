
from gpiozero import LED
from utils import config, Logger
from time import sleep

logger = Logger(config.get("bot_logfile"))

class Light:

    def __init__(self, name):
        self.name = name
        self.pin = config['gpio']['lights'][self.name]
        self.light = LED(self.pin)

    def toggle(self):
        self.light.toggle()
        sleep(0.5)

    def on(self):
        self.light.off()

    def on(self):
        self.light.off()
