import socket
import pickle

class Network:
    def __init__(self,ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def read_pos(self,str):
        str = str.split(",")
        return int(str[0]), int(str[1])


    def make_pos(self,tup):
        return str(tup[0]) + "," + str(tup[1])


    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
