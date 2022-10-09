import time
import serial  # sudo pip install pyserial should work
import cv2
import threading
import os
import sys

def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.029)

class ThreadCapCam (threading.Thread):  #definition d'une classe Thread pour faire plusieur tache en meme temps

    def __init__(self, nbFrame):                    # fonction d'nitialisation du Thread
        threading.Thread.__init__(self)
        self.nbFrame = nbFrame
        self.etat = False       # l'état du thread est soit False (à l'arrêt)
        # soit True (en marche)

    def run(self):                                  #fonction de lancement du Thread
                               # on passe en mode marche
        video = cv2.VideoCapture(0)
        width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer= cv2.VideoWriter('patchvideo.avi', cv2.VideoWriter_fourcc(*'png '), 30, (width,height))  #initialisation de la variable accueillant la video
        frames = []
        self.etat = True                # mettre l'etat a "En marche" pour le programme appellant ce Thread
        for i in range(0, self.nbFrame): # cap video
            sys.stdout.write("frame : " + str(i))
            flush_then_wait()
            check, frame = video.read()
            if not check:
                break
            frames.append(frame)

        for frame in frames: #save video
            writer.write(frame)
        writer.release()
        video.release()
        cv2.destroyAllWindows()
        self.etat = False

threadCapVideo = ThreadCapCam(500)          # créé un thread ou initialisation
threadCapVideo.start()                      # commence le Thread et continue le programme en laissant le Thread tourné de son coté
j=0
write_to_file_path="ground_truth.txt"
while os.path.exists(write_to_file_path):
    j+=1
    write_to_file_path = "ground_truth"+str(j)+".txt"
print(write_to_file_path)
output_file = open(write_to_file_path, "w+")


captures = []
i = 0
while threadCapVideo.etat == False: # Attend que le Thread soit bien lancé
    pass
ser = serial.Serial('/dev/ttyACM0', 9600)     # initialise la capture des données recue par le port USB COM4
while threadCapVideo.etat == True:    # capture des données recue par le port USB COM4
    sys.stdout.write("capture capteur : " + str(i))
    i += 1
    line = ser.readline()
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    captures.append(line)

for line in captures:
    output_file.write(line)
#modifier la chose qui enregistre en la mettant dans un thread
