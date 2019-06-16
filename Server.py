import socket
import datetime
from threading import Lock,Thread
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
threads = []
port = 8085
s.bind(('0.0.0.0',port))
counter = 0
thread_lock = Lock()
CHUNK_SIZE = 1024

class ClientHandler(Thread):
    def __init__(self,address,port,socket,choice):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.socket = socket
        self.choice = choice

    def run(self):
        if(self.choice == '1'):
            self.socket.send(str(datetime.datetime.now()).encode())


        elif(self.choice == '2'):
            with open('Files/sample.txt','rb') as f:
                data = f.read(CHUNK_SIZE)
                print(data)
                print('Sending File..')
                while data:
                    self.socket.send(data)
                    data = f.read(CHUNK_SIZE)

            print('File Sent')

        self.socket.close()

while True:
    try:
        s.listen(1)
        c,addr = s.accept()
        choice = c.recv(1024).decode()
        newThread = ClientHandler(addr[0],addr[1],c,choice)
        newThread.start()
        threads.append(newThread)
    except KeyboardInterrupt:
        print('Exiting Server')
        break

for item in threads:
    item.join()
    
