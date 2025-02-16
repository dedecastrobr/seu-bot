import os
import sys
from time import sleep
import pygame
from pygame.locals import QUIT
from hardware import Controller, MotorSet
from commands import CommandState, CommandManager
from admin import start_web_server
from utils import config, Logger

logger = Logger(config.get("bot_logfile"))

class SeuBot:
    def __init__(self, name=config.get("bot_name")):
        pygame.init()
        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.gamepad = Controller()
        self.gamepad.check_connection()

        self.motor_set = MotorSet()

        self.command_manager = CommandManager(self.gamepad)

        self.command_handlers = {
            CommandState.FORWARD: self.motor_set.move_forward,
            CommandState.BACKWARD: self.motor_set.move_backward,
            CommandState.TURN_LEFT: self.motor_set.turn_left,
            CommandState.TURN_RIGHT: self.motor_set.turn_right,
            CommandState.STOP: self.motor_set.stop,
            CommandState.QUIT: self.quit,
            CommandState.PRESSED_A: start_web_server,
            CommandState.PRESSED_B: self.restart

        }

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self):
        if self.gamepad.connected:
            active_commands = self.command_manager.get_active_commands()
            if not active_commands:
                self.command_handlers[CommandState.STOP]()
                return
            for command_state in active_commands:
                self.command_handlers[command_state]()

    def check_controller(self):
        if not self.gamepad.connected:
            self.gamepad.check_connection()

    def quit(self):
        logger.info(("Quiting!"))
        pygame.event.post(pygame.event.Event(QUIT))

    def restart(self):
        logger.info("Restarting "+ self.name)
        os.execv(sys.executable, ['python'] + sys.argv)
