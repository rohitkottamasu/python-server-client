import socket
import datetime
import os
import subprocess
from threading import Lock,Thread
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
threads = []
port = 8084
s.bind(('0.0.0.0',port))
CHUNK_SIZE = 1024
lock = Lock()
user_files_dict = {}
class ClientHandler(Thread):
    def __init__(self,address,port,socket,choice):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.socket = socket
        self.choice = choice

    def run(self):
        if(self.choice == '1'):
            command = self.socket.recv(1024).decode()
            command = command.split()
            command_result = subprocess.check_output(command)
            self.socket.send(command_result)

        elif(self.choice == '2'):
           
            username = self.socket.recv(1024).decode()
            
            list_of_files = subprocess.check_output(['ls','/home/rohit/Viasat/server_files/'+username])
            self.socket.send(list_of_files)
            file_name = self.socket.recv(1024).decode()
            with open('server_files/'+username+'/'+file_name,'rb') as f:
                data = f.read(CHUNK_SIZE)
                print(data)
                print('Sending File..')
                while data:
                    self.socket.send(data)
                    data = f.read(CHUNK_SIZE)
            print('File Sent')
        
        elif(self.choice == '3'):

            
            username_file = self.socket.recv(1024).decode()
            username = username_file.split()[0]
            file_name = username_file.split()[1]

            try:
                subprocess.check_output(['mkdir','/home/rohit/Viasat/server_files/'+username])
            except:
                print('Directory already exists')
            

            with open('server_files/'+username+ '/'+file_name,'wb') as f:
                while True:
                    data = self.socket.recv(CHUNK_SIZE)
                    print(data)
                    if not data:
                        break
                    f.write(data)
            f.close()



        self.socket.close()

while True:
    try:
        s.listen(1)
        c,addr = s.accept()
        print('Client connected with address '+addr[0])
        choice = c.recv(1024).decode()
        newThread = ClientHandler(addr[0],addr[1],c,choice)
        newThread.start()
        threads.append(newThread)
    except KeyboardInterrupt:
        s.close()
        print('Exiting Server')
        break

for item in threads:
    item.join()
    
