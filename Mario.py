import pygame, sys
from game_map import *
from settings import *
from resources import *


class Game:
    pygame.init() 
    pygame.display.set_caption("Mario")

    def __init__(self, screen_width, screen_height):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.screen_width = screen_width 
        self.screen_height = screen_height
        self.grid = Map.scene1
        self.floor_group = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()
        self.question_group = pygame.sprite.Group()
        self.question_special_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.mushroom_group = pygame.sprite.Group()
        self.goomba_group = pygame.sprite.Group()
        self.flag_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.brick_frames = Bricks_animation.bricks_frames
        self.brick_animation_active = False
        self.brick_animation_index = 0
        self.brick_animation_break_pos = (0,0)
        self.mariopowerup = False
        self.sounds = Sounds()
        self.sounds.main.play()
        self.game_scene = 1
        self.game_over = False  
        self.create_scenario()
        
    def create_scenario(self):
        self.floor_group.empty()
        self.bricks_group.empty()
        self.question_group.empty()
        self.question_special_group.empty()
        self.pipe_group.empty()
        self.player_group.empty()
        self.block_group.empty()
        self.coin_group.empty()
        self.mushroom_group.empty()
        self.goomba_group.empty()
        self.flag_group.empty()
        self.player_group.add(Player(self.screen_width, self.screen_height, self.mariopowerup)) 
       
        for row in range(ROWS):
            for column in range(COLS):
                x = column * CELL_SIZE
                y = row * CELL_SIZE
                if self.grid[row][column] == 1: 
                    block = Block_floor(x, y)  
                    self.floor_group.add(block)
                elif self.grid[row][column] == 2:
                    block = Block_brick(x, y)  
                    self.bricks_group.add(block) 
                elif self.grid[row][column] == 3:
                    block = Block_question(x, y)  
                    self.question_group.add(block) 
                elif self.grid[row][column] == 4:
                    block = Pipe(x, y)  
                    self.pipe_group.add(block)  
                elif self.grid[row][column] == 5:
                    block = Block_block(x, y)  
                    self.block_group.add(block)  
                elif self.grid[row][column] == 6:
                    block = Goomba(x, y)  
                    self.goomba_group.add(block)
                elif self.grid[row][column] == 7:
                    block = Coin(x, y)  
                    self.coin_group.add(block) 
                elif self.grid[row][column] == 8:
                    block = Block_question_special(x, y)  
                    self.question_special_group.add(block)
                elif self.grid[row][column] == 9:
                    block = Flag(x-15, y)  
                    self.flag_group.add(block)                          
                    
    def gravity(self):
        self.player_group.sprite.gravity += 1
        self.player_group.sprite.rect.y += self.player_group.sprite.gravity

        for sprite in self.goomba_group:
            sprite.gravity += 1
            sprite.rect.y += sprite.gravity

        for sprite in self.mushroom_group:
            sprite.gravity += 1
            sprite.rect.y += sprite.gravity    

    def bottom_to_top_collision(self):
           
        if self.player_group.sprite.gravity < 0: #jugador en el aire subiendo
            # bottom to top collision with bricks
            if pygame.sprite.spritecollide(self.player_group.sprite, self.bricks_group, False):
                block_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.bricks_group, True)
                self.player_group.sprite.gravity = 17
                self.sounds.brick.play()
                self.brick_animation_active = True
                self.brick_animation_break_pos = (block_temp[0].rect.x - 130, block_temp[0].rect.y - 100)
                
            # bottom to top collision with question bricks    
            if pygame.sprite.spritecollide(self.player_group.sprite, self.question_group, False):
                block_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.question_group, False)
                self.player_group.sprite.gravity = 17
                self.player_group.sprite.rect.y += 30
                self.sounds.question.play()  
                block_temp[0].image = pygame.image.load("graphics/block_question3.png")
                # coin spawn
                if not block_temp[0].hit:
                    coin = Coin(block_temp[0].rect.x,block_temp[0].rect.y - 30)
                    self.coin_group.add(coin)
                    self.sounds.coin.play()
                    block_temp[0].hit = True

            # bottom to top collision with question special bricks          
            if pygame.sprite.spritecollide(self.player_group.sprite, self.question_special_group, False):
                block_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.question_special_group, False)
                self.player_group.sprite.gravity = 17
                self.player_group.sprite.rect.y += 30
                self.sounds.question.play() 
                block_temp[0].image = pygame.image.load("graphics/block_question3.png")
                # mushroom spawn
                if not block_temp[0].hit:
                    mushroom = Mushroom(block_temp[0].rect.x - 10,block_temp[0].rect.y - 35)
                    self.sounds.mushroom.play()
                    self.mushroom_group.add(mushroom)
                    block_temp[0].hit = True    

    def top_to_bottom_collisions(self):
        for group in [self.floor_group,self.bricks_group,self.question_group,self.pipe_group,self.block_group,self.question_special_group]:
            collided_blocks = pygame.sprite.spritecollide(self.player_group.sprite, group, False)
            if collided_blocks:
                for block in collided_blocks:
                    if self.player_group.sprite.rect.bottom > block.rect.top:
                        self.player_group.sprite.rect.bottom = block.rect.top
                        self.player_group.sprite.gravity = 0
                        break

    def horizontal_collisions(self):
        if game.player_group.sprite.move_left: 
            if pygame.sprite.spritecollide(game.player_group.sprite, game.pipe_group, False):
                pipe_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.pipe_group, False)[0]
                if game.player_group.sprite.rect.bottom >= pipe_temp.rect.bottom:
                    game.player_group.sprite.rect.x += game.player_group.sprite.speed   
            if pygame.sprite.spritecollide(game.player_group.sprite, game.block_group, False):
                block_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.block_group, False)[0]
                if game.player_group.sprite.rect.bottom >= block_temp.rect.bottom:
                    game.player_group.sprite.rect.x += game.player_group.sprite.speed 
            if pygame.sprite.spritecollide(game.player_group.sprite, game.bricks_group, False):
                brick_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.bricks_group, False)[0]
                if game.player_group.sprite.rect.bottom >= brick_temp.rect.bottom:
                    game.player_group.sprite.rect.x += game.player_group.sprite.speed                            

        if game.player_group.sprite.move_right: 
            if pygame.sprite.spritecollide(game.player_group.sprite, game.pipe_group, False):
                pipe_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.pipe_group, False)[0]
                if game.player_group.sprite.rect.bottom >= pipe_temp.rect.bottom:
                    game.player_group.sprite.rect.x -= game.player_group.sprite.speed   
            if pygame.sprite.spritecollide(game.player_group.sprite, game.block_group, False):
                block_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.block_group, False)[0]
                if game.player_group.sprite.rect.bottom >= block_temp.rect.bottom:
                    game.player_group.sprite.rect.x -= game.player_group.sprite.speed  
            if pygame.sprite.spritecollide(game.player_group.sprite, game.bricks_group, False):
                brick_temp = pygame.sprite.spritecollide(game.player_group.sprite, game.bricks_group, False)[0]
                if game.player_group.sprite.rect.bottom >= brick_temp.rect.bottom:
                    game.player_group.sprite.rect.x -= game.player_group.sprite.speed                                  
        
    def coin_collision(self):
        coin_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.coin_group, True)
        if coin_temp:
            self.sounds.coin.play()

    def mario_is_in_ground(self):   
        if game.player_group.sprite.gravity == 0:
            return True
        else:
            return False        

    def mario_and_goomba_collision(self):
        goomba_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.goomba_group, False)
        # Mario kills goomba
        if goomba_temp and not self.mario_is_in_ground():
            self.sounds.kickgoomba.play()
            goomba_temp[0].kill()
            self.player_group.sprite.gravity = -9
        # Goomba kills Mario    
        if goomba_temp and self.mario_is_in_ground():
            self.sounds.death.play()
            self.sounds.main.stop()
            self.game_over = True
            
    def pit(self):
        if self.player_group.sprite.rect.bottom > SCREEN_HEIGHT + 100:
            self.sounds.death.play()
            self.sounds.main.stop()
            self.game_over = True

    def goomba_horizontal_collision(self):
        for sprite in self.goomba_group:
            if pygame.sprite.spritecollide(sprite, self.pipe_group, False):
                sprite.rect.x += sprite.speed #para evitar bug
                sprite.speed = -sprite.speed 
            elif pygame.sprite.spritecollide(sprite, self.block_group, False):
                sprite.rect.x += sprite.speed #para evitar bug
                sprite.speed = -sprite.speed  

    def goomba_vertical_collision(self):
        for sprite in self.goomba_group:
            for group in [self.floor_group,self.bricks_group,self.question_group,self.pipe_group,self.block_group]:
                collided_blocks = pygame.sprite.spritecollide(sprite, group, False)
                if collided_blocks:
                    for block in collided_blocks:
                        if sprite.rect.bottom >= block.rect.top:
                            sprite.rect.bottom = block.rect.top
                            sprite.gravity = 0
                            break 

    def mushroom_horizontal_collision(self):
        for sprite in self.mushroom_group:
            if pygame.sprite.spritecollide(sprite, self.pipe_group, False):
                sprite.rect.x -= sprite.speed #para evitar bug
                sprite.speed = -sprite.speed 
                                    
    def mushroom_vertical_collision(self):
        for sprite in self.mushroom_group:
            for group in [self.floor_group,self.bricks_group,self.question_group,self.pipe_group,self.block_group]:
                collided_blocks = pygame.sprite.spritecollide(sprite, group, False)
                if collided_blocks:
                    for block in collided_blocks:
                        if sprite.rect.bottom > block.rect.top:
                            sprite.rect.bottom = block.rect.top
                            sprite.gravity = 0
                            break        

    def mario_and_mushroom_collision(self):
        mush_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.mushroom_group, True)
      
        if mush_temp:
            self.sounds.powerup.play() 
            self.player_group.sprite.powerup = True
            self.mariopowerup = True
            self.player_group.sprite.image = pygame.image.load("graphics/bigmario.png")
            self.player_group.sprite.rect = self.player_group.sprite.image.get_rect(midbottom = (self.player_group.sprite.rect.x+15,self.screen_height - 60))
            
    def mario_and_flag_collision(self):
        flag_temp = pygame.sprite.spritecollide(self.player_group.sprite, self.flag_group, False)
      
        if flag_temp and flag_temp[0].play:
            self.sounds.main.stop()
            flag_temp[0].image = pygame.image.load("graphics/flag2.png")                              
            self.sounds.flag.play()
            flag_temp[0].play = False # para que el sonido suene una vez

    def mario_and_castle(self):   
        if self.grid == Map.scene6 and self.player_group.sprite.rect.x > SCREEN_WIDTH - 180:
            self.game_over = True
            self.sounds.finish.play()

    def brick_animation(self):
        if self.brick_animation_active:
            if self.brick_animation_index < len(self.brick_frames):
                self.screen.blit(self.brick_frames[self.brick_animation_index], self.brick_animation_break_pos)
                self.brick_animation_index += 1
            else:
                self.brick_animation_active = False
                self.brick_animation_index = 0        

    def scene_update(self):
        if self.player_group.sprite.rect.right > SCREEN_WIDTH - 20:
            if self.game_scene == 1:
                self.grid = Map.scene2
                self.create_scenario()
                self.game_scene = 2  
            elif self.game_scene == 2:
                self.grid = Map.scene3
                self.create_scenario()
                self.game_scene = 3 
            elif self.game_scene == 3:
                self.grid = Map.scene4
                self.create_scenario()
                self.game_scene = 4 
            elif self.game_scene == 4:
                self.grid = Map.scene5
                self.create_scenario()
                self.game_scene = 5 
            elif self.game_scene == 5:
                self.grid = Map.scene6
                self.create_scenario()

    def update(self):
        self.scene_update()
        self.player_group.update() 
        self.goomba_group.update()  
        self.mushroom_group.update() 
        self.coin_group.update()   
        self.question_group.update() 
        self.question_special_group.update()   

    def collisions_check(self):
        self.horizontal_collisions()
        self.gravity()   
        self.bottom_to_top_collision()  
        self.top_to_bottom_collisions()    
        self.coin_collision()
        self.mario_and_goomba_collision()
        self.pit()  
        self.goomba_horizontal_collision()
        self.goomba_vertical_collision()
        self.mushroom_horizontal_collision()
        self.mushroom_vertical_collision()
        self.mario_and_mushroom_collision()
        self.mario_and_flag_collision()
        self.mario_and_castle()
        
        
    def draw(self): 
        self.screen.fill((141,143,245)) 
        self.screen.blit(cloud, (80, 60)) 
        self.screen.blit(cloud, (SCREEN_WIDTH - 200, 30))  
        if self.grid != Map.scene5 and self.grid != Map.scene6:
            self.screen.blit(bush, (80,SCREEN_HEIGHT - CELL_SIZE*4)) 
            self.screen.blit(mountain, (SCREEN_WIDTH - 300,SCREEN_HEIGHT - CELL_SIZE*5)) 
        if self.grid == Map.scene6: 
            self.screen.blit(castle, (SCREEN_WIDTH - 300,SCREEN_HEIGHT - 223))

        self.floor_group.draw(game.screen)  
        self.bricks_group.draw(game.screen) 
        self.question_group.draw(game.screen) 
        self.question_special_group.draw(game.screen)
        self.player_group.draw(game.screen)  
        self.pipe_group.draw(game.screen) 
        self.block_group.draw(game.screen) 
        self.coin_group.draw(game.screen) 
        self.mushroom_group.draw(game.screen)  
        self.goomba_group.draw(game.screen) 
        self.flag_group.draw(game.screen)  
        self.brick_animation()  
                               



game = Game(SCREEN_WIDTH,SCREEN_HEIGHT)

while True:

    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

        if event.type == pygame.KEYDOWN:
                        
                if event.key == pygame.K_SPACE:
                    game.player_group.sprite.jump()          
                if event.key == pygame.K_RIGHT:
                    game.player_group.sprite.move_right = True
                if event.key == pygame.K_LEFT:
                    game.player_group.sprite.move_left = True
              
        if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT:
                    game.player_group.sprite.move_right = False 
                if event.key == pygame.K_LEFT:
                    game.player_group.sprite.move_left = False    
                               
    if not game.game_over:
        game.update()
        game.collisions_check()
        game.draw()   

    pygame.display.update()
    game.clock.tick(60)

