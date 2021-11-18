'''
Authors: Michele Alladio, Filippo Ferrando
'''

import sqlite3
from sqlite3 import Error
import socket as sck
import time
import RPi.GPIO as GPIO, subprocess

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #ettiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def select_task_id(conn, id):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"SELECT sequenza FROM Movimenti Where id = {id}") #esecuzione della query

    rows = cur.fetchall() #applicazione della query sul database

    for row in rows:
        return(row[0]) #retrive della tabella creata

def check_battery(): # funzione che serve a returnare lo stato della batteria edl raspberry pi
    s = subprocess.check_output(['vcgencmd', 'get_throttled'])
    return s.decode()

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def left(self, sTime=2, speed=30):  #funzione per "girare" a sinistra, definiamo noi la velocità e il tempo di eseguzione della funzione (questo vale per tutte le funzioni di movimento)
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sTime)
        self.stop()
        
    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def right(self, sTime=2, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sTime)
        self.stop()

    def forward(self, sTime=2, speed=40):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sTime)
        self.stop()

    def backward(self, sTime=2, speed=40):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sTime)
        self.stop()
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    s.bind(('0.0.0.0', 7000)) 

    Ab = AlphaBot()
    
    s.listen()
    conn, addr = s.accept()
    print(f"Connessione avvenuta con: {addr}")

    connDb = create_connection("./Movimenti.db")
    

    while True:
        data = conn.recv(4096).decode()  

        commandList = select_task_id(connDb, data).split(';') #retirve della lista di comandi tramite la funzione del db

        for command in commandList: #ciclo per eseguire le istruzioni della lista e per controllare se il comando sia uno STOP per fermare il robot o un BATTERY per controllare lo stato della batteria
            if command=='STOP':
                conn.sendall('STOP'.encode())
                conn.close()
                s.close()
                print('Connection closed')
                return
            elif command=='BATTERY-0':
                if(check_battery()=='00'):
                    conn.sendall('Battery status: OK'.encode())
                else:
                    conn.sendall('Battery status: LOW'.encode())
            else:
                conn.sendall(command.encode())

            direction = command.split('-')[0]
            tempo = float(command.split('-')[1])

            print(f'{command} for {tempo} seconds')

            if direction == 'W':
                Ab.forward(sTime=tempo)
            elif direction == 'S':
                Ab.backward(sTime=tempo)
            elif direction == 'D':
                Ab.right(sTime=tempo)
            elif direction == 'A':
                Ab.left(sTime=tempo)
  
    
if __name__ == "__main__":
    main()
