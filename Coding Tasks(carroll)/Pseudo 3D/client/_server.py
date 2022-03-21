import socket
from _thread import *
import sys
import random
import pickle
import pygame
from classes import pseudoplayer

class scoreentry():
    def __init__(self,pID):
        self.ID = pID
        self.kills = 0
        self.deaths = 0

scoreboard = []

#in order to ser this up the command 'ipconfig' must be run in command prompt
#the ipv4 adress must then be copied from that and put below

#put the ipv4 address here
server = "192.168.0.179"
#port is the standart port 5555 for simplicity
port = 5555
rawmap = open("map.txt","r")
maxplayers = 15

players = []
currentplayers = []

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
    return (str(tup[0]) + "," + str(tup[1]))

def initialpack(playerint):
    return (str(mapsize[0]) + " " + str(mapsize[1]) + "/" + spawnpoints[random.randint(0,spawncount) - 1] + "/" + mapstr + "/" + str(playerint))


pos = [(0,0),(100,100)]


currentPlayer = 0
playercount = 0
deadflag = False

def threaded_client(conn, player):
    deadflag = False
    #conn.send(str.encode("Connected"))
    ###conn.send(str.encode(make_pos(pos[player])))
    reply = conn.send(str.encode(initialpack(player)))
    placeholder = pseudoplayer(0,0,0,0)
    players.append(placeholder)
    currentplayers.append(player)
    boardline = scoreentry(player)
    scoreboard.append(boardline)
    #reply = (0,0)
    while True:
        indexval = currentplayers.index(player)
        if deadflag == False and players[indexval].health < 0:
            spawnpoint = spawnpoints[random.randint(0,spawncount) - 1].split(" ")
            players[indexval].posx = int(spawnpoint[1])
            players[indexval].posy = int(spawnpoint[0])
            deadflag = True
            #players[indexval].health = 100
        toreply = players.copy()
        #print(indexval)
        toreply.pop(indexval)
        toreply.insert(0,players[indexval])
        #print(currentplayers)
        reply = toreply
        try:
            data = pickle.loads(conn.recv(2048))
            #reply = data.decode("utf-8")
            indexval = currentplayers.index(player)
            temphealth = players[indexval].health
            if deadflag == True:
                temphealth = 100
                deadflag = False
            data.health = temphealth
            indexval = currentplayers.index(player)
            players[indexval] = data
            if data.todamage != -1:
                players[currentplayers.index(data.todamage)].health -= 20
                if players[currentplayers.index(data.todamage)].health < 0:
                    for i in scoreboard:
                        if i.ID == player:
                            i.kills += 1
                        elif i.ID == data.todamage:
                            i.deaths += 1
                            

            if not data:
                print ("disconnected")
                break
            else:
                #print("received: ", data)
                #print("sending: ", reply)
                pog = True
            conn.sendall(pickle.dumps(reply))

        except:
            break
    print("lost connection")
    #playercount -= 1
    indexval = currentplayers.index(player)
    players.pop(indexval)
    currentplayers.pop(indexval)
    conn.close()

def scoreprinter():
    clock = pygame.time.Clock()
    while True:
        print("\n\n==================")
        for i in scoreboard:
            print("player " + str(i.ID) + " | " + str(i.kills) + " kill(s) | " + str(i.deaths) + " death(s)")
        clock.tick(1)

start_new_thread(scoreprinter,())

while True:
    conn, addr = s.accept()
    print("conntected to:", addr)

    if (len(currentplayers) <= maxplayers):
        start_new_thread(threaded_client, (conn,currentPlayer))
        playercount += 1
        currentPlayer += 1
        #currentPlayer = 1-currentPlayer

    for i in range(0,playercount):
        print("player " + str(i))
