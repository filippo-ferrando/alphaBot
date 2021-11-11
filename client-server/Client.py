'''
Author: Michele Alladio, Filippo Ferrando
es:
'''

import socket as sck, string, time

BUFFER = 4098

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('192.168.0.122', 7000))
    #s.connect(('localhost', 7001))

    print("COMANDI:\n-1 --> avanti\n-2 --> indietro\n-3 --> sinistra\n-4 --> destra\n-5 --> stop\n-6 --> avanti-indietro\n-7 --> zigzag\n-8 --> drift\n-9 --> check stato della batteria")

    while True:
        command = input().upper().encode()

        s.sendall(command)

        data = s.recv(BUFFER).decode()
        print(data)

        if data == 'STOP':
            s.close()
            print('Connection closed')
            break

if __name__ == '__main__':
    main()