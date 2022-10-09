import cv2
import numpy as np
import os

def main():
    capture = cv2.VideoCapture("basicvideo.mp4")        # video a tester
    _, image = capture.read()
    previous = image.copy()
    diff = cv2.absdiff(previous, previous)                      # regarde la différence entre l'image actuelle et l'image précédente
    _, diff = cv2.threshold(diff, 32, 0, cv2.THRESH_TOZERO)     # pour comprendre, utilisé ce lien :https://docs.opencv.org/4.5.3/d7/d4d/tutorial_py_thresholding.html
    _, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)
    diff = cv2.medianBlur(diff, 5)                              # permet de diminuer le bruit sur l'image
    previousMean = np.mean(diff)

    i=0
    while (cv2.waitKey(1) < 0):
        i+=1
        check, image = capture.read()
        if not check:
            break
        diff = cv2.absdiff(image, previous)
        _, diff = cv2.threshold(diff, 32, 0, cv2.THRESH_TOZERO)
        _, diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)

        diff = cv2.medianBlur(diff, 5)
        frameMean = np.mean(diff)
        if (frameMean > previousMean+4 or frameMean < previousMean-4) and previousMean != 0: # permet de regarder la différence moyen entre l'image actuelle et la précédente
            cv2.imwrite('flash'+str(i)+'.jpg', image)       # enregistre l'image avec le numéro de frame si une différence de pixel importante est detecté, ici le Flash
        previous = image.copy()
        previousMean = frameMean.copy()

    capture.release()
    cv2.destroyAllWindows()

main()

