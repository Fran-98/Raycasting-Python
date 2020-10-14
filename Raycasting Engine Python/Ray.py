import pygame as pg
from numpy import *

class Ray:

    def __init__(self,x,y,ang,phi,fov):
        self.pos = [x,y]
        self.dir = array([cos(deg2rad(ang)),sin(deg2rad(ang))])
        self.cos = cos(deg2rad(absolute(fov/2-phi)))
        self.pot = 0
        
    def display(self, screen):
        pg.draw.line(screen,(0,0,255),self.pos,(self.pos+10 * self.dir),1)

    def cast(self,wall):

        #punto inicial boundary
        x1 = wall.a[0]
        y1 = wall.a[1]

        #punto final boundary
        x2 = wall.b[0]
        y2 = wall.b[1]

        #posicion del ray
        x3 = self.pos[0]
        y3 = self.pos[1]

        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        #Aplicando formula de la interseccion de dos segmento
        #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

        #denominador de la ecuacion
        den = (x1 - x2) * (y3 -y4) - (y1 - y2) * (x3 - x4)
        #numerador de la ecuacion
        num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)

        #Si las lineas son paralelas o coincidentes el denominador es cero, por lo que:
        if den == 0:
            return None

        #Aplicando las formulas

        t = num/den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        #si 0<t<1 la interseccion cae en el primer segmento, si u>0 cae en el segundo segmento
        if t > 0 and t < 1 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            self.pot = array([x,y])
            return self.pot
    
    def distance (self):
        #Calculo de distancia si estamos mirando al cuarto cuadrante (origen x,y jugador)
        d = 0
        #x2-x1 y y2-x1
        if self.pot[0]> self.pos[0] and self.pot[1] > self.pos[1]:
            d = sqrt(pow(self.pot[0]-self.pos[0],2)+pow(self.pot[1]-self.pos[1],2))
        #tercer cuadrante
        if self.pot[0]< self.pos[0] and self.pot[1] > self.pos[1]:
            d = sqrt(pow(self.pos[0]-self.pot[0],2)+pow(self.pot[1]-self.pos[1],2))
        #segundo cuadrante
        if self.pot[0]< self.pos[0] and self.pot[1] < self.pos[1]:
            d = sqrt(pow(self.pos[0]-self.pot[0],2)+pow(self.pos[1]-self.pot[1],2))
        #primer cuadrante
        if self.pot[0]> self.pos[0] and self.pot[1] < self.pos[1]:
            d = sqrt(pow(self.pot[0]-self.pos[0],2)+pow(self.pos[1]-self.pot[1],2))
                
        return d