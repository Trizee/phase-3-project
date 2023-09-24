# imports 
import pygame
from sys import exit

# pygame init

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tri\'s Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('lib/font/Pixeltype.ttf', 50)
game_active = True

sky_surf = pygame.image.load('lib/graphics/Sky.png').convert()
ground_surf = pygame.image.load('lib/graphics/ground.png').convert()

score_surf = test_font.render('My Game',False,(64,64,64))
score_rect = score_surf.get_rect(center = (400,50))

snail_surf = pygame.image.load('lib/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600,300))

player_surf = pygame.image.load('lib/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -20
                        print('jump')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 300:
                        player_gravity = -20
        
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
        # if event.type == pygame.KEYUP:
        #     print('key up')
    if game_active:   
        # putting surfaces on pygame dispaly
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        
        pygame.draw.rect(screen, '#c0e8ec', score_rect,)
        pygame.draw.rect(screen, '#c0e8ec', score_rect,10)

        screen.blit(score_surf,score_rect)

        snail_rect.left -= 4
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

    else:
        screen.fill('yellow')

    pygame.display.update()
    clock.tick(60)