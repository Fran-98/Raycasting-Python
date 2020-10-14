import pygame as pg
import numpy as np
from math import*
import Ray
import Wall
from CastingRender import CastingRender

pg.init()
screen_Width = 1200
screen_Height = 500
screen_Size = (screen_Width,screen_Height)
screen = pg.display.set_mode((screen_Width,screen_Height))

pg.display.set_caption("FranEngine")

walls = [Wall.Wall(50,50,50,400),Wall.Wall(50,400,400,400),Wall.Wall(50,50,400,50),Wall.Wall(400,400,400,50)] 

x = 250
y = 250
player_size = (20,20)
vel = 5
angVel = 2
ang = 0
fov = 60

run = True

fps=30
startFrameTime=0

while run:
    startFrameTime = pg.time.get_ticks()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and x>vel:
        x-=vel
    if keys[pg.K_RIGHT] and x<screen_Width-player_size[0]:
        x+=vel
    if keys[pg.K_UP] and y>vel:
        y-=vel
    if keys[pg.K_DOWN] and y<screen_Height-player_size[1]:      
        y+=vel
    if keys[pg.K_a]:
        ang -= angVel
    if keys[pg.K_d]:
        ang += angVel    
    
    screen.fill((0,0,0))

    # Drawing celling and floor
    pg.draw.rect(screen,(146,146,146),(int(screen_Width//2),int(screen_Height//2),int(screen_Width/2),int(screen_Height/2))) #floor
    pg.draw.rect(screen,(60,255,220),(int(screen_Width//2),0,int(screen_Width//2),int(screen_Height/2))) #celling

    #Drawing linea del medio para separar we
    pg.draw.line(screen,(255,255,0),(600,0),(600,500))
    
    #draw player

    pg.draw.rect(screen,(100,200,100),(x,y,player_size[0],player_size[1]))

    for wall in walls:
        #Render de las paredes
        wall.display(screen)        
        
    intersec = CastingRender.casting3D(screen,screen_Size,walls,(x,y),player_size,ang,fov)

    #Drawing raycast
    for inter in intersec:
        
        pg.draw.aaline(screen,(250,0,0),(x+(player_size[0]/2),y+(player_size[1]/2)),inter)

    

    pg.display.update() 

    #fps counter
    #print((pg.time.get_ticks()-startFrameTime))
    pg.time.delay((int(1000/fps))-(pg.time.get_ticks()-startFrameTime))