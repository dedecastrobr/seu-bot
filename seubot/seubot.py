import os
import sys
from time import sleep
import pygame
from pygame.locals import QUIT
from hardware import Controller, MotorSet, Light
from commands import Command, CommandState, CommandManager
from admin import start_web_server
from utils import get_config, Logger


config = get_config()
logger = Logger(config.get("bot_logfile"))

class SeuBot:

    def __init__(self, name=config.get("bot_name")):
        pygame.init()
        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.gamepad = Controller()

        self.motor_set = MotorSet(self.gamepad)

        self.white_light = Light("white_light")
        self.blue_light = Light("blue_light")
        self.green_light = Light("green_light")
        self.yellow_light = Light("yellow_light")

        self.command_manager = CommandManager(self.get_available_commands())
        self.command_handlers = {
            CommandState.QUIT: self.quit,
            CommandState.PRESSED_A: self.light_show_wave,
            CommandState.PRESSED_X: self.light_show_dance
        }

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self):
        if self.gamepad.is_connected():
            self.motor_set.handle_commands()
            active_commands = self.command_manager.get_active_commands()
            for command_state in active_commands:
                self.command_handlers[command_state]()

    def get_available_commands(self):
        return [
            Command(
                state=CommandState.QUIT,
                condition=lambda button=self.gamepad.get_buttons().R3: (
                    self.gamepad.getButtonState(int(button)) == 1
                )
            ),
            Command(
                state=CommandState.PRESSED_A,
                condition=lambda button=self.gamepad.get_buttons().A: (
                    self.gamepad.getButtonState(int(button)) == 1
                )
            ),
            Command(
                state=CommandState.PRESSED_X,
                condition=lambda button=self.gamepad.get_buttons().X: (
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

    def light_show_wave(self):

        for _ in range(3):
            # Forward wave
            self.white_light.on()
            sleep(0.3)
            self.blue_light.on()
            sleep(0.3)
            self.green_light.on()
            sleep(0.3)
            self.yellow_light.on()
            sleep(0.5)
            
            # Backward wave
            self.yellow_light.off()
            sleep(0.3)
            self.green_light.off()
            sleep(0.3)
            self.blue_light.off()
            sleep(0.3)
            self.white_light.off()
            sleep(0.5)

    def light_show_dance(self):

        # Phase 1: Alternating pairs
        for _ in range(5):
            self.white_light.on()
            self.green_light.on()
            self.blue_light.off()
            self.yellow_light.off()
            sleep(0.2)
            
            self.white_light.off()
            self.green_light.off()
            self.blue_light.on()
            self.yellow_light.on()
            sleep(0.2)
        
        # Phase 2: All lights blink together
        all_lights = [self.white_light, self.blue_light, 
                    self.green_light, self.yellow_light]
        
        for light in all_lights:
            light.off()
        
        for _ in range(4):
            for light in all_lights:
                light.toggle()
            sleep(0.15)
        
        # Phase 3: Sequential blinking
        for light in all_lights:
            light.off()
        
        for light in all_lights:
            light.blink()
            sleep(0.3)
        
        sleep(1)
        
        # Turn everything off at the end
        for light in all_lights:
            light.off()