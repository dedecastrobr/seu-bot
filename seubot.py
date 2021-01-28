import time
import datetime
import pygame
import names
from pygame.locals import QUIT
from controller import Controller, ControllerButtons, ControllerHats, ControllerAnalogs

class SeuBot:
    def __init__(self, name=names.get_full_name()):
        pygame.init()
        self.name = name
        print("Hello! My name is " + self.name + ". :)")
        self.gamepad = Controller()

    def move_forward(self):
        print(str(datetime.datetime.now()) + " Moving forward!")

    def move_backward(self):
        print(str(datetime.datetime.now()) + " Moving backward!")

    def turn_left(self):
        print(str(datetime.datetime.now()) + " Turning left!")
           
    def turn_right(self):
        print(str(datetime.datetime.now()) + " Turning right!")

    def are_you_leaving(self):
        if self.gamepad.getButtonState(int(ControllerButtons.R3)) == 1:
            pygame.event.post(pygame.event.Event(QUIT))

    def what_todo(self):
        if self.gamepad.getButtonState(int(ControllerButtons.R2)) == 1:
            self.move_forward()
        if self.gamepad.getButtonState(int(ControllerButtons.L2)) == 1:
            self.move_backward()
        if self.gamepad.getAxisState(int(ControllerAnalogs.L3X)) < 0.0 or self.gamepad.getHatState(int(ControllerHats.HAT_0))[0] < 0.0:
            self.turn_left()
        if self.gamepad.getAxisState(int(ControllerAnalogs.L3X)) > 0.005 or self.gamepad.getHatState(int(ControllerHats.HAT_0))[0] > 0.0:
            self.turn_right()

    def bot_state(self):
        print(datetime.datetime.now())
        print( "Gamepads: " + str(pygame.joystick.get_count()))
        print( "L2: " + str(self.gamepad.getButtonState(int(ControllerButtons.L2))))
        print( "R2: " + str(self.gamepad.getButtonState(int(ControllerButtons.R2))))
        print( "Hat: " + str(self.gamepad.getHatState(int(ControllerHats.HAT_0))))
        print( "L3x: " + str(self.gamepad.getAxisState(int(ControllerAnalogs.L3X))))
        print( "L3y: " + str(self.gamepad.getAxisState(int(ControllerAnalogs.L3Y))))
        print( "R3x: " + str(self.gamepad.getAxisState(int(ControllerAnalogs.R3X))))
        print( "R3y: " + str(self.gamepad.getAxisState(int(ControllerAnalogs.R3Y))))
