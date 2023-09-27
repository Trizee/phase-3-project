# imports 
import pygame
from sys import exit

# pygame init
global_score = 0 
def return_score():
    return global_score

def game():
    def display_score():
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
        score_rect = score_surf.get_rect(center = (400,50))
        screen.blit(score_surf,score_rect)
        return current_time

    pygame.init()
    screen = pygame.display.set_mode((800,400))
    pygame.display.set_caption('Tri\'s Game')
    clock = pygame.time.Clock()
    test_font = pygame.font.Font('lib/font/Pixeltype.ttf', 50)
    game_active = False
    start_time = 0
    score = 0


    sky_surf = pygame.image.load('lib/graphics/Sky.png').convert()
    ground_surf = pygame.image.load('lib/graphics/ground.png').convert()

    snail_surf = pygame.image.load('lib/graphics/snail/snail1.png').convert_alpha()
    snail_rect = snail_surf.get_rect(midbottom = (600,300))

    player_surf = pygame.image.load('lib/graphics/Player/player_walk_1.png').convert_alpha()
    player_rect = player_surf.get_rect(midbottom = (80,300))
    player_gravity = 0

    # intro Screen
    player_stand = pygame.image.load('lib/graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,2)
    player_stand_rect = player_stand.get_rect(center = (400,200))

    game_name = test_font.render('Pixel Runner',False,(111,196,169))
    game_name_rect = game_name.get_rect(center = (400,70))

    game_message = test_font.render('Press Space To Play',False,(111,196,169))
    game_message_rect = game_message.get_rect(center = (400,330))

    # timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer,900)


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
            
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        snail_rect.left = 800
                        start_time = int(pygame.time.get_ticks() / 1000)
            # if event.type == pygame.KEYUP:
            #     print('key up')
        if game_active:   
            # putting surfaces on pygame dispaly
            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,300))
            

            snail_rect.left -= 5
            if snail_rect.left < -50:
                snail_rect.left = 850
            screen.blit(snail_surf,snail_rect)

            # player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300: player_rect.bottom = 300
            screen.blit(player_surf,player_rect)

            # collision
            if player_rect.colliderect(snail_rect):
                game_active = False
                game_message = test_font.render(f'Final Score: {score}',False,(111,196,169))
            
            score = display_score()
            global_score = score
            # if event.type == obstacle_timer and game_active:
            #     print('true') 

        else:
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)

        pygame.display.update()
        clock.tick(60)

