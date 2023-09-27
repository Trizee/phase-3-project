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

    # timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer,900)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return score
                          
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 300:
                        player_gravity = -20
        

        # if event.type == pygame.KEYUP:
        #     print('key up')
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
            pygame.quit()
            return score
        
        score = display_score()
        # if event.type == obstacle_timer and game_active:
        #     print('true') 
        pygame.display.update()
        clock.tick(60)

