import socket
from _thread import *
import sys

#in order to ser this up the command 'ipconfig' must be run in command prompt
#the ipv4 adress must then be copied from that and put below

#put the ipv4 address here
server = "10.0.4.84"
#port is the standart port 5555 for simplicity
port = 5555

print("server: " + server, "port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, server started")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print ("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))

        except:
            break
    print("lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("conntected to:", addr)

    start_new_thread(threaded_client, (conn,))
