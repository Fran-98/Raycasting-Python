import pygame as pg
import numpy as np
from math import*
import Ray

class CastingRender:

    def casting3D(screen,screen_Size,walls,player_Pos,player_Size,look_ang,fov):

        #Define variables and other stuff. I should get rid off the number_ray variable as it is constant

        rays = []
        number_rays = 200
        ang_ray = look_ang-look_ang//360 * 360

        n = fov/number_rays

        for i in range(number_rays):
            rays.append(Ray.Ray(player_Pos[0]+(player_Size[0]/2),player_Pos[1]+(player_Size[1]/2),ang_ray + n * i, n * i,fov)) 
        
        #Define variables and other stuff.
        intersec = []
        pairs = []
        good_rays = []

        rendering_x = screen_Size[0]/2
    #La idea es tener un array así
    #[[(Tuple ray 1 cast 1),distance],
    # [(Tuple ray 1 cast 2), distancia]
    # ...............................
    # [(Tuple ray n cast n), distance]] 
    # Y luego saco un solo array con las posiciones de interseccion

        for ray in rays:
        
            pairs = []
        
            for wall in walls:
                
            
                if type(ray.cast(wall)) is np.ndarray:
                
                    pairs.append ([ray.cast(wall),ray.distance(),ray.cos])
                
                else:
                    pairs.append(["lul",screen_Size[0],"nope"])
            
        #Verifica las distancias y pasa el par mas corto a la lista de intersecciones
        
            now = ["lul",screen_Size[0],1]
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

        width_of_ray = int((screen_Size[0]/2)//number_rays)
    
        p = 0
    
        for ray in good_rays:
        
            p = 0
            p = ray[1] * ray[2]

            wall_Height = screen_Size[1] / p * 15
            if wall_Height > screen_Size[1]:
                wall_Height = screen_Size[1]/2
                
            b = 255 - 0.51 * p
            if b <0:
                b = 1

            for i in range(width_of_ray):
                rendering_x += 1
                pg.draw.line(screen,(b,0,0),(rendering_x,(screen_Size[1] - wall_Height)/2),(rendering_x,screen_Size[1]-(screen_Size[1] - wall_Height)/2))

        return intersec