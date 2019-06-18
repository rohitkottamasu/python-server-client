import socket
import subprocess
from datetime import datetime
s = socket.socket()
port = 8084
CHUNK_SIZE = 1024
s.connect(('',port))
username_pwd_flag = 0
username_pwd_list = {'root':'root'}

def validate(username,pwd):
    if(username_pwd_list[username]==pwd):
        return 1
    else:
        return 0


while True:

    print('Enter the option')
    print('1.Command Execute')
    print('2.File Download')
    print('3.File Upload')
    choice = input('Enter your choice:')
    s.send(str(choice).encode())

    if(choice== '1'):
        command = input("Enter the command:")
        s.send(command.encode()) 
        print(s.recv(1024).decode())

    elif(choice=='2'):

        if(username_pwd_flag == 0):
            username = input('Enter your username:')
            pwd = input('Enter your password:')
            
            if(validate(username,pwd)==0):
                print('Invalid Credentials')
                exit()
            username_pwd_flag = 1

        s.send(username.encode()) 
        list_of_files = s.recv(1024).decode()
        print(list_of_files.strip())
        download_file = input('Select the file to download:')
        s.send(download_file.encode())
        
        with open('client_files/'+download_file+' '+str(datetime.now()),'wb') as f:
            while True:
                data = s.recv(CHUNK_SIZE)
                print(data)
                if not data:
                    break
                f.write(data)

    elif(choice == '3'):
        #global username_pwd_flag
        if(username_pwd_flag == 0):
            username = input('Enter your username:')
            pwd = input('Enter your password:')
            if(validate(username,pwd) == 0):
                print('Invalid Credentials')
                exit()
        
        list_of_files = subprocess.check_output(['ls','/home/rohit/Viasat/client_files'])
        print(list_of_files.decode().strip())
        upload_file = input('Choose the file to upload:')

        username_file = username+' '+upload_file

        s.send(username_file.encode())
        with open('client_files/'+upload_file,'rb') as f:
            data = f.read(CHUNK_SIZE)
            print(data)
            print('Sending File..')
            while data:
                s.send(data)
                data = f.read(CHUNK_SIZE)

    elif(choice ==-1):
        exit()


        f.close()

    s.close()
