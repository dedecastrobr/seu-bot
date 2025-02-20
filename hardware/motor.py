from time import sleep
from gpiozero import Motor
from utils import config, Logger
from commands import Command, CommandState, CommandManager


logger = Logger("bot_logs")

class MotorSet:

    def __init__(self, gamepad):

        self.gamepad = gamepad

        right_config = config.get("gpio").get("motors").get("right_motor")
        self.right_motor = Motor(forward=right_config.get("forward_pin"),
                                 backward=right_config.get("backward_pin"),
                                 pwm=False)
        left_config = config.get("gpio").get("motors").get("left_motor")
        self.left_motor =  Motor(forward=left_config.get("forward_pin"),
                                 backward=left_config.get("backward_pin"),
                                 pwm=False)

        self.command_manager = CommandManager(self.get_available_commands())
        self.command_handlers = {
            CommandState.FORWARD: self.move_forward,
            CommandState.BACKWARD: self.move_backward,
            CommandState.TURN_LEFT: self.turn_left,
            CommandState.TURN_RIGHT: self.turn_right,
            CommandState.STOP: self.stop
        }

    def get_available_commands(self):
        return [
            Command(
                state=CommandState.FORWARD,
                condition=lambda: self.gamepad.getButtonState(int(self.gamepad.get_buttons().R2)) == 1
            ),
            Command(
                state=CommandState.BACKWARD,
                condition=lambda: self.gamepad.getButtonState(int(self.gamepad.get_buttons().L2)) == 1
            ),
            Command(
                state=CommandState.TURN_LEFT,
                condition=lambda: (
                    self.gamepad.getAxisState(int(self.gamepad.get_analogs().L3X)) < 0.0 or 
                    self.gamepad.getHatState(int(self.gamepad.get_hats().HAT_0))[0] < 0.0
                )
            ),
            Command(
                state=CommandState.TURN_RIGHT,
                condition=lambda: (
                    self.gamepad.getAxisState(int(self.gamepad.get_analogs().L3X)) > 0.005 or 
                    self.gamepad.getHatState(int(self.gamepad.get_hats().HAT_0))[0] > 0.0
                )
            )
        ]

    def handle_commands(self):
        active_commands = self.command_manager.get_active_commands()
        if not active_commands:
            self.command_handlers[CommandState.STOP]()
            return
        
        for command_state in active_commands:
            self.command_handlers[command_state]()
        
    def move_forward(self):
        self.right_motor.forward()
        self.left_motor.forward()

    def move_backward(self):
        self.right_motor.backward()
        self.left_motor.backward()

    def turn_right(self):
        self.left_motor.forward()
        self.right_motor.backward()
        sleep(0.5)

    def turn_left(self):
        self.right_motor.forward()
        self.left_motor.backward()
        sleep(0.5)

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()
           

