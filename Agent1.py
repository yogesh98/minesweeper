import pygame
import time
from minesweeper import Minesweeper
from knowledgebase import A1 as KB

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 00)
GREEN = (0, 250, 0)
BLUE = (0, 0, 255)

ORIGIN = (0, 0)

pygame.init()
screen_size = 960
screen = pygame.display.set_mode((screen_size, screen_size))
screen.fill(WHITE)
pygame.display.flip()
pygame.event.get()

kb = None

def agent1(game):
    global kb

    #initializing knowledge base
    kb = KB(game)

    pass


def game_update(game):
    game_updated = game.draw(screen_size)
    screen.fill(WHITE)
    pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, ORIGIN)
    pygame.display.update()

if __name__ == '__main__':

    size = 30
    game = Minesweeper(size, 70)
    agent1(game)
    game_update(game)
    for i in range(size):
        for x in range(size):
            game.query(i, x)
    game_update(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()
    quit()