import sys
import pygame
from pygame.locals import QUIT
from seubot import SeuBot

def main():
    print("Initializing SeuBot..")
    seubot = SeuBot("Ana Bot")
    print("Waiting for joystick commands!")
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
        seubot.are_you_leaving()
        seubot.what_todo()

    print("I hope to see you soon! Bye!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
