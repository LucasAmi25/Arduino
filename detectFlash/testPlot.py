import cv2
import matplotlib.pyplot as plt
import numpy as np

video = cv2.VideoCapture("flash.mp4")

i=0
ypoints = []

while video.isOpened():
    check, frame = video.read()
    if not check:
        break

    print('\rTracking frame: {}'.format(i), end='')

    ypoints.append(np.mean(frame))
    i+=1

plt.plot(np.arange(0,i), np.array(ypoints))
plt.savefig("mygraph.png")
