import os
import sys
from time import sleep, time
import pygame
from pygame.locals import *
from admin.admin import is_alive
from hardware import MotorSet, Light
from admin import start_web_server
from utils import get_config, Logger


config = get_config()
logger = Logger(config.get("bot_logfile"))

class SeuBot:

    def __init__(self, name=config.get("bot_name")):
        pygame.init()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        logger.info(f"Found {joystick_count} joystick(s)")
        if joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            logger.info(f"Initialized joystick: {self.joystick.get_name()}")

        self.name = name
        logger.info(("Hello! My name is " + self.name + ". :)"))

        self.motor_set = MotorSet()

        lights_config = config.get("gpio").get("service_lights")      
        self.lights = self.initialize_lights(lights_config)
        self.lights.get("seubot_green_light").on()

        if config.get("enable_admin"):
            start_web_server()

    def what_todo(self, events):
        for event in events:
            logger.debug(f"Event: {event}")

            if event.type == JOYDEVICEADDED:
                logger.info(f"Joystick added!")
                if not hasattr(self, 'joystick'):
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                logger.info("Initialized Controller: " + self.joystick.get_name())

            elif event.type == JOYDEVICEREMOVED:
                logger.info(f"Joystick removed!")
                if hasattr(self, 'joystick'):
                    del self.joystick

            elif event.type == JOYBUTTONDOWN and event.button == 11:
                self.quit()

            elif event.type == JOYBUTTONDOWN and event.button == 10:
                self.restart()

            elif event.type == JOYBUTTONDOWN and event.button == 7:
                self.motor_set.move_forward()

            elif event.type == JOYBUTTONDOWN and event.button == 6:
                self.motor_set.move_backward()

            elif event.type == JOYBUTTONUP and event.button in [6,7]:
                if pygame.event.poll().type != JOYHATMOTION:
                    self.motor_set.stop()

            elif event.type == JOYHATMOTION:
                if event.hat == 0:
                    if event.value == (1, 0):
                        self.motor_set.turn_right()
                    elif event.value == (-1, 0):
                        self.motor_set.turn_left()
                    elif event.value == (0, 0):
                        event = pygame.event.get()
                        logger.debug(f"Event type: {event}")
                        if pygame.event.poll().type != JOYBUTTONDOWN:
                            self.motor_set.stop()                

            elif event.type == KEYDOWN:
                logger.info(f"KEYDOWN: {event.key}")

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

    
    def initialize_lights(self, lights_config):
        lights = {}
        for light_name, pin in lights_config.items():
            lights[light_name] = Light(light_name, pin)
        return lights

    def quit(self):
        logger.info("Quiting! I hope to see you soon! Bye!")
        self.lights.get("seubot_green_light").off()
        sleep(0.5)
        pygame.quit()
        sys.exit()

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