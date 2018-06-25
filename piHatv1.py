#!/usr/bin/env python
import time
import serial
import RPi.GPIO as GPIO

import requests
import json

#pushbullet api key
API_KEY = 'pushbulletapikey'

ser = serial.Serial(
 port = '/dev/ttyUSB0',
 baudrate = 9600,
 parity = serial.PARITY_NONE,
 stopbits = serial.STOPBITS_ONE,
 bytesize = serial.EIGHTBITS,
 timeout = 1
)
counter=0

statusPin = 8
warningPin = [3,5,7]
buzzerPin = 10
sev_low = [1,0,0]
sev_mid = [1,1,0]
sev_high = [1,1,1]
sev_clear=[0,0,0]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(statusPin, GPIO.OUT)
for pin in warningPin:
    GPIO.setup(pin,GPIO.OUT)
GPIO.setup(buzzerPin,GPIO.OUT)

def severity_warning(sev_level):
        for x in range (0,3):
            GPIO.output(warningPin[x],sev_level[x])
        if sev_level[2] == 1:
            GPIO.output(buzzerPin, 1)
        else:
            GPIO.output(buzzerPin, 0)
            
def aq_status(aqstat):
    if aqstat == False:
        GPIO.output(statusPin,1)
    else:
        GPIO.output(statusPin,0)
        
def pushMessage(title, body):
    data = {
        'type':'note', 
        'title':title,
        'body':body
        }
    resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))

def dangerNotif(type):
    pushMessage("Warning", "Dude, your " +str(type)+ " is abnormal, check your hat lights for details.")
    
def doomNotif(type):
    pushMessage("Impending Doom", "Wherever you are, get out of there. The "+str(type)+" is so bad.")
    
while 1:
 counter = counter + 1
 time.sleep(2)
 #print(counter)
 x = ser.readline()
 #print(x)
 '''
 if len(x) == 6:
     UVval = float(x);
     print("UV: " + str(UVval))
 elif len(x) == 5:
     aq = int(x);
     print("aq: " + str(aq))
 else:
     print("yo")
'''
 if counter%3 == 1:
     UVval = float(x);
     if UVval >= 50:
         counter = counter - 1
     else:
      print("UV: " + str(UVval))
     aq_status(False)
     if UVval >= 5 and UVval < 7:
      severity_warning(sev_low)
     elif UVval >= 7 and UVval < 9:
      severity_warning(sev_mid)
      dangerNotif("UV level")
     elif UVval >= 9 and UVval < 11:
      severity_warning(sev_high)
      doomNotif("UV level")
     else:
      print("UV ok")
      severity_warning(sev_clear)
 elif counter%3 == 2:
     aq = int(x);
     print("aq: " + str(aq))
     aq_status(True)
     if aq >= 700 and aq < 1500:
      severity_warning(sev_low)
     elif aq >= 1500 and aq < 3000:
      severity_warning(sev_mid)
      dangerNotif("air quality")
     elif aq >= 3000:
      severity_warning(sev_high)
      doomNotif("air quality")
     else:
      print("aq ok")
      severity_warning(sev_clear)
 else:
     print()
     if counter%30 == 0:
         pushMessage("Hat Update", "Yo, I'm your hat. The UV level right now is " + str(UVval) + ", and the air quality sensors value is "+str(aq))
         print("Push notification sent!")
        



