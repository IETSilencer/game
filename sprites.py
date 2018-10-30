
from settings import *
import pygame as pg
import math
import random 

vec = pg.math.Vector2 




class Player(pg.sprite.Sprite):
    # sprite for the Player
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game 
        self.image = pg.Surface((50,50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        self.rect.center = ((WIDTH/2,HEIGHT/2))
        self.acc_up = vec(0,0) 
        
    def jump(self):
        self.rect.x += 1
        hit = pg.sprite.spritecollide(self,self.game.platforms, False)
        self.rect.x -= 1
        if hit:
            self.vel.y = PLAYER_JUMP 

    def sticktowall(self):
        hit = pg.sprite.spritecollide(self.player,self.platforms,False)
        if self.player.rect.midleft < self.platforms.rect.midright and self.player.rect.top < self.platforms.rect.bottom:
            if hit:
                self.player.rect.midleft = hit[0].rect.midright
 
        
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)   
        keystate = pg.key.get_pressed()
       

        if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keystate[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        if keystate[pg.K_UP]:
            self.acc_up = (0,-5) 

        self.acc.x += self.vel.x * PLAYER_FRICTION 
        self.vel += self.acc
        self.pos += self.vel + self.acc
        self.acc_up += self.acc_up
        

        if self.pos.x > WIDTH:
            self.pos.x = 0
 
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
        

        
        """
        if self.rect.bottom > HEIGHT - 20:
            self.rect.center = ((WIDTH /2, HEIGHT / 2))
        """
        
            
        

class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y

class movingplatforms(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y
        self.vel_x = 10

    def update(self):
        self.rect.x += 10
        if self.rect.x > WIDTH:
            width = random.randrange(50,100)

            mp = movingplatforms(random.randrange(0,WIDTH-width),
                         random.randrange(-75,-30),
                         width,20)
            self.movingplatforms.add(mp)

            self.all_sprites.add(mp)

       
            
            

class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        


        
