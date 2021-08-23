import os 
import time
import random
import serial
import struct 
import ssl

import sys 
import urllib 
import requests
import smbus 
from ctypes import c_short

import RPi.GPIO as GPIO
import datetime
from datetime import datetime
from time import sleep 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)	
GPIO.setup(21,GPIO.OUT)	
GPIO.setup(26,GPIO.OUT)	



ser = serial.Serial()
ser.baudrate = 9600 
ser.port = '/dev/ttyUSB0' 

fd = open("DataofControlSystemTemHumLight_2.csv", 'a+')
fd.write("Date,Time,Temperature,Humidity,PPFD\n")
fd.close()

#Turn ON Lights at 6AM and OFF at 8PM
on_time = time.strftime('%H:%M', time.gmtime(((6 * 60 + 0) * 60))) 
off_time = time.strftime('%H:%M', time.gmtime(((20 * 60 + 0) * 60)))


while True:
    fd = open("DataofControlSystemTemHumLight_2.csv", 'a+')
    try:
        ser.open()
        time.sleep(60)           
        raw_data = ser.readline()
        data = raw_data.decode('utf-8').strip()
        timestamp = time.ctime()
        tdate = (timestamp[0:10])
        ttime = (timestamp[11:19])
        print (tdate+ttime+","+data)
        print (tdate+ttime+","+data, file=fd)
           
    except:
        data = "50,90,90,"
        time.sleep(60)           
        timestamp = time.ctime()
        print (tdate+ttime+","+data)
        print (tdate+ttime+","+data, file=fd)
        
    fd.close()        
    temperature, humidity, ppfd, x= data.split(",")
    tempc = float (temperature)
    humc = float(humidity)
    ppfdc = float(ppfd)
    
           
# Turn ON and OFF lights
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
                      
#if current_time >= on_time and current_time <= off_time:
    if current_time>= on_time and current_time <= off_time:
        
        GPIO.output(16,GPIO.HIGH)
        if tempc < 25.0:
            GPIO.output(26,GPIO.HIGH)
        else:
            GPIO.output(26,GPIO.LOW)
    else:
        GPIO.output(16,GPIO.LOW)
           
#if current_time >= on_time and current_time <= off_time:
#GPIO.output(16,GPIO.LOW) 
                
# Turn ON and OFF fan
    if tempc >= 25.0:
        
        GPIO.output(21,GPIO.HIGH)
    else:
        GPIO.output(21,GPIO.LOW)
            

# Turn ON and OFF heater

    if tempc<= 15.0:  
        GPIO.output(26,GPIO.HIGH)
         
    ser.close()
        
