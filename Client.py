import socket
import pyaudio

s = socket.socket()
port = 8085
CHUNK_SIZE = 1024
s.connect(('127.0.0.1',port))

print('Enter the option')
print('1.Date')
print('2.File Download')
print('3.File Upload')
choice = input('Enter your choice:')
s.send(str(choice).encode())

if(choice=='1'):   
    print(s.recv(1024).decode())

elif(choice=='2'):
   with open('client_files/received_file.txt','wb') as f:
       while True:
           data = s.recv(CHUNK_SIZE)
           print(data)
           if not data:
               break
           f.write(data)
   f.close() 
s.close()
