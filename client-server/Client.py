'''
Author: Michele Alladio
es:
'''

#import time
#import RPi.GPIO as GPIO

import socket as sck, string, time

a = 'W100'
print(a[1:])

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('192.168.0.122', 7002))

    print("COMANDI:\n-W --> avanti\n-S --> indietro\n-D --> destra\n-A --> sinistra\n-STOP --> stop\nI comandi devono essere seguiti da un numero che indica di quanto avanzare e i due argomenti separati da un punto.\nEs:W.100")

    while True:
        command = input().upper().encode()

        s.sendall(command)

    '''try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()'''

if __name__ == '__main__':
    main()





'''import socket as sck
import string
import threading as thr
import time

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('localhost', 7000))

    while True:
        message = input("Inserisci il messaggio: ")
        s.sendall(message.encode())

        data = s.recv(4096)
        print(data.decode())

if __name__ == "__main__":
    main()'''