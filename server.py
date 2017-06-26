# Echo server program
import socket, os

import RPi.GPIO as GPIO

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


directionalControl = Controller()

directionSwitch = {
    104: directionalControl.backward,
    88: directionalControl.backward,
    100: directionalControl.left,
    83: directionalControl.left,
    102: directionalControl.right,
    85: directionalControl.right,
    98: directionalControl.forward,
    80: directionalControl.forward,
    115: directionalControl.stop
}

sock_name = '/tmp/uv4l.socket'              # Arbitrary non-privileged port
s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
try:
    os.remove(sock_name)
except OSError:
    pass

s.bind(sock_name)
s.listen(1)

while 1:
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break
        directionSwitch[data]()
        conn.sendall(data)
    conn.close()
