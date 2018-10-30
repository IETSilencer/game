import pygame as pg 
import os
import sys
from pygame.locals import *
from time import *
import random
import math
import random
from os import path 
from settings import * 
from sprites import * 

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir,HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0        
        

    def new(self):
        self.background = Background('bg_grasslands.png',[0,0])
        self.backgroundgroup = pg.sprite.Group()
        self.backgroundgroup.add(self.background)

        self.movingplatforms = pg.sprite.Group() 

    

         
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)

        self.all_sprites.add(self.background)
        self.all_sprites.add(self.player)

        self.score = 0
    
        for mplat in PLATFORM_LIST:
            mp = movingplatforms(*mplat)
            self.all_sprites.add(mp)
            self.movingplatforms.add(mp) 


        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)



        self.run()
        
    
    def run(self):
        self.playing = True 
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw() 

    def update(self):
        self.all_sprites.update()


        if self.player.vel.y > 0: 
            hit = pg.sprite.spritecollide(self.player,self.platforms,False)
            if hit:
                self.player.pos.y = hit[0].rect.top
                self.player.vel.y = 0 
  

            
        if self.player.pos.y <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10 


        for plat in self.movingplatforms:
            if plat.rect.x > WIDTH:
                plat.kill()
                width = random.randrange(50,100)

                mp = movingplatforms(random.randrange(0,WIDTH-width),
                         random.randrange(-75,-30),
                         width,20)
                movingplatforms.add(mp)

                self.all_sprites.add(mp)


        while len(self.platforms) < 6:
            width = random.randrange(50,100)

            p = Platform(random.randrange(0,WIDTH-width),
                         random.randrange(-75,-30),
                         width,20)
            self.platforms.add(p)

            self.all_sprites.add(p)

        
    
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()


        if len(self.platforms) == 0:
            self.playing = False

        
                
        

    def events(self):
        for event in pg.event.get():
        # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump() 


        

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),100,WHITE, WIDTH/2,HEIGHT/2)
        

        pg.display.flip()
    

    def show_start_screen(self):
        self.screen.fill(BLUE) 
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrows to move and Space to jump", 22, WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("press a key to start",22, WHITE,WIDTH/2,HEIGHT/3)

        self.draw_text("HighScore" + str(self.highscore),22, WHITE,WIDTH/2,0)

        pg.display.flip()
        self.wait_for_key()       


    def show_go_screen(self):
        if not self.running:
            return 
        self.screen.fill(BLUE)
        self.draw_text('score' + str(self.score),48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrows to move and Space to jump", 22, WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("press a key to start over",22, WHITE,WIDTH/2,HEIGHT/3)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGHSCORE" + str(self.score),22, WHITE,WIDTH/2,100)
            with open(path.join(self.dir, HS_FILE),'w') as f:
                f.write(str(self.score)) 

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                if event.type == pg.KEYUP:
                    waiting = False 
                
                    

    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)
        


g = Game()  
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()


    
    

pg.quit() 
    
