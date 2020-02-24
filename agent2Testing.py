import pygame
import time
from minesweeper import Minesweeper
from knowledgebase import A1_cell

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


def agent2(game):
    global knowledge_base

    #initializing knowledge base
    initialize_kb(game)

    pass

def initialize_kb(game):
    #initializing knowledge base
    for row in range(game._dim):
        knowledge_base.append([])
        for col in range(game._dim):
            if (row == 0 and col == 0) or (row == game._dim - 1 and col == game._dim - 1):
                knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 3))
            elif row == 0 or row == game._dim - 1 or col == 0 or col == game._dim - 1:
                knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 5))
            else:
                knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 8))

    for row in range(game._dim):
        for col in range(game._dim):
            dim = game._dim
            current = knowledge_base[row][col]

            # adding up and to the left cell to neighbor
            if row - 1 >= 0 and col - 1 >= 0:
                current.neighbors.append(knowledge_base[row - 1][col - 1])

            # adding up cell to neighbor
            if row - 1 >= 0 and col < dim:
                current.neighbors.append(knowledge_base[row - 1][col])

            # adding up and to the right cell to neighbor
            if row - 1 >= 0 and col + 1 < dim:
                current.neighbors.append(knowledge_base[row - 1][col + 1])

            # adding left cell to neighbor
            if row >= 0 and col - 1 >= 0:
                current.neighbors.append(knowledge_base[row][col - 1])

            # adding right cell to neighbor
            if row >= 0 and col + 1 < dim:
                current.neighbors.append(knowledge_base[row][col + 1])

            # adding under and to the left cell to neighbor
            if row + 1 < dim and col - 1 >= 0:
                current.neighbors.append(knowledge_base[row + 1][col - 1])

            # adding under cell to neighbor
            if row + 1 < dim and col >= 0:
                current.neighbors.append(knowledge_base[row + 1][col])

            # adding under and to the right cell to neighbor
            if row + 1 < dim and col + 1 < dim:
                current.neighbors.append(knowledge_base[row + 1][col + 1])

def game_update(game):
    game_updated = game.draw(screen_size)
    screen.fill(WHITE)
    pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, ORIGIN)
    pygame.display.update()

if __name__ == '__main__':

    size = 30
    game = Minesweeper(size, 70)
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