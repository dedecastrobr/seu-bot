import os
import sys
from time import sleep, time
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

        lights_config = config.get("gpio").get("service_lights")      
        self.lights = self.initialize_lights(lights_config)
        self.lights.get("seubot_green_light").on()

        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.gamepad = Controller()
        self.motor_set = MotorSet(self.gamepad)

        self.command_manager = CommandManager(self.get_available_commands())
        self.command_handlers = {
            CommandState.QUIT: self.quit,


        }

        self.last_health_check = 0
        self.health_check_interval = 10  # seconds

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self):
        if self.gamepad.is_connected():
            self.lights.get("controller_blue_light").on()
            self.motor_set.handle_commands()
            active_commands = self.command_manager.get_active_commands()
            for command_state in active_commands:
                self.command_handlers[command_state]()
        else:
            self.lights.get("controller_blue_light").off()

    def check_admin_service(self):
        current_time = time()
        if current_time - self.last_health_check >= self.health_check_interval:
            try:
                service_light = self.lights.get("service_yellow_light")
                admin_status = is_alive()
                if admin_status:
                    service_light.on()
                else:
                    service_light.off()
            except Exception as e:
                logger.error(f"Service health check error: {e}")
            self.last_health_check = current_time

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
            )
        ]
    
    def initialize_lights(self, lights_config):
        lights = {}
        for light_name, pin in lights_config.items():
            lights[light_name] = Light(light_name, pin)
        return lights

    def quit(self):
        logger.info(("Quiting!"))
        self.lights.get("seubot_green_light").off()
        sleep(0.5)
        pygame.event.post(pygame.event.Event(QUIT))

    def restart(self):
        logger.info("Restarting "+ self.name)
        os.execv(sys.executable, ['python'] + sys.argv)

    def light_show_wave(self):
        for _ in range(3):
            for light in self.lights.values():
                # Forward wave
                light.on()
                sleep(0.3)
            
            for light in self.lights.values():
                # Forward wave
                light.off()
                sleep(0.3)