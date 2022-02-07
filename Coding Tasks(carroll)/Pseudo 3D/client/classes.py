import pygame
import math

class pseudoplayer():
   def __init__(self,pox,posy,rotation,Pid):
       self.posx = pox
       self.posy = posy
       self.rotation = rotation
       self.id = Pid
       self.todamage = -1
       self.health = 100
