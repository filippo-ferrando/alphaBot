import requests
import time
import random


def main():
    while True:
        sensors = requests.get('http://192.168.0.139:5000/api/v1/sensors/obstacles')
        print(sensors.json())

        '''if sensors.json()['right'] == 0:
            r = requests.get(f'http://192.168.0.139:5000/api/v1/motors/m2?pwmL={30}40&pwmR={0}&time={0.15}')

        elif sensors.json()['left'] == 0:
            r = requests.get(f'http://192.168.0.139:5000/api/v1/motors/m2?pwmL={0}&pwmR={-30}&time={0.15}')'''

        if sensors.json()['left'] == 1 and sensors.json()['right'] == 1:
            r = requests.get(f'http://192.168.0.139:5000/api/v1/motors/m2?pwmL={70}&pwmR={-35}&time={0.4}')
            r = requests.get(f'http://192.168.0.139:5000/api/v1/motors/m2?pwmL={25}&pwmR={-70}&time={0.4}')
            
            
        
        elif sensors.json()['left'] == 0 and sensors.json()['right'] == 0:
            r = requests.get(f'http://192.168.0.139:5000/api/v1/motors/m2?pwmL={-30}40&pwmR={30}&time={0.5}')

        time.sleep(0.2)


if __name__ == "__main__":
    main()