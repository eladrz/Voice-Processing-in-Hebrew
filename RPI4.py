import socket
import threading
import RPi.GPIO as GPIO
import time

Led = 0
GLed = 0
RLed = 0
delay = 0.1
redPin = 8
greenPin = 37
ledpin = 38
buttonpin = 40
button_state = 1
button_state_old = 1

GPIO.setmode(GPIO.BOARD)
# set the white led
GPIO.setup(ledpin, GPIO.OUT)
GPIO.output(ledpin, Led)
GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# set the red led
GPIO.setup(redPin, GPIO.OUT)
GPIO.output(redPin, RLed)
# set the green led
GPIO.setup(greenPin, GPIO.OUT)
GPIO.output(greenPin, GLed)

listWhite = ['white', 'white boy']
listRed = ['red', 'adum', 'red!']
listGreen = ['green', 'yalok', 'yelong', 'yabok', 'green!', 'yogh!']
listCheck = ['test', 'Nahon Army', 'condition of the bulbs.', 'check out',
             'sweetness', 'alkki hart', 'check', 'checking', 'c', 'examination']
listOnAll = ['good morning', 'on', 'buki atuv']
listOffAll = ['', 'cowgirl', 'check him out', 'already a voice', 'hulk crutches',
              'turn all off', 'turn it all off', 'off', 'good night', 'laila', 'night', 'turn it all off!']
stateD = []
buffer = 1024
ServerPort = 2224
# ServerIP = '192.168.1.125'
ServerIP = '192.168.68.226'
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((ServerIP, ServerPort))
error = '-1'


def sock():
    global Led
    global RLed
    global GLed
    while True:
        message, address = RPIsocket.recvfrom(buffer)
        message = message.decode('utf-8')
        if message in listCheck:
            stateD.clear()
            stateD.append(str(Led))
            stateD.append(str(RLed))
            stateD.append(str(GLed))
            state = [str(item) for item in stateD]
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        elif message in listWhite:
            Led = not Led
            GPIO.output(ledpin, Led)
            stateD.clear()
            stateD.append(str(Led))
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        elif message in listRed:
            RLed = not RLed
            GPIO.output(redPin, RLed)
            stateD.clear()
            stateD.append(str(RLed))
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        elif message in listGreen:
            GLed = not GLed
            GPIO.output(greenPin, GLed)
            stateD.clear()
            stateD.append(str(GLed))
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        elif message in listOnAll:
            Led = 1
            RLed = 1
            GLed = 1
            GPIO.output(ledpin, Led)
            GPIO.output(redPin, RLed)
            GPIO.output(greenPin, GLed)
            stateD.clear()
            stateD.append(str(Led))
            stateD.append(str(RLed))
            stateD.append(str(GLed))
            state = [str(item) for item in stateD]
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        elif message in listOffAll:
            Led = 0
            RLed = 0
            GLed = 0
            GPIO.output(ledpin, Led)
            GPIO.output(redPin, RLed)
            GPIO.output(greenPin, GLed)
            stateD.clear()
            stateD.append(str(Led))
            stateD.append(str(RLed))
            stateD.append(str(GLed))
            state = [str(item) for item in stateD]
            state = str(stateD).encode('utf-8')
            RPIsocket.sendto(state, address)
        else:
            state = str(error).encode('utf-8')
            RPIsocket.sendto(state, address)
        print(f"Client address {address[0]} from port {address[1]}")
        time.sleep(0.1)


threadSocket = threading.Thread(target=sock)
try:
    threadSocket.start()
    while True:
        button_state = GPIO.input(buttonpin)
        if button_state == 0 and button_state_old == 1:
            Led = not Led
            GPIO.output(ledpin, Led)
        button_state_old = button_state
        time.sleep(delay)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO clean seccessfully")
