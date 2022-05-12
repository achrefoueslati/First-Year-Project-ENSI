import sys
import random 
from random import randint
import pickle
import time 
import pygame
from pygame.locals import *
from pygame import mixer
from os import path 



pygame.mixer.pre_init(44100 , -16 , 2 , 512)
mixer.init()
pygame.init()
#machekel fps 
clock = pygame.time.Clock()
fps = 80
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Super Learn')

#font 
font = pygame.font.SysFont('Bauhaus 93 ' , 70)
font_score = pygame.font.SysFont('Bauhaus 93 ' , 30 )
font1 = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 24)

#color 
white = (255 , 255 , 255)
blue = (0 , 0 , 255 )
black = (0 , 0 , 0)
cyan = (0, 255 , 255)
yellow = (255 , 255 , 0)
purple = (255 , 0 , 255)
green = (0 , 255 , 0)
red = (255 , 0 , 0)

#some game variables
tile_size = 30
game_over = 0 
main_menu = True
level = 1
max_levels = 7
coin_score_count = 0 
triviabool_gameover = False
triviatime = False
savecor_x = 0
savecor_y = 0 
triviafail = False
randlist = []
nb = 1



#loading images :
bg = pygame.image.load('img/bgimg.jpg')
bgimg = pygame.transform.scale(bg,(600,600))
qbg1 = pygame.image.load('img/qbg1.png')
qbg2L = pygame.image.load('img/qbg2.png')
qbg2 = pygame.transform.scale(qbg2L,(600,600))
qbg3L = pygame.image.load('img/qbg3.png')
qbg3 = pygame.transform.scale(qbg3L,(600,600))
qbg4L = pygame.image.load('img/qbg4.png')
qbg4 = pygame.transform.scale(qbg4L,(600,600))
qbg5L = pygame.image.load('img/qbg5.png')
qbg5 = pygame.transform.scale(qbg5L,(600,600))
qbg6L = pygame.image.load('img/qbg6.png')
qbg6 = pygame.transform.scale(qbg6L,(600,600))


idle_spritesheet_image = pygame.image.load('img/Idle.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png')
startim = pygame.image.load('img/start_btn.png')
start_img = pygame.transform.scale(startim, (210,100))
exim = pygame.image.load('img/exit_btn.png')
exit_img = pygame.transform.scale(exim, (210,100))


#loading sounds :
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1,0.0,5000) 
coin_sound = pygame.mixer.Sound('img/coin.wav')
coin_sound.set_volume(0.3)
jump_sound = pygame.mixer.Sound('img/jump.wav')
jump_sound.set_volume(0.3)
gameover_sound = pygame.mixer.Sound('img/game_over.wav')
gameover_sound.set_volume(0.3)

#-----------------------------------------------------------------------
#                             FUNCTIONS       
#-----------------------------------------------------------------------

#draw text function
def draw_text(text , font ,text_col , x , y ) : 
    img = font.render(text , True , text_col)
    screen.blit(img , (x ,y) )

