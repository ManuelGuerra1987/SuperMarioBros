import pygame
pygame.init() 

cloud = pygame.image.load("graphics/cloud.png")
bush = pygame.image.load("graphics/bush.png")
mountain = pygame.image.load("graphics/mountain.png")
castle = pygame.image.load("graphics/castle.png")


class Block_floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/block_floor.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 

class Block_brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/block_brick.png")
        self.rect = self.image.get_rect(topleft = (x, y))

class Block_question(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/blockquestion1.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 
        self.hit = False
        self.image_ready = True
        self.image_time = 0
        self.image_delay = 300
        self.image_state = 1 

    def animation(self):        
        if not self.image_ready:
            current_time = pygame.time.get_ticks()   
            if current_time - self.image_time >= self.image_delay:
                self.image_ready = True 

        elif self.image_ready and not self.hit:
            self.image_ready = False
            if self.image_state == 1:
                self.image = pygame.image.load("graphics/blockquestion1.png")  
                self.image_state = -self.image_state 
                self.image_time = pygame.time.get_ticks()  
            elif self.image_state == -1:
                self.image = pygame.image.load("graphics/blockquestion2.png")
                self.image_state = -self.image_state       
                self.image_time = pygame.time.get_ticks()          

    def update(self):
        self.animation()    

class Block_question_special(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/blockquestion1.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 
        self.hit = False  
        self.image_ready = True
        self.image_time = 0
        self.image_delay = 300
        self.image_state = 1 

    def animation(self):        
        if not self.image_ready:
            current_time = pygame.time.get_ticks()   
            if current_time - self.image_time >= self.image_delay:
                self.image_ready = True 

        elif self.image_ready and not self.hit:
            self.image_ready = False
            if self.image_state == 1:
                self.image = pygame.image.load("graphics/blockquestion1.png")  
                self.image_state = -self.image_state 
                self.image_time = pygame.time.get_ticks()  
            elif self.image_state == -1:
                self.image = pygame.image.load("graphics/blockquestion2.png")
                self.image_state = -self.image_state       
                self.image_time = pygame.time.get_ticks()          

    def update(self):
        self.animation()           

class Block_block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/block_block.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/pipe.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/flag.png")
        self.rect = self.image.get_rect(topleft = (x, y))   
        self.play = True  

class Bricks_animation():
    frame1 = pygame.image.load("graphics/bricks_animation1.png")
    frame2 = pygame.image.load("graphics/bricks_animation2.png")
    frame3 = pygame.image.load("graphics/bricks_animation3.png")
    frame4 = pygame.image.load("graphics/bricks_animation4.png")
    frame5 = pygame.image.load("graphics/bricks_animation5.png")
    frame6 = pygame.image.load("graphics/bricks_animation6.png")
    frame7 = pygame.image.load("graphics/bricks_animation7.png")
    frame8 = pygame.image.load("graphics/bricks_animation8.png")  
    bricks_frames = [frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8]  
           
class Sounds():
    main = pygame.mixer.Sound("sound/main_theme.ogg")
    coin = pygame.mixer.Sound("sound/coin.ogg")
    mushroom = pygame.mixer.Sound("sound/mushroom.ogg") 
    brick = pygame.mixer.Sound("sound/brick_smash.ogg")
    question = pygame.mixer.Sound("sound/question_brick_smash.ogg")
    jump = pygame.mixer.Sound("sound/jump.ogg")
    powerup = pygame.mixer.Sound("sound/powerup.ogg")
    death = pygame.mixer.Sound("sound/death.wav")
    kickgoomba = pygame.mixer.Sound("sound/kick.ogg")
    flag = pygame.mixer.Sound("sound/flag.wav")
    finish = pygame.mixer.Sound("sound/stage_clear.wav")         

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/mushroom.png")
        self.rect = self.image.get_rect(topleft = (x, y))   
        self.speed = 2 
        self.gravity = 0   

    def constrain_movement(self):
        if self.rect.left < 0:
            self.kill()     

    def update(self):
        self.rect.x += self.speed 
        self.constrain_movement()                        

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/goomba.png")
        self.rect = self.image.get_rect(topleft = (x, y)) 
        self.speed = 2 
        self.gravity = 0
        self.image_ready = True
        self.image_time = 0
        self.image_delay = 200
        self.image_state = 1

    def constrain_movement(self):
        if self.rect.left < 0:
            self.kill()   

    def animation(self):        
        if not self.image_ready:
            current_time = pygame.time.get_ticks()   
            if current_time - self.image_time >= self.image_delay:
                self.image_ready = True 

        elif self.image_ready:
            self.image_ready = False
            if self.image_state == 1:
                self.image = pygame.image.load("graphics/goomba.png")  
                self.image_state = -self.image_state 
                self.image_time = pygame.time.get_ticks()  
            elif self.image_state == -1:
                self.image = pygame.image.load("graphics/goomba2.png")
                self.image_state = -self.image_state       
                self.image_time = pygame.time.get_ticks()          

    def update(self):
        self.rect.x -= self.speed 
        self.constrain_movement() 
        self.animation()  

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/coin.png")
        self.rect = self.image.get_rect(topleft = (x, y))    
        self.image_ready = True
        self.image_time = 0
        self.image_delay = 200
        self.image_state = 1  

    def animation(self):        
        if not self.image_ready:
            current_time = pygame.time.get_ticks()   
            if current_time - self.image_time >= self.image_delay:
                self.image_ready = True 

        elif self.image_ready:
            self.image_ready = False
            if self.image_state == 1:
                self.image = pygame.image.load("graphics/coin.png")  
                self.image_state = -self.image_state 
                self.image_time = pygame.time.get_ticks()  
            elif self.image_state == -1:
                self.image = pygame.image.load("graphics/coin2.png")
                self.image_state = -self.image_state       
                self.image_time = pygame.time.get_ticks()          

    def update(self):
        self.animation()       