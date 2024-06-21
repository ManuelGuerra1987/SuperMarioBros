import pygame
from resources import Sounds

class Player(pygame.sprite.Sprite):
    def __init__(self, game, screen_width, screen_height, powerup: bool):
        super().__init__()
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gravity = 0
        if not powerup:
            self.image = pygame.image.load("graphics/smallmario.png")
        elif powerup:
            self.image = pygame.image.load("graphics/bigmario.png")
        self.rect = self.image.get_rect(midbottom = (40,self.screen_height - 60))            
        self.speed = 4
        self.image_ready = True
        self.image_time = 0
        self.image_delay = 100
        self.image_state = 1
        self.previous_position = self.rect.topleft
        self.powerup = powerup
        self.move_right = False
        self.move_left = False
        self.jump_sound = Sounds.jump
     
    def constrain_movement(self):
        if self.rect.left < 0:
            self.rect.left = 0  

    def is_moving(self):
        if self.rect.topleft != self.previous_position:
            self.previous_position = self.rect.topleft
            return True
        return False
    
    def jump(self):
        if self.gravity == 0:
            self.gravity = -16
            self.jump_sound.play()

    def movement(self):
        if self.move_left: 
            self.rect.x -= self.speed 
            #pipe horizontal collision:
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.pipe_group, False):
                self.rect.x += self.speed
            #block horizontal collision:    
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.block_group, False):
                self.rect.x += self.speed
            #brick horizontal collision:    
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.bricks_group, False):
                self.rect.x += self.speed    
                            
        if self.move_right: 
            self.rect.x += self.speed  
            #pipe horizontal collision:
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.pipe_group, False):
                self.rect.x -= self.speed
            #block horizontal collision:    
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.block_group, False):
                self.rect.x -= self.speed    
            if pygame.sprite.spritecollide(self.game.player_group.sprite, self.game.bricks_group, False):
                self.rect.x -= self.speed         

    def animation(self):

        if not self.powerup:
            if not self.image_ready:
                current_time = pygame.time.get_ticks()   
                if current_time - self.image_time >= self.image_delay:
                    self.image_ready = True 

            if self.gravity < 0:
                self.image = pygame.image.load("graphics/smallmariojump.png")
            elif not self.is_moving():
                self.image = pygame.image.load("graphics/smallmario.png")

            elif self.image_ready:
                self.image_ready = False
                if self.image_state == 1:
                    self.image = pygame.image.load("graphics/smallmariorun1.png")  
                    self.image_state = -self.image_state 
                    self.image_time = pygame.time.get_ticks()  
                elif self.image_state == -1:
                    self.image = pygame.image.load("graphics/smallmariorun2.png")
                    self.image_state = -self.image_state       
                    self.image_time = pygame.time.get_ticks() 

        elif self.powerup:
            
            if not self.image_ready:
                current_time = pygame.time.get_ticks()   
                if current_time - self.image_time >= self.image_delay:
                    self.image_ready = True 

            if self.gravity < 0:
                self.image = pygame.image.load("graphics/bigmariojump.png")
            elif not self.is_moving():
                self.image = pygame.image.load("graphics/bigmario.png")
                

            elif self.image_ready:
                self.image_ready = False
                if self.image_state == 1:
                    self.image = pygame.image.load("graphics/bigmariorun1.png")  
                    self.image_state = -self.image_state 
                    self.image_time = pygame.time.get_ticks()  
                elif self.image_state == -1:
                    self.image = pygame.image.load("graphics/bigmariorun2.png")
                    self.image_state = -self.image_state       
                    self.image_time = pygame.time.get_ticks()                      

    def update(self):  
        self.movement()
        self.constrain_movement() 
        self.animation()   