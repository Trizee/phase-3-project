# imports 
import pygame
from sys import exit
from random import randint
from pygame import mixer

# pygame init


def game():
    def display_score():
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
        score_rect = score_surf.get_rect(center = (400,50))
        screen.blit(score_surf,score_rect)
        return current_time
    
    
    def obstacle_movement(obstacle_rect_list):
        if obstacle_rect_list:
            for obstacle_rect in obstacle_rect_list:
                obstacle_rect.x -= 5

                if obstacle_rect.bottom == 300:
                    screen.blit(snail_surf,obstacle_rect)
                else:
                    screen.blit(fly_surf,obstacle_rect)
            
            obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x > -100]

            return obstacle_rect_list
        else: return []

    def collisions(player,obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect):
                    return False
        return True
    
    pygame.init()
    screen = pygame.display.set_mode((800,400))
    pygame.display.set_caption('Tri\'s Game')
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('lib/font/Pixeltype.ttf', 50)
    game_active = False
    start_time = 0
    score = 0
    
    # music

    sky_surf = pygame.image.load('lib/graphics/Sky.png').convert()
    ground_surf = pygame.image.load('lib/graphics/ground.png').convert()

    snail_surf = pygame.image.load('lib/graphics/snail/snail1.png').convert_alpha()
    fly_surf = pygame.image.load('lib/graphics/Fly/Fly1.png').convert_alpha()

    obstacle_rect_list = []

    player_walk1 = pygame.image.load('lib/graphics/Player/player_walk_1.png').convert_alpha()
    player_walk2 = pygame.image.load('lib/graphics/Player/player_walk_2.png').convert_alpha()
    player_walk = [player_walk1,player_walk2]
    player_index = 0
    player_jump = pygame.image.load('lib/graphics/Player/jump.png').convert_alpha()
    player_surf = player_walk[player_index]
    player_rect = player_surf.get_rect(midbottom = (80,300))
    player_gravity = 0

    player_stand = pygame.image.load('lib/graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,2)
    player_stand_rect = player_stand.get_rect(center = (400,200))

    game_name = test_font.render('Pixel Runner',False,(111,196,169))
    game_name_rect = game_name.get_rect(center = (400,70))

    game_message = test_font.render('Press Space To Play',False,(111,196,169))
    game_message_rect = game_message.get_rect(center = (400,340))

    end_game_message = test_font.render('Thank You For Playing',False,(111,196,169))
    end_game_message_rect = game_message.get_rect(center = (400,340))

    # timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer,1500)


    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return score

            if game_active:               
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player_rect.bottom == 300:
                            player_gravity = -20
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos):
                        if player_rect.bottom == 300:
                            player_gravity = -20
                if event.type == obstacle_timer and game_active:
                    if randint(0,1):
                        obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                    else:
                        obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),175)))
        
            else:
                if score == 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_active = True
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.quit()
                            return score
        # if event.type == pygame.KEYUP:
        #     print('key up')
        # putting surfaces on pygame dispaly
        if game_active:
            
            #Set preferred volume


            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,300))
            

            # snail_rect.left -= 5
            # if snail_rect.left < -50:
            #     snail_rect.left = 850
            # screen.blit(snail_surf,snail_rect)

            # player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300: player_rect.bottom = 300
            screen.blit(player_surf,player_rect)

            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            # collision
            # if player_rect.colliderect(snail_rect):
            #     pygame.quit()
            #     return score
            score = display_score()

            game_active = collisions(player_rect,obstacle_rect_list)
            
            
        
        else:
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            screen.blit(game_name,game_name_rect)
            if score == 0:
                screen.blit(game_message,game_message_rect)
            else:
                screen.blit(end_game_message,end_game_message_rect)
        # if event.type == obstacle_timer and game_active:
        #     print('true') 
        pygame.display.update()
        clock.tick(60)

