# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM4', baudrate=9600)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = '45' # Taking input from user
    value = write_read(num)
    print(value) # printing the value