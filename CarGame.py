from typing import Any
import pygame
from pygame.locals import *
from random import randint
import time

sprites = ["enemy1.png","enemy2.png","enemy3.png","enemy3.png"]

class sprite(pygame.sprite.Sprite):
    def __init__(self,img,pos,screen,layer):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        self._layer = layer
        pygame.sprite.Sprite.__init__(self)


class car(sprite):
    def __init__(self,img,pos,screen,layer):
        super().__init__(img,pos,screen,layer)
        self.CollisionRect = self.rect.copy()
        self.CollisionRect.center = pygame.Vector2(pos.x+15,pos.y+15)
        self.CollisionRect.width -= 30
        self.CollisionRect.height -= 40
        pygame.draw.rect(self.image,"green",[15,15,self.CollisionRect.width,self.CollisionRect.height],5)
    def update(self,pos):
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.CollisionRect.center = pygame.Vector2(pos.x+15,pos.y+15)
        pygame.draw.rect(self.image,"green",[15,15,self.CollisionRect.width,self.CollisionRect.height],5)
        #pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        
class Enemy(sprite):
    def __init__(self,img,pos,screen,group,layer,speed):
        super().__init__(img,pos,screen,layer)
        self.speed = speed
        self.pos = pos
        pygame.sprite.Sprite.__init__(self,group)
    def update(self,lose):
        self.rect = self.image.get_rect()
        if(not lose):
            self.pos.y += (self.speed)*dt
        self.rect.center = self.pos
        pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        self.reset()
    def reset(self):
        if(self.rect.y>=screen.get_height()):
            #self.__init__(sprites[randint(0,1)]
            #            ,pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100))
            #            ,screen,group,0,randint(int(1),int(1)))
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(sprites[randint(0,3)]).convert_alpha()
            self.rect = self.image.get_rect()
            self.pos = pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,0))
            self.rect.center = self.pos
            pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
            screen.blit(self.image,self.rect)
            self.speed = randint(int(1),int(2))

    
pygame.init()

running = True
lost=False
clock = pygame.time.Clock()
dt = 0
StartTime = time.time()
RespawnRate = 3
score = 0

screen = pygame.display.set_mode()  
road = pygame.image.load("road.png").convert()
pygame.draw.rect(road,"red",[0,0,road.get_rect().width,road.get_rect().height],5)
screen.blit(road,((screen.get_width() / 2 )-(road.get_width()/2), -10))
myfont = pygame.font.SysFont("monospace", 24)

x = ((int(screen.get_width() / 2 ))-(int(road.get_width()/2))) + 100
lx = (x + road.get_width()) -300
group = pygame.sprite.LayeredUpdates()
PPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)
player = car("player7.png",PPos,screen,1)
enemy0 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100)),screen,group,0,2)
enemy1 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100)),screen,group,0,3)
enemy2 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100)),screen,group,0,1)
enemy3 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100)),screen,group,0,2)
enemy4 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,100)),screen,group,0,2)
while running:
    screen.fill("green")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(road,((screen.get_width() / 2 )-(road.get_width()/2), -10))
    
    player.update(PPos)
    group.update(lost)
    group.draw(screen)
    
    #coll = pygame.sprite.spritecollideany(player, group, collided = None)
    coll = player.CollisionRect.collidelist(group.get_sprites_from_layer(0))
    print(coll)
    if(coll != -1):
        lost = True
        
    if(not lost):
        keys = pygame.key.get_pressed()     
        if keys[pygame.K_a]:
            if(not((player.rect.x - (7 * dt))<=x)):
                PPos.x -= 7 * dt
        if keys[pygame.K_d]:
            if(not((player.rect.x + (7 * dt))>=lx)):
                PPos.x += 7 * dt
        score = int((time.time() - StartTime))
    else:
        EndGameText = myfont.render(f"Good game \n Score: {score} \n Better luck next time", 0, "red")
        pygame.draw.rect(screen,"#00FFB9",[(screen.get_width() / 2)-(EndGameText.get_width()/2), screen.get_height()/2,EndGameText.get_width(),EndGameText.get_height()],0)
        screen.blit(EndGameText, ((screen.get_width() / 2)-(EndGameText.get_width()/2), screen.get_height()/2))
    
    scoretext = myfont.render(f"Score: {score}", 0, "red")
    pygame.draw.rect(screen,"#00FFB9",[50,25,scoretext.get_width(),scoretext.get_height()],0)
    screen.blit(scoretext, (50, 25))
    
    pygame.display.update()
    
    dt = clock.tick(30) / 10
    
pygame.quit()































#players = pygame.sprite.Group()
#players.add(player)
#print(players)
#100*191
#players.update()
#players.draw(screen)
#screen.blit(grass,(0,0))
#grass = pygame.image.load("Grass.png")
#player.update(PPos)
#screen.blit(grass,(0,0))