# imports 
import pygame
from sys import exit

# pygame init

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tri\'s Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('lib/font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('lib/graphics/Sky.png').convert()
ground_surface = pygame.image.load('lib/graphics/ground.png').convert()
text_surface = test_font.render('My Game',False,'Black').convert()

snail_surface = pygame.image.load('lib/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load('lib/graphics/Player/player_walk_1.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(350,50))
    snail_rect.left -= 3
    if snail_rect.left < -50:
        snail_rect.left = 850
    screen.blit(snail_surface,snail_rect)
    # print(player_rectangle.left)
    screen.blit(player_surface,player_rectangle)

    pygame.display.update()
    clock.tick(60)