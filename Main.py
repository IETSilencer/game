import pygame
import os
import sys
from pygame.locals import *
from time import *
import random
import math

import pygame
import random

from PIL import Image
from settings import * 




class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.image.load('protein.png')
        self.image = pygame.transform.scale(self.image,(50,50))
        
        

        self.image.set_colorkey(BLACK)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = ((WIDTH-200, HEIGHT / 2))
        self.speedx = 0
        self.speedy = 0 
    
        

    def update(self):
        self.speedx = 0
        self.speedy = 0 

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5

        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        if keystate[pygame.K_UP]:
            self.speedy = -5

            

        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                    self.rect.x += -self.x_speed
            elif event.key == pygame.K_RIGHT:
                    self.rect.x += self.x_speed
       
                 
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        """
        if self.rect.x > WIDTH:
            self.rect.x = 0

        if self.rect.bottom > HEIGHT - 20:
            self.rect.center = ((WIDTH /2, HEIGHT / 2))


    def shoot(self):
            bullet = Bullet(self.rect.center, self.rect.top,RED)
            all_sprites.add(bullet)
            bullets.add(bullet)


                

class Mob(pygame.sprite.Sprite):
    def __init__(self, tsw, tsh):
        pygame.sprite.Sprite.__init__(self)
        self.tsw = tsw
        self.tsh = tsh
        #self.color = color
        #self.image = pygame.Surface((self.tsw,self.tsh))
        #self.image.fill(self.color)
        self.image = pygame.image.load('dna.png')
        self.image = pygame.transform.scale(self.image,(self.tsw,self.tsh))
        
        
        self.rect = self.image.get_rect()
        #self.thingrect.left, self.thingrect.top = location 
        self.rect.center = ((WIDTH / 2, HEIGHT / 2))
        self.speedx = random.randint(1,9) 
        self.speedy = random.randint(-9,9) 

        

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        
        if self.rect.x < 0:
            self.rect.x = random.randint(WIDTH,WIDTH+700)
            self.rect.y = random.randint(0, HEIGHT) 
            self.rect.x += -random.randint(1,30)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x, y,color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((20,20))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.speedx = 50
        self.rect.bottom = y
        self.rect.center = x 

    def update(self):
        self.rect.x += self.speedx 

        if self.rect.x > WIDTH :
            self.kill()

            


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Example")
clock = pygame.time.Clock()

player = Player()
background = Background('bg_grasslands.png',[0,0])
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
mobs = pygame.sprite.Group() 

for elements in range(35):
    m = Mob(random.randint(20,100),random.randint(20,100))
    all_sprites.add(m)
    mobs.add(m) 
    




bullets = pygame.sprite.Group()






# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot() 

    
    
    screen.blit(background.image, background.rect)
    #screen.blit(thing.surf,thing.thingrect)


    

    #thinglist.thingmove()
    #thinglist.thingupdate() 
    # Updates

    all_sprites.update() 

    hits = pygame.sprite.groupcollide(bullets,mobs,True, True)
    for hit in hits:
        m = Mob(random.randint(20,100),random.randint(20,100)) 
        all_sprites.add(m)
        mobs.add(m) 
        


    hit = pygame.sprite.spritecollide(player,mobs,False)
    if hit:
        running = False
    

    
 

   
    # screen.fill(BLUE)
    all_sprites.draw(screen)
   
   
    

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
