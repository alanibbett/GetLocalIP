import os
import socket
import RPi.GPIO as GPIO
import time


redPin = 27
greenPin = 22

if os.name != "nt":
    import fcntl
    import struct
    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', bytes(ifname[:15]))
                # Python 2.7: remove the second argument for the bytes call
            )[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    #print ("Get Host Name = ") + ip
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
        for ifname in interfaces:
            try:
		#print("Trying : ") + ifname
                ip = get_interface_ip(ifname)
                break;
            except IOError:
                pass
    return ip


def toggleLEDs(delay,speed):
	startTime = time.time()
	curTime = startTime
	while curTime < (startTime + delay):
		curTime = time.time()
		GPIO.output(greenPin,GPIO.HIGH)
		GPIO.output(redPin,GPIO.LOW)
		time.sleep(speed/2)
                GPIO.output(greenPin,GPIO.LOW)
                GPIO.output(redPin,GPIO.HIGH)
		time.sleep(speed/2)

        GPIO.output(greenPin,GPIO.LOW)
        GPIO.output(redPin,GPIO.LOW)

def flashLed(counts,speed,LED):
        
	
        for x in range (0,counts):
                GPIO.output(LED,GPIO.HIGH)
                time.sleep(speed)
                GPIO.output(LED,GPIO.LOW)
		time.sleep(speed)

        GPIO.output(LED,GPIO.LOW)



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(redPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(greenPin,GPIO.OUT,initial=GPIO.LOW)
GPIO.output(greenPin,GPIO.LOW)
GPIO.output(redPin,GPIO.LOW)
toggleLEDs(1,0.25)
#flashLed(5,0.1,greenPin)
#flashLed(5,0.2,redPin)
time.sleep(1.5)

for z in range (0,2):
	#print (get_lan_ip())
	l = list (get_lan_ip())

	for x in l:
		if x == ".":
			flashLed(1,0.5,redPin)
			continue
		if x == "0":
			flashLed(1,2,greenPin)
			time.sleep(1)
			continue
		if int(x) in range(1,10):
			flashLed(int(x),0.5,greenPin)
			time.sleep(1)

	toggleLEDs(1,0.25)
	time.sleep(1.5)


