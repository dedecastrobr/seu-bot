import sys
import pygame
from pygame.locals import QUIT
from seubot import SeuBot
from utils import config, Logger

logger = Logger(config.get("bot_logfile"))

def main():
    logger.info("Initializing SeuBot..")
    seubot = SeuBot()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
        seubot.what_todo()

    logger.info("I hope to see you soon! Bye!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
