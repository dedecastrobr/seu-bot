import os
import sys
import pygame
from pygame.locals import QUIT
from hardware import Controller, MotorSet, Light
from commands import Command, CommandState, CommandManager
from admin import start_web_server
from utils import config, Logger
from hardware.controller import ControllerButtons

logger = Logger(config.get("bot_logfile"))

class SeuBot:
    def __init__(self, name=config.get("bot_name")):
        pygame.init()
        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.gamepad = Controller()
        self.gamepad.check_connection()

        self.motor_set = MotorSet(self.gamepad)

        self.green_light = Light("green_light")
        self.blue_light = Light("blue_light")
        self.yellow_light = Light("yellow_light")
        self.head_lights = Light("head_lights")

        self.command_manager = CommandManager(self.gamepad, self.get_available_commands())

        self.command_handlers = {
            CommandState.QUIT: self.quit,
            CommandState.PRESSED_A: self.green_light.toggle,
            CommandState.PRESSED_B: self.blue_light.toggle,
            CommandState.PRESSED_X: self.yellow_light.toggle,
            CommandState.PRESSED_Y: self.head_lights.toggle
        }

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self):
        if self.gamepad.connected:
            self.motor_set.handle_commands()
            active_commands = self.command_manager.get_active_commands()
            for command_state in active_commands:
                self.command_handlers[command_state]()


    def get_available_commands(self):
        return [
            Command(
                state=CommandState.QUIT,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.R3)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_A,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.A)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_B,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.B)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_X,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.X)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_Y,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.Y)) == 1
                    )
            )
        ]

    def check_controller(self):
        if not self.gamepad.connected:
            self.gamepad.check_connection()

    def quit(self):
        logger.info(("Quiting!"))
        pygame.event.post(pygame.event.Event(QUIT))

    def restart(self):
        logger.info("Restarting "+ self.name)
        os.execv(sys.executable, ['python'] + sys.argv)
