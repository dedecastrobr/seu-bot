import os
import sys
from time import sleep
import pygame
from pygame.locals import QUIT
from hardware import Controller, MotorSet, Light
from commands import Command, CommandState, CommandManager
from admin import start_web_server
from utils import config, Logger

logger = Logger(config.get("bot_logfile"))

class SeuBot:

    def __init__(self, name=config.get("bot_name")):
        pygame.init()
        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.gamepad = Controller()

        self.motor_set = MotorSet(self.gamepad)

        self.green_light_commands = [
            {
                "state": CommandState.PRESSED_X, 
                "controller": self.gamepad.get_buttons().X,
                "method": "on"
            },
            {
                "state": CommandState.PRESSED_Y, 
                "controller": self.gamepad.get_buttons().Y, 
                "method": "off"
            },
            {
                "state": CommandState.PRESSED_R1, 
                "controller": self.gamepad.get_buttons().R1, 
                "method": "blink"
            },
        ]
        self.green_light = Light("green_light", self.gamepad, self.green_light_commands)

        self.yellow_light = Light("yellow_light")

        self.command_manager = CommandManager(self.get_available_commands())
        self.command_handlers = {
            CommandState.QUIT: self.quit
        }

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self):
        if self.gamepad.is_connected():
            self.motor_set.handle_commands()
            self.green_light.handle_commands()
            active_commands = self.command_manager.get_active_commands()
            self.yellow_light.on()
            for command_state in active_commands:
                self.command_handlers[command_state]()
        else:
            self.yellow_light.off()


    def get_available_commands(self):
        return [
            Command(
                state=CommandState.QUIT,
                    condition=lambda button=self.gamepad.get_buttons().R3: (
                        self.gamepad.getButtonState(int(button)) == 1
                    )
            )
        ]

    def quit(self):
        logger.info(("Quiting!"))
        sleep(0.5)
        pygame.event.post(pygame.event.Event(QUIT))

    def restart(self):
        logger.info("Restarting "+ self.name)
        os.execv(sys.executable, ['python'] + sys.argv)
