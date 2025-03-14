import pygame
from pygame.locals import *
from seubot import SeuBot
from utils import get_config, Logger

config = get_config()
logger = Logger(config.get("bot_logfile"))

def main():
    logger.info("Initializing SeuBot..")
    pygame.init()
    pygame.joystick.init()

    seubot = SeuBot()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        pygame.event.pump()
        events = pygame.event.get()
        seubot.what_todo(events)

if __name__ == "__main__":
    main()
