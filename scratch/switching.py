import sys
import time
import RPi.GPIO as GPIO

def sleep(a = 0.1):
    time.sleep(a)

LEFT_PIN = 35
RIGHT_PIN = 37

REVERSE_PIN = 38
SWITCH_PIN = 40

# Enables step by step checking by wiring some LEDs to those 3 terminals
def wait_a_key():
    print "waiting..."
    raw_input()

def go_backwards():
	GPIO.output(REVERSE_PIN, 0)
	GPIO.output(SWITCH_PIN, 1)

def go_forwards():
	GPIO.output(REVERSE_PIN, 0)
	GPIO.output(SWITCH_PIN, 0)

def stop():
	GPIO.output(REVERSE_PIN, 1)
	GPIO.output(SWITCH_PIN, 0)

def straight():
	GPIO.output(LEFT_PIN, 1)
	GPIO.output(RIGHT_PIN, 0)

def left():
	GPIO.output(LEFT_PIN, 0)
	GPIO.output(RIGHT_PIN, 0)

def right():
	GPIO.output(LEFT_PIN, 0)
	GPIO.output(RIGHT_PIN, 1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEFT_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PIN, GPIO.OUT)
GPIO.setup(REVERSE_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.OUT)

stop()
straight()


print "Setup complete..."
wait_a_key()

#GPIO.output(REVERSE_PIN, 0)
#print "reverse off!"
#wait_a_key()


#GPIO.output(REVERSE_PIN, 1)
#print "reverse on!"
#wait_a_key()
while True:
	#stop()
	#print "stopped!"
	straight()
	print "straight!"
	wait_a_key()

	#go_forwards()
	#print "forward!"
	left()
	print "left!"
	wait_a_key()

	#stop()
	#print "stopped!"
	straight()
	print "straight!"
	wait_a_key()
	
	#go_backwards()
	#print "backward!"
	right()
	print "right!"
	wait_a_key()

GPIO.cleanup()
