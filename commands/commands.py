from dataclasses import dataclass
from enum import Enum
from typing import Callable

class CommandState(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    QUIT = "quit"
    PRESSED_A = "a_button"
    PRESSED_B = "b_button"
    PRESSED_X = "x_button"
    PRESSED_Y = "y_button"
    PRESSED_R1 = "R1_button"

@dataclass
class Command:
    state: CommandState
    condition: Callable[[], bool]

class CommandManager:
    def __init__(self, commands):
        self.commands = commands
    
    def get_active_commands(self) -> list[CommandState]:
        return [
            command.state for command in self.commands 
            if command.condition()
        ]