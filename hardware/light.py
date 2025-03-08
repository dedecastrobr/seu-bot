from gpiozero import LED
from utils import get_config, Logger
from time import sleep

logger = Logger(get_config().get("bot_logfile"))

class Light:

    def __init__(self, name, pin):
        self.name = name
        try:
            self.config = get_config()
            self.name = name
            self.pin = pin
            self.light = LED(self.pin)
        except KeyError as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Error initializing light {self.name}: {e}") from e

    def toggle(self):
        self.light.toggle()
        sleep(0.5)

    def blink(self):
        self.light.blink()

    def on(self):
        self.light.on()

    def off(self):
        self.light.off()
