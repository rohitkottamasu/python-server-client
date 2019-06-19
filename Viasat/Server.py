import socket
import datetime
import os
import subprocess
from threading import Lock,Thread
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
threads = []
port = 8083
s.bind(('0.0.0.0',port))
CHUNK_SIZE = 1024
lock = Lock()
user_files_dict = {}
class ClientHandler(Thread):
    def __init__(self,address,port,socket):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.socket = socket
        #self.choice = choice

    def run(self):
        while True:
            choice = self.socket.recv(1024).decode()
            if(choice == '1'):
                command = self.socket.recv(1024).decode()
                command = command.split()
                command_result = subprocess.check_output(command)
                self.socket.send(command_result)

            elif(choice == '2'):
            
                username = self.socket.recv(1024).decode()
                self.socket.send('ack'.encode())
                list_of_files = subprocess.check_output(['ls','/home/rohit/Viasat/server_files/'+username])
                self.socket.send(list_of_files)

                while(self.socket.recv(1024).decode()!='ack'):
                    pass

                file_name = self.socket.recv(1024).decode()

                self.socket.send('ack'.encode())

                with open('/home/rohit/Viasat/server_files/'+username+'/'+file_name,'r') as f:
                    data = f.readlines()
                    str1 = ''
                    data = str1.join(data)
                    self.socket.send(data.encode())
            
            elif(choice == '3'):

                
                username_file = self.socket.recv(1024).decode()
                username = username_file.split()[0]
                file_name = username_file.split()[1]

                self.socket.send('ack'.encode())

                try:
                    subprocess.check_output(['mkdir','/home/rohit/Viasat/server_files/root'])
                except:
                    print('Directory already exists')
                

                with open('/home/rohit/Viasat/server_files/'+username+'/uploaded_file.txt'+str(datetime.datetime.now()),'wb') as f:
                    data = self.socket.recv(1024)
                    f.write(data)
                f.close()



        self.socket.close()

while True:
    try:
        s.listen(1)
        c,addr = s.accept()
        print('Client connected with address '+addr[0])
        #choice = c.recv(1024).decode()
        newThread = ClientHandler(addr[0],addr[1],c)
        newThread.start()
        threads.append(newThread)
    except KeyboardInterrupt:
        s.close()
        print('Exiting Server')
        break

for item in threads:
    item.join()
    
