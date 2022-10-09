	##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed
import time

import serial  # sudo pip install pyserial should work
import cv2
import re
import subprocess
import os

def find_by_id(n):
    v,p=n.split(':')
    v=removeLeadingZeros(v)
    p=removeLeadingZeros(p)
    v=os.popen(f"	")
    return v.read().split('DEVNAME=')[-1][:-1]


def removeLeadingZeros(test):
    count=0
    for i in test:
        
        if i=='0':
            count+=1
        else:
            return test[count:]
    if test=='0000':
        return 'O'
    return test




device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []

for i in str(df).split('\\n'):
    if i:
        info = device_re.match(i)
        if info:
            dinfo = info.groupdict()
            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            devices.append(dinfo)
for d in devices:
    if d['tag'].__contains__('Arduino'):
        serial_port = '/dev/ttyACM0' 
serial_port ='/dev/ttyACM0' 		 	 	 	
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)
j=0
write_to_file_path="ground_truth.txt"
while os.path.exists(write_to_file_path):
    j+=1
    write_to_file_path = "ground_truth"+str(j)+".txt"

output_file = open(write_to_file_path, "w+")
ser = serial.Serial(serial_port, baud_rate)

video = cv2.VideoCapture(0)
width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_name="basicvideo.avi"
k=0
while os.path.exists(video_name):
    k+=1
    video_name = "basicvideo"+str(k)+'.avi'

writer= cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'png '), 30, (width,height))
i = 0
frames = []
captures = []
while len(frames) < 2000:
    print(i)
    i+=1
    start = time.perf_counter()
    check, frame = video.read()
    print("prise d'image : "+str(time.perf_counter()-start))
    if not check:
        break
    start2 = time.perf_counter()
    line = ser.readline()
    print("prise capteur : "+str(time.perf_counter()-start2))
    line = line.decode("latin-1") #ser.readline returns a binary, convert to string
    captures.append(line)
    #cv2.imshow('frame',frame)
    #writer.write(frame)
    frames.append(frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    print("one prise : "+ str(time.perf_counter()-start))
for frame in frames:
    writer.write(frame)
for line in captures:
    output_file.write(line)
video.release()
writer.release()
cv2.destroyAllWindows()
