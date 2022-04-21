import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect, url_for, make_response
import time, random, string
from datetime import datetime
import RPi.GPIO as GPIO, subprocess
from flask import jsonify


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


app = Flask(__name__)
token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def validate(username, password):
    completion = False
    db = sqlite3.connect("Movimenti.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM USERS")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        #print(dbUser)
        dbPass = row[1]
        #print(dbPass)
        if dbUser == username:
            completion = check_password(dbPass, password)
    return completion
    db.close()

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #ettiva connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

def select_task_id(conn, id):   #returna w.1 oppure w.1;s.3 in base alla query scritta sul db
    conn = create_connection("Movimenti.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"SELECT sequenza FROM Movimenti Where id = {id}") #esecuzione della query

    rows = cur.fetchall()

    for row in rows:
        return(row[0])

    conn.close()

def history(user, command):
    conn = create_connection("Movimenti.db")
    cur = conn.cursor()         #in pratica questo serve solamente a fare le query per fare il retrive della lista di comandi
    cur.execute(f"INSERT INTO HISTORY (Utente, Command, Date_Log) VALUES ('{user}', '{command}', '{datetime.today()}')") #esecuzione della query
    cur.execute("commit")
    conn.close()

def login_log(user):
    conn = create_connection("Movimenti.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO LOG_UTENTI (USERNAME, DATE) VALUES ('{user}', '{datetime.today()}')")
    cur.execute("commit")
    conn.close()

mDict = {"forward":1,"backward":2, "left":3, "right":4, "stop":5, "fb":6, "zigzag":7, "drift":8}

global failed_login
failed_login = 0

ab = AlphaBot()

@app.route('/', methods=['GET', 'POST'])
def login():
    global failed_login
    error = None
    if request.method == 'POST':
        if failed_login <= 3:
            username = request.form['username']
            #* print(username)
            password = request.form['password']
            #* print(password)
            completion = validate(username, password)
            if completion == False:
                error = 'Invalid Credentials. Please try again.'
                #failed_login += 1
                print(error)
            else:
                #failed_login = 0
                login_log(username)
                print(f"{username} logged in!")
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', username)
                return resp
        elif failed_login > 3 and failed_login < 5:
            time.sleep(10)
            username = request.form['username']
            #* print(username)
            password = request.form['password']
            #* print(password)
            completion = validate(username, password)
            if completion == False:
                error = 'Invalid Credentials. Please try again.'
                failed_login += 1
                print(error)
            else:
                failed_login = 0
                login_log(username)
                print(f"{username} logged in!")
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', username)
                return resp
        elif failed_login >= 5 and failed_login < 15:
            time.sleep(20)
            username = request.form['username']
            #* print(username)
            password = request.form['password']
            #* print(password)
            completion = validate(username, password)
            if completion == False:
                error = 'Invalid Credentials. Please try again.'
                failed_login += 1
                print(error)
            else:
                failed_login = 0
                login_log(username)
                print(f"{username} logged in!")
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', username)
                return resp
        elif failed_login >=15:
            time.sleep(20)
            print("Probabile Bruteforce incoming")
            error = "Page blocked"
    return render_template('login.html', error=error)


@app.route(f'/{token}', methods=['GET', 'POST'])
def index():
    #print("--> Servita pagina di login <--")
    dbNotFound = False
    connDb = create_connection("Movimenti.db")
    if connDb == None:
        print("Database: 404")
        dbNotFound = True

    if request.method == 'POST':
        #* print(request.form.get('forward'))
        dtime = 0.5
        if request.form.get('forward') == '▲':
            #* print(username)
            username = request.cookies.get('username')
            history(username, 'forward')
            print("Avanti")
            ab.forward(sTime=dtime)
        elif  request.form.get('backward') == '▼':
            username = request.cookies.get('username')
            history(username, 'backward')
            print("Indietro")
            ab.backward(sTime=dtime)
        elif  request.form.get('left') == '◄':
            username = request.cookies.get('username')
            history(username, 'left')
            print("Sinistra")
            ab.left(sTime=dtime)
        elif  request.form.get('right') == '►':
            username = request.cookies.get('username')
            history(username, 'right')
            print("Destra")
            ab.right(sTime=dtime)
        elif request.form.get('movement'):
            data = request.form.get('movement').lower()
            #* print(username, data)
            username = request.cookies.get('username')
            history(username, data)
            commandList = select_task_id(connDb, mDict[data]).split(";")
            #* print(commandList)
            for command in commandList:
                if dbNotFound == False:
                    direction = command.split('-')[0]
                    tempo = float(command.split('-')[1])
                    print(f"{command} for {tempo} seconds")
                if direction == 'W':
                    ab.forward(sTime=tempo)
                elif direction == 'S':
                    ab.backward(sTime=tempo)
                elif direction == 'D':
                    ab.right(sTime=tempo)
                elif direction == 'A':
                    ab.left(sTime=tempo)
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


sDict = {}
DR = 16
DL = 19
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
@app.route('/api/v1/sensors/obstacles', methods=['GET'])
def sensors():
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    if((DL_status == 1) and (DR_status == 1)):
        sDict["left"] = 1
        sDict["right"] = 1
    elif((DL_status == 1) and (DR_status == 0)):
        sDict["left"] = 1
        sDict["right"] = 0
    elif((DL_status == 0) and (DR_status == 1)):
        sDict["left"] = 0
        sDict["right"] = 1
    else:
        sDict["left"] = 0
        sDict["right"] = 0

    return jsonify(sDict)
pwmL = 0
pwmR = 0
time = 0
@app.route(f'/api/v1/motors/m2?pwmL={pwmL}&pwmR={pwmR}&time={time}', methods=['GET'])
def m2():
    ab.set_pwm_a(pwmR)
    ab.set_pwm_b(pwmL)
    GPIO.output(ab.IN1, GPIO.LOW)
    GPIO.output(ab.IN2, GPIO.HIGH)
    GPIO.output(ab.IN3, GPIO.HIGH)
    GPIO.output(ab.IN4, GPIO.LOW)
    time.sleep(time)
    ab.stop()


#           .--.                  
# ::\`--._,'.::.`._.--'/::     
# ::::.  ` __::__ '  .:::: 
# ::::::-:.`'..`'.:-::::::
# ::::::::\ `--' /::::::::           

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')