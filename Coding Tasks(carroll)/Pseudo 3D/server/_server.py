import socket
from _thread import *
import sys

#in order to ser this up the command 'ipconfig' must be run in command prompt
#the ipv4 adress must then be copied from that and put below

#put the ipv4 address here
server = "10.0.4.84"
#port is the standart port 5555 for simplicity
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bing((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, server started")
