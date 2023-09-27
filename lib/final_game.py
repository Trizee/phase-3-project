import pygame
from sys import exit
from random import randint

def game():

    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('TriGame')
    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
        
game()
