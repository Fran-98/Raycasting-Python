import pygame as pg
import numpy as np
from math import*
import Ray
import Wall

pg.init()
screen_Width = 1200
screen_Height = 500
screen = pg.display.set_mode((screen_Width,screen_Height))

pg.display.set_caption("FranEngine")

walls = [Wall.Wall(50,50,50,400),Wall.Wall(50,400,400,400),Wall.Wall(50,50,400,50),Wall.Wall(400,400,400,50)] 

x = 250
y = 250
width = 20
height = 20
vel = 5
angVel = 2
ang = 0
fov = 60
number_rays = 200
run = True
lookAt = []

fps=30
startFrameTime=0

while run:
    startFrameTime = pg.time.get_ticks()

    rendering_x = screen_Width/2
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and x>vel:
        x-=vel
    if keys[pg.K_RIGHT] and x<screen_Width-width:
        x+=vel
    if keys[pg.K_UP] and y>vel:
        y-=vel
    if keys[pg.K_DOWN] and y<screen_Height-height:      
        y+=vel
    if keys[pg.K_a]:
        ang -= angVel
    if keys[pg.K_d]:
        ang += angVel    
    
    
    screen.fill((0,0,0))
    # Drawing celling and floor
    pg.draw.rect(screen,(146,146,146),(screen_Width/2,screen_Height/2,screen_Width/2,screen_Height/2)) #floor
    pg.draw.rect(screen,(60,255,220),(screen_Width/2,0,screen_Width/2,screen_Height/2)) #celling
    #Drawing linea del medio para separar we
    pg.draw.line(screen,(255,255,0),(600,0),(600,500))
    rays = []


    ang_ray = ang-ang//360 * 360
    
    n = fov/number_rays
    for i in range(number_rays):
        rays.append(Ray.Ray(x+(width/2),y+(height/2),ang_ray + n * i, n * i,fov)) 
        
    #draw player
    pg.draw.rect(screen,(100,200,100),(x,y,width,height))

    #La idea es tener un array así
    #[[(Tuple ray 1 cast 1),distance],
    # [(Tuple ray 1 cast 2), distancia]
    # ...............................
    # [(Tuple ray n cast n), distance]] 
    # Y luego saco un solo array con las posiciones de interseccion

    intersec = []
    i = 0
    dist = 0
    good_rays = []
    for ray in rays:
        #Creo la variable de pairs
        pairs = [[1,1]]*len(walls)
        
        i = 0
        for wall in walls:
            dist = 0
            
            if type(ray.cast(wall)) is np.ndarray:
                
                pairs[i] = [ray.cast(wall),ray.distance(),ray.cos]

            else:
                pairs[i] = ["lul",screen_Width,"nope"]
            i += 1
        #Verifica las distancias y pasa el par mas corto a la lista de intersecciones
        
        now = ["lul",screen_Width]
        for pair in pairs:
            if pair[1] < now[1]:
                now = pair
        if now[0] != "lul":
            intersec.append(now[0])     
            good_rays.append (now)
        #3D cast

    #Render en la segunda parte del screen
    # debemos tomar cuantos pixeles va a tener de ancho cada ray
    # luego podemos hacer las lineas de ese numero de pixeles

    width_of_ray = int((screen_Width/2)//number_rays)
    
    p = 0
    
    for ray in good_rays:
        
        p = 0
        
        p = ray[1] * ray[2]
        wall_Height = screen_Height / p * 10
        if wall_Height > screen_Height:
                wall_Height = screen_Height/2

        b = 255 - 0.51 * p
        if b <0:
            b = 1
        for i in range(width_of_ray):
            
            rendering_x += 1
            pg.draw.line(screen,(b,0,0),(rendering_x,(screen_Height - wall_Height)/2),(rendering_x,screen_Height-(screen_Height - wall_Height)/2))
                    

    for wall in walls:
        #Render de las paredes
        wall.display(screen)        
        
       
    #Drawing raycast
    for inter in intersec:
        
        pg.draw.aaline(screen,(250,0,0),(x+(width/2),y+(height/2)),inter)

    

    pg.display.update() 

    #fps counter
    #print((pg.time.get_ticks()-startFrameTime))
    pg.time.delay((int(1000/fps))-(pg.time.get_ticks()-startFrameTime))