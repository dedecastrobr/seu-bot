from gpiozero import Motor
from utils import get_config, Logger

logger = Logger("bot_logs")

class MotorSet:

    def __init__(self):

        try:
            self.config = get_config()
            right_config = self.config.get("gpio").get("motors").get("right_motor")
            self.right_motor = Motor(forward=right_config.get("forward_pin"),
                                     backward=right_config.get("backward_pin"),
                                     pwm=False)
            left_config = self.config.get("gpio").get("motors").get("left_motor")
            self.left_motor = Motor(forward=left_config.get("forward_pin"),
                                    backward=left_config.get("backward_pin"),
                                    pwm=False)
        except KeyError as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Error initializing motors: {e}") from e
        
    def move_forward(self):
        self.right_motor.forward()
        self.left_motor.forward()

    def move_backward(self):
        self.right_motor.backward()
        self.left_motor.backward()

    def turn_right(self):
        self.left_motor.forward()
        self.right_motor.backward()

    def turn_left(self):
        self.right_motor.forward()
        self.left_motor.backward()

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()


