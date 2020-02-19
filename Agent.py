import pygame
from minesweeper import Minesweeper

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 00)
GREEN = (0, 250, 0)
BLUE = (0, 0, 255)

ORIGIN = (0,0)

pygame.init()
screen = pygame.display.set_mode((100, 100))
screen.fill(WHITE)
pygame.display.flip()
pygame.event.get()



if __name__ == '__main__':

    game = Minesweeper(30, 50)
    game_update = game.draw()
    pygame.display.set_mode(game_update.get_size())
    screen.blit(game_update, ORIGIN)
    pygame.display.update()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


