from dataclasses import dataclass
from enum import Enum
from typing import Callable
from hardware.controller import ControllerButtons, ControllerHats, ControllerAnalogs


class CommandState(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    QUIT = "quit"
    PRESSED_A = "a_button"
    PRESSED_B = "b_button"

@dataclass
class Command:
    state: CommandState
    condition: Callable[[], bool]

class CommandManager:
    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.commands = self._init_commands()
        
    def _init_commands(self) -> list[Command]:
        return [
            Command(
                state=CommandState.FORWARD,
                condition=lambda: self.gamepad.getButtonState(int(ControllerButtons.R2)) == 1
            ),
            Command(
                state=CommandState.BACKWARD,
                condition=lambda: self.gamepad.getButtonState(int(ControllerButtons.L2)) == 1
            ),
            Command(
                state=CommandState.TURN_LEFT,
                condition=lambda: (
                    self.gamepad.getAxisState(int(ControllerAnalogs.L3X)) < 0.0 or 
                    self.gamepad.getHatState(int(ControllerHats.HAT_0))[0] < 0.0
                )
            ),
            Command(
                state=CommandState.TURN_RIGHT,
                condition=lambda: (
                    self.gamepad.getAxisState(int(ControllerAnalogs.L3X)) > 0.005 or 
                    self.gamepad.getHatState(int(ControllerHats.HAT_0))[0] > 0.0
                )
            ),
            Command(
                state=CommandState.QUIT,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.R3)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_A,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.A)) == 1
                    )
            ),
            Command(
                state=CommandState.PRESSED_B,
                    condition=lambda: (
                        self.gamepad.getButtonState(int(ControllerButtons.B)) == 1
                    )
            )
        ]
    
    def get_active_commands(self) -> list[CommandState]:
        return [
            command.state for command in self.commands 
            if command.condition()
        ]