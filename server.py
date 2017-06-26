# Echo server program
import socket, os, re, signal

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

def stop_all():
    directionalControl.stop()
    directionalControl.straight()

def back_left():
    directionalControl.backward()
    directionalControl.left()

def back_straight():
    directionalControl.backward()
    directionalControl.straight()

def back_right():
    directionalControl.backward()
    directionalControl.right()

def forward_left():
    directionalControl.forward()
    directionalControl.left()

def forward_straight():
    directionalControl.forward()
    directionalControl.straight()

def forward_right():
    directionalControl.forward()
    directionalControl.right()

directionSwitch = {
    '0': stop_all,
    '6': stop_all,          #numpad 5
    '5': directionalControl.left, #numpad 4
    '7': directionalControl.right,#numpad 6
    '2': back_left,         #numpad 1
    '3': back_straight,     #numpad 2
    '4': back_right,        #numpad 3
    '8': forward_left,      #numpad 7
    '9': forward_straight,  #numpad 8
    '10': forward_right,    #numpad 9
    '104': directionalControl.backward,
    '88': directionalControl.backward,
    '100': directionalControl.left,
    '83': directionalControl.left,
    '102': directionalControl.right,
    '85': directionalControl.right,
    '98': directionalControl.forward,
    '80': directionalControl.forward,
    '103': directionalControl.forward,
    '108': directionalControl.backward,
    '105': directionalControl.left,
    '106': directionalControl.right,
    '31': directionalControl.stop,
    '20': directionalControl.straight,
    '115': directionalControl.stop
}


def get_motion_fn(data):
    searchStr = data

    if not searchStr:
        searchStr = '0'

    match = re.search('\d+', data)
    keycode = '0'

    if match:
        keycode = match.group(0)

    fn = stop_all

    if keycode in directionSwitch:
        fn = directionSwitch[keycode]

    print "data: {0} keycode: {1} function: {2}".format(data, keycode, fn.__name__)

    return fn


sock_name = '/tmp/uv4l.socket'              # Arbitrary non-privileged port

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)

try:
    os.remove(sock_name)
except OSError:
    pass

s.bind(sock_name)
s.listen(1)

run = True

def signal_handler(signal, frame):
    global run
    run = False
    print 'closing server...'

signal.signal(signal.SIGINT, signal_handler)

while run:
    conn, addr = s.accept()

    while run:
        data = None
        try:
            data = conn.recv(1024)
        except socket.error as serr:
            break

        if not data: break
        print data

        fn = get_motion_fn(data)
        conn.sendall(fn.__name__)

        if not fn:
            directionalControl.stop()
            directionalControl.straight()
            print "{0} was not a handled keycode".format(data)
        else:
            fn()

    conn.close()

print "cleaning up..."
GPIO.cleanup()
