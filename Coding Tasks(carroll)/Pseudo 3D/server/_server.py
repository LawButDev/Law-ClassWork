import socket
from _thread import *
import sys
import random

#in order to ser this up the command 'ipconfig' must be run in command prompt
#the ipv4 adress must then be copied from that and put below

#put the ipv4 address here
server = "192.168.0.167"
#port is the standart port 5555 for simplicity
port = 5555
rawmap = open("map.txt","r")

rawmap.seek(0)
rawmapsize = rawmap.readline()
rawmapsize = rawmapsize.split(" ")
mapsize = (int(rawmapsize[0]),int(rawmapsize[1]))
savedmap = []
mapstr = ""
for line in range(mapsize[1] ):
    temp = rawmap.readline()
    savedmap.append(temp)
    mapstr += str(temp)# + "|")

spawnpoints = []
spawncount = 0
rawmap.seek(0)
for y in range (mapsize[1] ):
    ystr = savedmap[y]
    for x in range (mapsize[0]):
        if ystr[x] == "s":
            spawnpoints.append(str(x) + " " + str(y))
            spawncount += 1
    

print("server: " + server, "port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, server started")

def test():
    print("yeet")

def read_pos(str):
    str = str.split(",")
    return int(str[0]),int(str[1])

def make_pos(tup):
    return (str(playercount) + "|" + str(tup[0]) + "," + str(tup[1]))

def initialpack():
    return (str(mapsize[0]) + " " + str(mapsize[1]) + "/" + spawnpoints[random.randint(0,spawncount) - 1] + "/" + mapstr)

test = initialpack()

pos = [(0,0),(100,100)]

def threaded_client(conn, player):
    #conn.send(str.encode("Connected"))
    ###conn.send(str.encode(make_pos(pos[player])))
    conn.send(str.encode(initialpack()))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            #reply = data.decode("utf-8")
            pos[player] = data

            if not data:
                print ("disconnected")
                break
            else:
                print("received: ", data)
                print("sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break
    print("lost connection")
    conn.close()

currentPlayer = 0
playercount = 0

while True:
    conn, addr = s.accept()
    print("conntected to:", addr)

    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer += 1
    playercount += 1
