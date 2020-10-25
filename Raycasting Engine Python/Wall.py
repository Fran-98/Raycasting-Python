import pygame as pg
import numpy as np

class Wall:

    def __init__(self,x1,y1,x2,y2):
        self.a = [x1,y1]
        self.b = [x2,y2]
    def display(self,screen):
        pg.draw.line(screen,(255,0,0),self.a,self.b)
    def hola():
        print("Hola")