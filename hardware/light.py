from gpiozero import LED
from utils import get_config, Logger
from time import sleep
from commands import CommandManager, Command

logger = Logger(get_config().get("bot_logfile"))

class Light:

    def __init__(self, name, pin, gamepad=None, light_commands=[]):
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

        if gamepad:
            try:
                self.gamepad = gamepad
                self.light_commands = light_commands
                self.command_manager = CommandManager(self.get_available_commands())
                self.command_handlers = {
                    cmd["state"]: getattr(self, cmd["method"], self.invalid_method)
                    for cmd in self.light_commands
                }
            except Exception as e:
                raise RuntimeError(f"Error initializing gamepad commands for {self.name}: {e}") from e

    def invalid_method(self):
        logger.error(f"Invalid method in command handlers for {self.name}")
        raise RuntimeError(f"Invalid method in command handlers for {self.name}")

    def get_available_commands(self):
        return [
            Command(
                state=cmd["state"],
                condition=lambda btn=cmd["controller"]: self.gamepad.getButtonState(btn) == 1
            )
            for cmd in self.light_commands
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
