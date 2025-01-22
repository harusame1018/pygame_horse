import pygame
from pygame.locals import *
import sys
import os
import time
import asyncio
#import pyjsdl as pygame
#FPS = 2

class sankaku(pygame.sprite.Sprite):
    def __init__(self,filename,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.Sankaku = pygame.Surface((240,240))
        print(self.rect)
        print(self.Sankaku)
        self.x = x
        self.y = y
    def update(self,x,y):
        self.x = x
        self.y = y


class horse_Sprite(pygame.sprite.Sprite):
    frame = 0
    flag = 0
    images = []

    def __init__(self,name,x,y):
        pygame.sprite.Sprite.__init__(self)
        all_image = pygame.image.load(name).convert_alpha()
        self.char_width = all_image.get_width()
        self.char_height = all_image.get_height()

        for i in range(0,self.char_height,240):
            for j in range(0,self.char_width,240):
                c_pattern = pygame.Surface((240,240))
                c_pattern.blit(all_image,(0,0),(j,i,240,240))
                c_pattern.convert_alpha()
                colorkey = c_pattern.get_at((0,0))
                c_pattern.set_colorkey(colorkey,RLEACCEL)
                self.images.append(c_pattern)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x,y))
        print(self.rect)
        self.y = 240
    def update(self,way,bgx,mono):
        #print(self.images)
        #print(int(self.frame/5) + way * int(self.char_width / 240))
        self.image = self.images[int(self.frame/5) + way * int(self.char_width / 240)]

        if self.flag == 0:
            self.frame += 1
        else:
            self.frame -= 1

        if self.frame >= len(self.images) / int(self.char_height / 240) *5:
            self.frame = 5 * 2 - 1
            self.flag = 1
        elif self.frame < 0:
            self.frame = 5
            self.flag = 0
            
        #if self.rect.colliderect(mono):
        #    print("True")
        #self.rect = self.image.get_rect(center=((500,420)))
    def draw(self,surface,x,y):
        surface.blit(self.image,(x,y))
        self.y = y
    #def collide_shogaibutsu(self,mono):

def menu():
    running = True
    pygame.init()
    font = pygame.font.SysFont("けいふぉんと",36)
    screen = pygame.display.set_mode((1000,800))
    pygame.display.set_caption("you are an idiot")
    clock = pygame.time.Clock()
    start_text = font.render("馬が走るだけのゲーム\n注意:中毒性なし\n閉じたら始まります",True,(0,0,0))
    while running:
        screen.fill((255,255,255))
        screen.blit(start_text,(0,400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit
                
async def main():
    await asyncio.sleep(0)
    start_time = time.time()
    end_flag = False
    space_count = 0
    horse_y = 320
    shogaibutsu_yoketa = 0
    mae = pygame.sprite.LayeredUpdates()
    way = 0
    pygame.init()
    font = pygame.font.SysFont(None,50)
    screen = pygame.display.set_mode((1000,800))
    pygame.display.set_caption("you are an idiot")
    shogaibutsu = sankaku("./img/sankaku.png",400,420)
    shogaibutsu2 = sankaku("./img/sankaku.png",400,120)
    goal = pygame.image.load("./img/goal.png").convert_alpha()
    rect_goal = goal.get_rect()
    bg = pygame.image.load("./img/bg.png").convert_alpha()
    rect_bg = bg.get_rect()
    #rect_shogaibutsu = shogaibutsu.image.get_rect()
    scroll_speed = 3
    bgx = 0
    player1 = horse_Sprite("./img/horse.png",500,420)
    #bg_group = pygame.sprite.Group()
    #bg_group.add(bg)
    #bg_group.add(shogaibutsu)
    #mae.add(goal)
    clock = pygame.time.Clock()
    while end_flag == False:
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and space_count == 0:
                    for i in range(0,3):
                        horse_y /= 1.13
                        screen.blit(player1.image,(360,horse_y))
                    #print(horse_y)
                    space_count = 1
                elif event.key == K_LSHIFT and space_count == 1: 
                    for i in range(0,3):
                        horse_y *= 1.13
                        screen.blit(player1.image,(360,horse_y))
                    #print(horse_y)
                    space_count = 0
                elif event.key == K_RSHIFT:
                    end_flag = True
                    
        #collide = pygame.Rect.colliderect(player1.rect,shogaibutsu.rect)
        #print(collide)
        #collide = player1.collide_shogaibutsu(shogaibutsu)
        #if collide:
        #    print("true")
        #    scroll_speed = 0
        #else:
        #    scroll_speed = 3
        
        
            #print(True)
        
        #print((bgx - scroll_speed) % rect_bg.width)
        bgx = (bgx - scroll_speed) % rect_bg.width
        bgx_goal = bgx + 400
        screen.blit(bg,(bgx,0))
        screen.blit(bg,(bgx - rect_bg.width,0))
        if(shogaibutsu_yoketa > 8):
            screen.blit(goal,(bgx_goal,340))
        shogaibutsu.update(bgx,0)
        shogaibutsu2.update(bgx,120)
        player1.update(way,bgx,shogaibutsu)
        player1.draw(screen,360,horse_y)
        screen.blit(shogaibutsu.image,(bgx,400))
        bgx100 = bgx +350
        screen.blit(shogaibutsu2.image,(bgx100,120))
        
        #mae.move_to_front(goal)
        pygame.display.update()
        clock.tick(60)
        #print(shogaibutsu2.x)
        #print(horse_y)
        #print(player1.y)
        #print(bgx)
        #print(bgx_goal)
        if shogaibutsu.x < 480 and shogaibutsu.x > 400 and player1.y < 321 and player1.y > 221 and player1.y != 221.77605192886264:
            scroll_speed = 0
        elif shogaibutsu2.x > 150 and shogaibutsu2.x < 200 and player1.y > 221 and player1.y == 221.77605192886264:
            scroll_speed = 0
        else:
            scroll_speed = 15
        if bgx == 12 or bgx == 2:
            shogaibutsu_yoketa += 1
            #print(shogaibutsu_yoketa)
        if bgx_goal < 700 and bgx_goal < 670 and player1.y != 221.77605192886264 and shogaibutsu_yoketa > 9:
            end_flag = True
        
    gameclear = pygame.image.load("./img/clear.png").convert_alpha()
    screen.blit(gameclear,(0,0))
    stop_time = time.time()
    result = stop_time - start_time
    result_text = font.render(str(result) + "seconds",True,(0,0,0))
    while True:
        screen.blit(result_text,(500,400))
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit
if __name__ == "__main__":
    menu()
    asyncio.run(main())