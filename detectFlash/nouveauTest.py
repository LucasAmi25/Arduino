import cv2
import numpy as np
import os

def main():
    capture = cv2.VideoCapture("basicvideo.mp4")
    _, image = capture.read()
    previous = image.copy()
    diff = cv2.absdiff(previous, previous)
    _, diff = cv2.threshold(diff, 32, 0, cv2.THRESH_TOZERO)
    _, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)
    diff = cv2.medianBlur(diff, 5)
    previousMean = np.mean(diff)
    frames = []
    i=0
    width= int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer= cv2.VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (width,height))
    while (cv2.waitKey(1) < 0):
        i+=1
        check, image = capture.read()
        if not check:
            break
        diff = cv2.absdiff(image, previous)
        #image = cv2.flip(image, 3)
        #image = cv2.norm(image)
        _, diff = cv2.threshold(diff, 32, 0, cv2.THRESH_TOZERO)
        _, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)

        diff = cv2.medianBlur(diff, 5)
        frames.append(diff)
        frameMean = np.mean(diff)
        if (frameMean > previousMean+4 or frameMean < previousMean-4) and previousMean != 0:
            cv2.imwrite('flash'+str(i)+'.jpg', image)
        previous = image.copy()
        previousMean = frameMean.copy()

    capture.release()
    for frame in frames: #save video
        writer.write(frame)
    cv2.destroyAllWindows()

main()