import pygame
from enum import IntEnum

class Controller:
    def __init__( self ): 
        pygame.joystick.init()
        self.joystick = None
        self.connected = False

    def is_connected(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.connected = True
        else:
            self.joystick = None
            self.connected = False

        return self.connected

    def getAxisState(self, axis):
        return self.joystick.get_axis(axis)

    def getButtonState(self, button):
        return self.joystick.get_button(button)

    def getHatState(self, hat):
        return self.joystick.get_hat(hat)

    class ControllerButtons(IntEnum):
        Y = 0
        B = 1
        A = 2
        X = 3
        L1 = 4
        R1 = 5
        L2 = 6
        R2 = 7
        L3 = 10
        R3 = 11

    class ControllerHats(IntEnum):
        HAT_0 = 0

    class ControllerAnalogs(IntEnum):
        L3X = 0
        L3Y = 1
        R3X = 2
        R3Y = 3

    @staticmethod
    def get_buttons():
        return Controller.ControllerButtons

    @staticmethod
    def get_analogs():
        return Controller.ControllerAnalogs
    
    @staticmethod
    def get_hats():
        return Controller.ControllerHats