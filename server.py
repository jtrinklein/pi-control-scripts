# Echo server program
from controller import Controller
import socket, os, re, signal
import RPi.GPIO as GPIO

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
