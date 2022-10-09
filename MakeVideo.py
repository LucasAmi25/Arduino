from PyQt6.QtWidgets import (QWidget, QTableWidget,QTableWidgetItem,QHeaderView,QApplication , QPushButton , QInputDialog , QLineEdit ,QMainWindow, QTextEdit
,QFileDialog, QApplication ,QProgressBar,QLabel,QGridLayout,QVBoxLayout,QTabWidget,QHBoxLayout)
from PyQt6.QtGui import QIcon, QAction,QImage, QPixmap
from PyQt6.QtCore import Qt,QThread, pyqtSignal, pyqtSlot,QProcess
from pathlib import Path
import numpy as np
import cv2
import sys  
import os
import time
import math
from random import randint
import subprocess 
from shlex import split
import serial  # sudo pip install pyserial should work
import re

width=400
height=680

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changeHelpText = pyqtSignal(str)
    imageSave = pyqtSignal(cv2.VideoCapture)

    
    def __init__(self):
        super().__init__()
        self.processedImage=None
        self.faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades+'./haarcascade_frontalface_default.xml')
        self.th2=None
        self.cap = cv2.VideoCapture(0)
        self.imageSave.emit(self.cap)

    def run(self):
        
        while True:
            ret, frame = self.cap.read()
            if ret:
                
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 2)
                FlippedImage=self.detect_face(FlippedImage)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format.Format_RGB888)
                p = ConvertToQtFormat.scaled(900, height*2, Qt.AspectRatioMode.KeepAspectRatio)
                self.changePixmap.emit(p)


    def detect_face(self,img):
        texte=''
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=self.faceCascade.detectMultiScale(gray,1.2,5,minSize=(90,90))

        '''

        if str(len(faces)==0):
            self.texte.setText('mettez votre tete devant la camera et pas trop proche')
'''
        for(x,y,w,h) in faces:
            if int(w*h) <=60000 or int(x)<=100 or int(y) <=60 or int(x)>=250 or int(y)>=170:
                if int(w*h) <=60000:
                    texte+=' rapprochez vous'
                if int(x)<=100 :
                    texte+=' droite'
                if int(y) <=60 :
                    texte+=' bas'
                if int(x)>=250:
                    texte+=' gauche'
                if int(y)>=170:
                    texte+=' haut'
                test=True
                
            else:
                texte='ne bougez plus'
                test=False
            self.changeHelpText.emit(texte)
            if test:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        return img
    
        
    

    

    
class Thread2(QThread):
    changeText = pyqtSignal(str)
    def run(self):
        temps=time.time()
        diff=0
        test=120
        while diff<test:
            tmp=test-diff
            tmp2=(math.modf(tmp)[0])*0.6
            self.changeText.emit('{:.2f}'.format(math.modf(tmp)[1]+tmp2))
            print('{:.2f}'.format(math.modf(tmp)[1]+tmp2))
            diff=(time.time() -temps)
            time.sleep(0.07)
        self.changeText.emit('{:.2f}'.format(0))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.pathOutTMP = os.getcwd()
        self.title='Video'
        self.width=1000
        self.height=900
        self.processedImage=None
        self.th = Thread()
        self.initUI()
        self.p = None
        self.Image = None
       
        

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def setString(self, string):
        self.texte.setText(string)
    @pyqtSlot(str)
    def setString2(self, string):
        self.texteAmeliorationData.setText(string)
    @pyqtSlot(cv2.VideoCapture)
    def setImage2(self,array):
        self.Image = array


    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        
        
        # create a label
        self.label = QLabel(self)
        #self.label.hide()
        
        self.th.changePixmap.connect(self.setImage)
        self.th.changeHelpText.connect(self.setString2)
        self.th.start()

        self.texteAmeliorationData=QLabel(self)
        self.texteAmeliorationData.setText("Initialisation...")
        self.texteAmeliorationData.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('font-size:30px;background-color:white;')
        

        

        self.texte = QLabel(self)
        self.texte.setText('120:00')
        self.texte.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.texte.setStyleSheet('font-size: 60px;border : 2px solid black')

        self.btnTimer=QPushButton('Start',self)
        self.btnTimer.clicked.connect(self.Timer)
        self.btnTimer.setStyleSheet('background-color : lightgray;')
        

        self.btnTimer2=QPushButton('Restart',self)
        self.btnTimer2.clicked.connect(self.Timer2)
        self.btnTimer2.setStyleSheet('background-color : lightgray;')

        self.pathOut = QLabel(self)
        self.pathOut.setText(self.pathOutTMP)
        #self.pathOut.setAutoFillBackground(True)
        self.pathOut.setStyleSheet('background-color : #FFFFFF;border:1px solid lightgray;font-size: 15px;')

        self.titlePathOut = QLabel(self)
        self.titlePathOut.setText('Current path Out :')
        self.titlePathOut.setStyleSheet('font-weight:500;font-size:15px')

        self.btmPathOut= QPushButton(self)
        self.btmPathOut.setText('Change')
        self.btmPathOut.clicked.connect(self.ChangeDirectory)
        
##################################################################################################################################################################################
        hbox =QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.label,16)
        hbox.addStretch(1)
        
        

        hbox2=QHBoxLayout()
        hbox2.addWidget(self.texteAmeliorationData,3)

        vboxtmp = QVBoxLayout()
        vboxtmp.addWidget(self.btnTimer)
        vboxtmp.addWidget(self.btnTimer2)

        hbox2.addLayout(vboxtmp,2)
        hbox2.addWidget(self.texte,3)

        hbox3 =QHBoxLayout()
        hbox3.addWidget(self.titlePathOut,1)
        hbox3.addWidget(self.pathOut,7)
        hbox3.addWidget(self.btmPathOut,1)

        vbox = QVBoxLayout()   
        vbox.addLayout(hbox3,2)
        vbox.addStretch(1) 
        vbox.addLayout(hbox,16)
        vbox.addStretch(1)
        vbox.addLayout(hbox2,2  )
        
        self.setLayout(vbox)
        self.setWindowTitle('Enregistrement viideo')
        self.setFixedSize(1000, 900)
        self.center()
        self.show()
    def ChangeDirectory(self):
        home_dir = str(Path.home())
        QDir = QFileDialog.getExistingDirectory(self, "Select Directory",home_dir)  
        if QDir!='':
            self.pathOutTMP=QDir
            self.pathOut.setText(self.pathOutTMP)
   

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

    def process_finished(self):
        print("Process finished.")
        self.p = None
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


    def Timer(self):
        self.th2 = Thread2(self)
        self.th2.changeText.connect(self.setString)
        self.th2.start()
        '''code_Pulse_Sensor/
        if self.p is None:  # No process running.
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python3", ['./code_Pulse_Sensor/captureData.py'])
        '''
        '''
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
        '''
         
        serial_port ='/dev/ttyACM0' 		 	 	 	
        baud_rate = 9600 #In arduino, Serial.begin(baud_rate)
        j=0
        write_to_file_path="ground_truth.txt"
        while os.path.exists(write_to_file_path):
            j+=1
            write_to_file_path = "ground_truth"+str(j)+".txt"

        output_file = open(write_to_file_path, "w+")
        ser = serial.Serial(serial_port, baud_rate)

        self.th.imageSave.connect(self.setImage2)
        print(self.Image)
        
        width= int(self.Image.get(cv2.CAP_PROP_FRAME_WIDTH))
        height= int(self.Image.get(cv2.CAP_PROP_FRAME_HEIGHT))
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

            

    def Timer2(self):
        if self.th2.isRunning():
            self.th2.terminate()
        self.texte.setText('120:00')
##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed







        
        


def main():

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


