import os
import random
import time
import RPi.GPIO as GPIO
import alsaaudio
import wave
import random
import requests
import json
import re
from alexa_client import AlexaClient

#Settings
button = 18 #GPIO Pin with button connected
device = "plughw:1" # Name of your microphone/soundcard in arecord -L

#Setup
recorded = False
servers = ["127.0.0.1:11211"]
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))



def internet_on():
    print "Checking Internet Connection"
    try:
        r =requests.get('https://api.amazon.com/auth/o2/token')
	print "Connection OK"
        return True
    except:
	print "Connection Failed"
    	return False

	


def start():
	alexa = AlexaClient()
	last = GPIO.input(button)
	while True:
		val = GPIO.input(button)
		GPIO.wait_for_edge(button, GPIO.FALLING) # we wait for the button to be pressed
		inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)
		inp.setchannels(1)
		inp.setrate(16000)
		inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		inp.setperiodsize(500)
		audio = ""
		while(GPIO.input(button)==0): # we keep recording while the button is pressed
			l, data = inp.read()
			if l:
				audio += data
		rf = open(path+'recording.wav', 'w')
		rf.write(audio)
		rf.close()
		inp = None
        	alexa.ask(path+'recording.wav', save_to=path+"response.mp3")
		os.system('mpg123 -q {}1sec.mp3 {}response.mp3 {}1sec.mp3'.format(path, path, path))
			

	

if __name__ == "__main__":
	GPIO.setwarnings(False)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	while internet_on() == False:
		print "."
	os.system('mpg123 -q {}1sec.mp3 {}hello.mp3'.format(path, path))
	start()
