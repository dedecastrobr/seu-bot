from gpiozero import Motor
from utils import config

class MotorSet:

    def __init__(self):
        right_config = config.get("gpio").get("motors").get("right_motor")
        self.right_motor = Motor(forward=right_config.get("forward_pin"),
                                 backward=right_config.get("backward_pin"),
                                 pwm=False)
        
        left_config = config.get("gpio").get("motors").get("left_motor")
        self.left_motor =  Motor(forward=left_config.get("forward_pin"),
                                 backward=left_config.get("backward_pin"),
                                 pwm=False)
        
    def move_forward(self):
        self.right_motor.forward()
        self.left_motor.forward()

    def move_backward(self):
        self.right_motor.backward()
        self.left_motor.backward()

    def turn_right(self):
        self.right_motor.value = 0

    def turn_left(self):
        self.left_motor.value = 0

    def stop(self):
        self.right_motor.stop()
        self.left_motor.stop()
           

