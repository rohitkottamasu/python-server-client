import socket
import subprocess
from datetime import datetime
s = socket.socket()
port = 8083
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

        while(s.recv(1024).decode()!='ack'):
            pass
        


        list_of_files = s.recv(1024).decode()
        s.send('ack'.encode())
        print(list_of_files.strip())
        download_file = input('Select the file to download:')
        s.send(download_file.encode())
        
        while(s.recv(1024).decode()!='ack'):
            pass

        with open('/home/rohit/Viasat/client_files/'+download_file+' '+str(datetime.now()),'wb') as f:
            data = s.recv(CHUNK_SIZE)
            f.write(data)
        f.close()
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

        while(s.recv(1024).decode()!='ack'):
            pass
        

        with open('/home/rohit/Viasat/client_files/'+upload_file,'r') as f:
            data = f.readlines()
            str1 = ''
            data = str1.join(data)
            print('Sending File..')
            s.send(data.encode())
        
        f.close()

    elif(choice =='-1'):
        exit()



s.close()
