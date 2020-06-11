import RPi.GPIO as GPIO
from Adafruit_IO import*
import time
GPIO.setmode(GPIO.BOARD)

#Adafruit IO

ADAFRUIT_IO_USERNAME = 'adanew_3'
ADAFRUIT_IO_KEY = 'aio_wYpY96G3mVaUJLXBI3OY3M0JGSsH'
aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
try:
    ldrtest = aio.feeds('ldrtest')
except RequestError:
    ldrtest_feed = Feed(name='ldrtest')
    ldrtest_feed = aio.create_feed(ldrtest_feed)

#define the pin that goes to the circuit
pin_to_circuit = 7

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while True:
        time.sleep(1)
        value=rc_time(pin_to_circuit)
        print(value)
        if ( value <= 10000 ):
                aio.send('ldrtest',value)
        elif (value > 10000):
                aio.send('ldrtest',value)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
