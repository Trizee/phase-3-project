# imports 
import pygame
from sys import exit

# pygame init

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Tri\'s Game')
clock = pygame.time.Clock()

test_surface = pygame.Surface((100,200))
test_surface.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(test_surface,(400,200))

    pygame.display.update()
    clock.tick(60)