#fonction next/reset level 
def reset_level(level) : 
    player.reset(50 , screen_height - 80 )
    #clearing old levels
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    door_group.empty()
    if path.exists(f'Data_Files/level{level}_data') : 
        pickle_in = open(f'Data_Files/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world

#fonction next/reset level 
def reset_trivia(level) : 
    trivia = Trivia(f"Trivia_Files/testtrivia{level}.txt")
    return trivia

#print text function
def print_text(font, x, y, text, color=(255,255,255), shadow=True):
    if shadow:
        imgText = font.render(text, True, (0,0,0))
        screen.blit(imgText, (x-2,y-2))
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#check if a number is in a list 
def cointains(nb,list) : 
    bool = False
    for i in range(len(list)) : 
        if i == nb : 
            return True
    return False

#-----------------------------------------------------------------------
#                             CLASSES       
#-----------------------------------------------------------------------

#spritesheet class : 
class SpriteSheet() : 
    def __init__(self , image):
        self.sheet = image

#Loading spritesheets 
    def get_image(self, frame , width , height , scale , colour) :
        image = pygame.Surface((width , height )).convert_alpha()
        image.blit(self.sheet , (0,0) , ((frame * width) , 0 , width , height))
        image = pygame.transform.scale (image , (width * scale , height * scale))
        image.set_colorkey(colour)
        return image

#button class : 
class Button():
    def __init__(self,x,y,image) : 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.clicked = False

    def draw(self) : 
        action = False 
        #get mouse position 
        pos =pygame.mouse.get_pos()
        
        #check mouseover and click 
        if self.rect.collidepoint(pos) : 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False : 
                action = True
                self.clicked = True 

        if pygame.mouse.get_pressed()[0] == 0 :
            self .clicked = False
        
        #draw button
        screen.blit(self.image,self.rect)
        return action



#player class 
class Player():
    def __init__(self,x,y):
        self.reset(x,y)


    def update(self,game_over):
        #variables 
        dx = 0
        dy = 0 
        walk_cooldown = 5
        col_max = 20 
        idle_check = True
        
        if game_over == 0 : 
            #get keypress
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jump == False and self.in_air == False :
                jump_sound.play()
                self.vel_y = -15
                self.jump = True
            if key[pygame.K_SPACE] == False :
                self.jump = False
            if key[pygame.K_LEFT] :
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT] : 
                dx += 3
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False :
                self.counter = 0 
                self.index = 0
                if self.direction == 1 :
                    self.image = self.images_right[self.index]
                if self.direction == -1 :
                    self.image = self.images_left[self.index]

            #idle animation 
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.idle_cooldown : 
                self.frame += 1 
                self.last_update = current_time
                if self.frame >= len(self.idle_list ) : 
                    self.frame = 0    
            
            
            #animation 
            if self.counter > walk_cooldown :
                self.counter = 0 
                self.index += 1
                if self.index >= len(self.images_right) : 
                    self.index = 0 
                if self.direction == 1 :
                    self.image = self.images_right[self.index]
                if self.direction == -1 :
                    self.image = self.images_left[self.index] 
            
            
            
            #gravity ??
            self.vel_y += 1
            if (self.vel_y > 10) :
                self.vel_y = 10 
            dy += self.vel_y
            
            #cas d'obstacle (collision)
            self.in_air = True
            for tile in world.tile_list : 
                #collision in x axe 
                if tile[1].colliderect(self.rect.x + dx ,self.rect.y , self.width , self.height) : 
                    dx = 0
                #collision sur l'axe y 
                if tile[1].colliderect(self.rect.x , self.rect.y + dy , self.width , self.height) : 
                    if self.vel_y < 0 :
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0 
                    elif self.vel_y >= 0 : 
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0 
                        self.in_air = False 
            
            #check for collision with ennemies: 
            if pygame.sprite.spritecollide(self,blob_group,False) : 
                game_over = -1
                gameover_sound.play()
            #check for collision with lava : 
            if pygame.sprite.spritecollide(self,lava_group,False) : 
                game_over = -1
                gameover_sound.play()
            #door teleport :
            if pygame.sprite.spritecollide(self,door_group,False) : 
                    game_over = 1

            #check for collision with moving platforms : 
            for platform in platform_group : 
                #collision in x axe : 
                if platform.rect.colliderect(self.rect.x + dx ,self.rect.y , self.width , self.height) : 
                    dx = 0 
                #collision in y axe : 
                if platform.rect.colliderect(self.rect.x  ,self.rect.y + dy , self.width , self.height) : 
                    #check if below platform (jey melouta) 
                    if abs((self.rect.top + dy ) - platform.rect.bottom) < col_max :
                        self.vel_y = 0 
                        dy = platform.rect.bottom - self.rect.top
                    #check if over platform (jey melfouk)
                    elif abs((self.rect.bottom + dy ) - platform.rect.top) < col_max :
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False 
                        dy = 0 
                    #move with the platform (aal ajneb )
                    if platform.move_x != 0 :
                        self.rect.x += platform.move_direction 

           #update coor
            self.rect.x += dx
            self.rect.y += dy
        
        elif game_over == -1 : 
            if triviafail == False : 
                self.image = self.dead_image
                draw_text('GAME OVER !' , font , white , (screen_width // 2) - 150 , screen_height // 2 - 50  )
                self.rect.y -= 5 
            else : 
                print_text(font1, 150, 100, "You Failed The Trivia ! ", red )
                print_text(font1, 150, 190,  "Better Luck Next Time ! ", red )
        
        
        #draw player on screen
        #if idle_check == True : 
        #    screen.blit(self.idle_list[self.frame],(self.rect.x , self.rect.y - 5 ))
        #else :
        screen.blit(self.image,self.rect)
        return game_over

    #reset player
    def reset(self,x,y) :
        self.idle_list = []
        self.idle_steps = 13
        self.last_update = pygame.time.get_ticks()
        self.idle_cooldown = 75
        self.frame = 0  
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0 
        
        
        for i in range (1,13) :    
            img_right = pygame.image.load(f'img/frog{i}.png')
            img_right = pygame.transform.scale(img_right, (26,28) )
            img_left = pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0 
        self.jump = False
        self.direction = 0
        self.in_air = True
        for i in range(self.idle_steps) : 
            self.idle_list.append(idle_spritesheet.get_image(i , 32 , 32 , 1.5 , black ))

        

        

#classes for worlds
class World():
    def __init__(self,data):
        self.tile_list = []
        
        
        #load world images
        dirt_img = pygame.image.load('img/dirt.png') 
        grass_img = pygame.image.load('img/grass.png')
        bordervert_img = pygame.image.load('img/bordervert.png')
        
        row_count = 0
        for row in data :
            col_count = 0 
            for tile in row :
                if tile == 1 : 
                    img = pygame.transform.scale(dirt_img, (tile_size + 3,tile_size + 3))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2 : 
                    img = pygame.transform.scale(grass_img, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 3 : 
                    blob = Enemy(col_count * tile_size + 15 , row_count * tile_size + 15 )
                    blob_group.add(blob)
                if tile == 4 : 
                    platform = Platform(col_count * tile_size , row_count * tile_size , 1 , 0)  
                    platform_group.add(platform)
                if tile == 5 : 
                    platform = Platform(col_count * tile_size , row_count * tile_size , 0 , 1 )
                    platform_group.add(platform)
                if tile == 6 : 
                    lava = Lava(col_count * tile_size , row_count * tile_size + (tile_size // 2 ))
                    lava_group.add(lava)
                if tile == 7 :
                    coin = Coin(col_count * tile_size + (tile_size // 2) ,  row_count * tile_size + (tile_size // 2 ))
                    coin_group.add(coin)
                if tile == 8 : 
                    door = Door(col_count * tile_size ,  row_count * tile_size - (tile_size // 2 ))
                    door_group.add(door)
                if tile == 9 : 
                    img = pygame.transform.scale(bordervert_img(tile_size,tile_size))
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    
    
    def draw(self) : 
        for tile in self.tile_list :
            screen.blit(tile[0],tile[1])

#class ennemy
class Enemy(pygame.sprite.Sprite) : 
    def __init__(self,x,y) : 
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/blob.png')
        self.image = pygame.transform.scale(img , (tile_size // 1.5, tile_size // 2 ))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y   
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction 
        self.move_counter += 1 
        if abs(self.move_counter) > 50 : 
            self.move_direction *= -1
            self.move_counter *= -1


#class plateforme 
class Platform(pygame.sprite.Sprite) : 
    def __init__(self,x,y,move_x,move_y) : 
        pygame.sprite.Sprite.__init__(self)  
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img , (tile_size , tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.move_counter = 0
        self.move_direction = 1
       #binaire 
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1 
            if abs(self.move_counter) > 50 : 
                self.move_direction *= -1
                self.move_counter *= -1  

#class lava 
class Lava(pygame.sprite.Sprite) : 
    def __init__(self,x,y) : 
        pygame.sprite.Sprite.__init__(self)  
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img ,(tile_size , tile_size // 2 ))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y  
 
#class door
class Door(pygame.sprite.Sprite) : 
    def __init__(self,x,y) : 
        pygame.sprite.Sprite.__init__(self)  
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img ,(tile_size , int(tile_size * 1.5 )))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y  

#class coin 
class Coin(pygame.sprite.Sprite) : 
    def __init__(self,x,y) : 
        pygame.sprite.Sprite.__init__(self)  
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img ,(tile_size // 2 , tile_size // 2 ))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

#class Trivia 
class Trivia(object):
    def __init__(self, filename):
        self.data = []
        self.current = 0
        self.total = 0
        self.correct = 0
        self.score = 0
        self.scored = False
        self.failed = False
        self.wronganswer = 0
        self.colors = [white,white,white,white]

        
        
        #read trivia data from file
        f = open (filename, "r")
        trivia_data = f.readlines()
        f.close()

        #count and clean up trivia data
        for text_line in trivia_data:
            self.data.append(text_line.strip())
            self.total += 1

    def show_question(self):
        print_text(font1, 210, 5, "TRIVIA TIME")
        print_text(font2, 100, 500-20, "Appuyez sur les touches (1-4) pour repondre", cyan)
        print_text(font2, 530, 5, "SCORE", cyan)
        print_text(font2, 550, 25, str(self.score), cyan)
        print_text(font2, 20, 50, "Attention ! Il faut au moins un score de 2/4 pour avancer !", red)
        #get correct answer out of data (first)
        self.correct = int(self.data[self.current+5])

        #display question
        question = self.current // 6 + 1
        print_text(font1, 5, 80, "QUESTION " + str(question))
        print_text(font2, 20, 120, self.data[self.current], yellow)

        #respond to correct answer
        if self.scored:
            self.colors = [white,white,white,white]
            self.colors[self.correct-1] = green
            print_text(font1, 230, 380, "BINGO!", green)
            print_text(font2, 100, 420, "Appuyez sur Entree pour la question suivante ", green)
        elif self.failed:
            self.colors = [white,white,white,white]
            self.colors[self.wronganswer-1] = red
            self.colors[self.correct-1] = green
            print_text(font1, 220, 380, "INCORRECT!", red)
            print_text(font2, 100, 420, "Appuyez sur Entree pour la question suivante", red)

        #display answers
        print_text(font1, 5, 170, "REPONSES")
        print_text(font2, 20, 210, "1 - " + self.data[self.current+1], self.colors[0])
        print_text(font2, 20, 240, "2 - " + self.data[self.current+2], self.colors[1])
        print_text(font2, 20, 270, "3 - " + self.data[self.current+3], self.colors[2])
        print_text(font2, 20, 300, "4 - " + self.data[self.current+4], self.colors[3])

    def handle_input(self,number):
        if not self.scored and not self.failed:
            if number == self.correct:
                self.scored = True
                self.score += 1
            else:
                self.failed = True
                self.wronganswer = number

    

    def next_question(self):
        if self.scored or self.failed:
            self.scored = False
            self.failed = False
            self.correct = 0
            self.colors = [white,white,white,white]
            self.current += 6
            if self.current >= self.total:
                return True
            else:
                return False


        

#--------------------------------------------------------------------------------------
#                              GROUPS INITIALISATION
#--------------------------------------------------------------------------------------
idle_spritesheet = SpriteSheet(idle_spritesheet_image)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
player = Player(50 , screen_height - 80 )
#coin icon for score 
score_coin = Coin(tile_size // 2 , tile_size // 2 )
coin_group.add(score_coin)

#--------------------------------------------------------------------------------------
#                              LOADING DATA
#--------------------------------------------------------------------------------------

#load trivia data 
trivia = Trivia(f"Trivia_Files/testtrivia{level}.txt")
#loading levels data
if path.exists(f'Data_Files/level{level}_data') : 
    pickle_in = open(f'Data_Files/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#--------------------------------------------------------------------------------------
#                              lOADING BUTTONS
#--------------------------------------------------------------------------------------

#buttons : 
restart_button = Button(screen_width // 2 - 50 , screen_height // 2 + 30 ,restart_img)
start_button = Button(screen_width // 2 - 250 , screen_height // 2 , start_img)
exit_button = Button(screen_width // 2 + 50 , screen_height // 2 , exit_img)


#--------------------------------------------------------------------------------------
#                              GAME LOOP
#--------------------------------------------------------------------------------------

run = True 
while run :
    clock.tick(fps)
    if triviatime == False :
        screen.blit(bgimg,(0,0))
        if main_menu == True : 
            if exit_button.draw() : 
                run = False
            if start_button.draw() :
                main_menu = False
        else : 
            world.draw()
            if game_over == 0 :
                blob_group.update()
                platform_group.update()
                draw_text('Level ' + str(level), font_score, white, screen_width - 75, 10)
                #score
                #check if a coin is collected 
                if pygame.sprite.spritecollide(player , coin_group , True) : 
                    coin_score_count += 1 
                    coin_sound.play()
                draw_text('X ' + str(coin_score_count) , font_score , white , tile_size  , 7 )
            blob_group.draw(screen)
            platform_group.draw(screen)
            lava_group.draw(screen)
            door_group.draw(screen)
            coin_group.draw(screen)
            game_over = player.update(game_over)

            #if player dies or fails trivia  
            if game_over == -1 :
                if restart_button.draw() :    
                    if triviafail : 
                        level -= 1 
                    world_data = []
                    world = reset_level(level)
                    game_over = 0 
                    coin_score_count = 0 
            
            #if player completes level 
            if game_over == 1 :
                #go to next level 
                savecor_x = player.rect.x
                savecor_y = player.rect.y
                triviatime = True
                level += 1
                if level <= max_levels : 
                    #next level
                    world_data = []
                    world = reset_level(level)
                    trivia = reset_trivia(level - 1 )
                    game_over = 0     
                else : 
                    draw_text( 'YOU WON ! ! !' , font , white  , (screen_width // 2 ) - 130 , screen_height // 2 - 100 )
                    #restart game
                    if restart_button.draw() :     
                        level = 1 
                        world_data = []
                        world = reset_level(level)
                        game_over = 0 
                        coin_score_count = 0 
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            run = False
        if (triviatime == True and level <7 ) : 
            if event.type == KEYUP :
                if event.key == pygame.K_1:
                    trivia.handle_input(1)
                elif event.key == pygame.K_2:
                    trivia.handle_input(2)
                elif event.key == pygame.K_3:
                    trivia.handle_input(3)
                elif event.key == pygame.K_4:
                    trivia.handle_input(4)
                elif event.key == pygame.K_RETURN:
                    triviabool_gameover = trivia.next_question()
                if triviabool_gameover:
                    triviatime = False
                    trivia.current = 0
                    triviabool_gameover = False
                    if trivia.score < 2 :
                        triviafail = True
                        game_over = -1 
                    else :
                        coin_score_count += trivia.score
                        triviafail = False 
            if not triviabool_gameover:
                if level == 2 : 
                    screen.blit(qbg1,(0,0))
                elif level == 3 :
                    screen.blit(qbg2,(0,0))
                elif level == 4 :
                    screen.blit(qbg3,(0,0))
                elif level == 5 :
                    screen.blit(qbg4,(0,0))
                elif level == 6 :
                    screen.blit(qbg5,(0,0))
                elif level == 7 :
                    screen.blit(qbg6,(0,0))
                screen.blit(player.image,(savecor_x,savecor_y))
                trivia.show_question()


    pygame.display.update()

pygame.quit()