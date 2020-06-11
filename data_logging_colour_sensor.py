from Adafruit_IO import*
from queue import Queue
import RPi.GPIO as GPIO
import time

ADAFRUIT_IO_USERNAME = 'adanew_3'
ADAFRUIT_IO_KEY = 'aio_wYpY96G3mVaUJLXBI3OY3M0JGSsH'
aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
try:
    counttest = aio.feeds('counttest')
except RequestError:
    counttest = Feed(name='counttest')
    counttest = aio.create_feed(counttest_feed)

#Red Queue
red_start_q = Queue(maxsize=10)
red_end_q = Queue(maxsize=10)
red_no=1

#Blue Queue
blue_start_q = Queue(maxsize=10)
blue_end_q = Queue(maxsize=10)
blue_no=1

'''
#Green
green_start_q = Queue(maxsize=10)
green_end_q = Queue(maxsize=10)
green_no=1
'''

#Colour Sensor Config
Sensor2_s2 = 27
Sensor2_s3 = 22
Sensor2_sig2 = 17
Sensor1_s2 = 23
Sensor1_s3 = 24
Sensor1_sig1 = 25
NUM_CYCLES = 10

#Color Sensor Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Sensor1_sig1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Sensor2_sig2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Sensor1_s2,GPIO.OUT)
GPIO.setup(Sensor1_s3,GPIO.OUT)
GPIO.setup(Sensor2_s2,GPIO.OUT)
GPIO.setup(Sensor2_s3,GPIO.OUT)
  

try:
    
    while True:
        
        #Sensor 1
        #Red
        GPIO.output(Sensor1_s2,GPIO.LOW)
        GPIO.output(Sensor1_s3,GPIO.LOW)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(Sensor1_sig1, GPIO.FALLING)
        duration = time.time() - start 
        red  = NUM_CYCLES // duration
        
        #Blue
        GPIO.output(Sensor1_s2,GPIO.LOW)
        GPIO.output(Sensor1_s3,GPIO.HIGH)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
          GPIO.wait_for_edge(Sensor1_sig1, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES // duration
    
        #Green
        """GPIO.output(Sensor1_s2,GPIO.HIGH)
        GPIO.output(Sensor1_s3,GPIO.HIGH)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
          GPIO.wait_for_edge(Sensor1_sig1, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES // duration"""
    
  
        #SENSOR 2
  
        #Red
        GPIO.output(Sensor2_s2,GPIO.LOW)
        GPIO.output(Sensor2_s3,GPIO.LOW)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
          GPIO.wait_for_edge(Sensor2_sig2, GPIO.FALLING)
        duration = time.time() - start 
        red2  = NUM_CYCLES // duration
        
        #Blue
        GPIO.output(Sensor2_s2,GPIO.LOW)
        GPIO.output(Sensor2_s3,GPIO.HIGH)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
          GPIO.wait_for_edge(Sensor2_sig2, GPIO.FALLING)
        duration = time.time() - start
        blue2 = NUM_CYCLES // duration
        
        #Green
        """GPIO.output(Sensor2_s2,GPIO.HIGH)
        GPIO.output(Sensor2_s3,GPIO.HIGH)
        time.sleep(0.2)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
          GPIO.wait_for_edge(Sensor2_sig2, GPIO.FALLING)
        duration = time.time() - start
        green2 = NUM_CYCLES // duration"""
    
        if red > 29000 :
            print("Sensor1: Red Starts")
            time.sleep(0.5)
            starttime=time.perf_counter()
            red_start_q.put(starttime)
        elif red2>17000:
            time.sleep(0.5)
            endtime=time.perf_counter()
            print("Sensor1: Red {} Ends".format(red_no))
            red_end_q.put(endtime)
            red_stime=red_start_q.get()
            red_etime=red_end_q.get()
            red_ttime=red_etime-red_stime
            print("Time: {}".format(red_ttime))
            if red_ttime>15:
                aio.send('counttest',"Red {}".format(red_no))
            red_no+=1
        elif blue > 24000 :
            print("Sensor1: Blue Starts")
            time.sleep(0.5)
            starttime=time.perf_counter()
            blue_start_q.put(starttime)
        elif blue2>24000:
            time.sleep(0.5)
            endtime=time.perf_counter()
            print("Sensor1: Blue {} Ends".format(blue_no))
            blue_end_q.put(endtime)
            blue_stime=blue_start_q.get()
            blue_etime=blue_end_q.get()
            blue_ttime=blue_etime-blue_stime
            print("Time: {}".format(blue_ttime))
            if blue_ttime>15:
                aio.send('counttest',"Blue {}".format(blue_no))
            blue_no+=1
        
except KeyboardInterrupt:
    GPIO.cleanup()
