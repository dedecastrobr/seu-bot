
from gpiozero import LED
from utils import config, Logger
from time import sleep
from commands import CommandManager, Command

logger = Logger(config.get("bot_logfile"))

class Light:

    def __init__(self, name, gamepad=None, light_commands=[]):
        self.name = name
        self.pin = config['gpio']['lights'][self.name]
        self.light = LED(self.pin)

        if gamepad:
            self.gamepad = gamepad
            self.light_commands = light_commands
            self.command_manager = CommandManager(self.get_available_commands())
            self.command_handlers = {
                cmd["state"]: getattr(self, cmd["method"], self.invalid_method)
                for cmd in self.light_commands
            }

    def invalid_method(self):
        logger.error(f"Invalid method in command handlers for {self.name}")

    def get_available_commands(self):
        return [
            Command(
                state=cmd["state"],
                condition=lambda btn=cmd["controller"]: self.gamepad.getButtonState(btn) == 1
            )
            for cmd in self.light_commands  # Iterating over self.light_commands
        ]
    
    def handle_commands(self):
        active_commands = self.command_manager.get_active_commands()
        for command_state in active_commands:
            self.command_handlers[command_state]()

    def toggle(self):
        self.light.toggle()
        sleep(0.5)

    def blink(self):
        self.light.blink()

    def on(self):
        self.light.on()

    def off(self):
        self.light.off()
