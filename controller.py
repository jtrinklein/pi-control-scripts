import sys
import time
import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(STEERING_PIN_0, GPIO.OUT)
# GPIO.setup(STEERING_PIN_1, GPIO.OUT)
# GPIO.setup(self.DRIVE_PIN_0, GPIO.OUT)
# GPIO.setup(self.DRIVE_PIN_1, GPIO.OUT)


class Controller:
    DRIVE_FORWARD = 4
    DRIVE_BACKWARD = 2
    DRIVE_STOP = 1
    STEER_LEFT = 32
    STEER_RIGHT = 16
    STEER_STRAIGHT = 8

    STEERING_PIN_0 = 35
    STEERING_PIN_1 = 37

    DRIVE_PIN_0 = 38
    DRIVE_PIN_1 = 40

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STEERING_PIN_0, GPIO.OUT)
        GPIO.setup(self.STEERING_PIN_1, GPIO.OUT)
        GPIO.setup(self.DRIVE_PIN_0, GPIO.OUT)
        GPIO.setup(self.DRIVE_PIN_1, GPIO.OUT)
        self.straight()
        self.stop()

    # Enables step by step checking by wiring some LEDs to those 3 terminals
    def wait_a_key(self):
        print "waiting..."
        raw_input()

    def backward(self):
    	GPIO.output(self.DRIVE_PIN_0, 0)
    	GPIO.output(self.DRIVE_PIN_1, 1)

    def forward(self):
    	GPIO.output(self.DRIVE_PIN_0, 0)
    	GPIO.output(self.DRIVE_PIN_1, 0)

    def stop(self):
    	GPIO.output(self.DRIVE_PIN_0, 1)
    	GPIO.output(self.DRIVE_PIN_1, 0)

    def straight(self):
    	GPIO.output(self.STEERING_PIN_0, 1)
    	GPIO.output(self.STEERING_PIN_1, 0)

    def left(self):
    	GPIO.output(self.STEERING_PIN_0, 0)
    	GPIO.output(self.STEERING_PIN_1, 0)

    def right(self):
    	GPIO.output(self.STEERING_PIN_0, 0)
    	GPIO.output(self.STEERING_PIN_1, 1)


    def move_for_cycle_count(self, cycles, dir):
        if cycles > 1000:
            cycles = 1000

        if (dir & this.DRIVE_BACKWARD) is not 0:
            self.backward()

        if (dir & this.DRIVE_FORWARD) is not 0:
            self.forward()

        if (dir & this.DRIVE_STOP) is not 0:
            self.stop()

        if (dir & this.STEER_LEFT) is not 0:
            self.left()

        if (dir & this.STEER_RIGHT) is not 0:
            self.right()

        if (dir & this.STEER_STRAIGHT) is not 0:
            self.straight()

        while (cycles > 0):
            cycles -= 1

        self.straight()
        self.stop()

if __name__ == "__main__":
    c = Controller()

    while 1:
        print "enter to go forward"
        c.wait_a_key()

        c.forward()
        print "enter to stop"
        c.wait_a_key()

        c.stop()
        print "enter to backward"
        c.wait_a_key()

        c.backward()
        print "enter to stop"
        c.wait_a_key()

        c.stop()
        print "enter to left"
        c.wait_a_key()

        c.left()
        print "enter to stop"
        c.wait_a_key()

        c.straight()
        print "enter to right"
        c.wait_a_key()

        c.right()
        print "enter to stop"
        c.wait_a_key()

        c.straight()
