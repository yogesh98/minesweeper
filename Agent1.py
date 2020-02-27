import pygame
import random
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
    game_over = False
    id_mine = []
    id_safe = []
    while not game_over:
        if len(id_safe) > 0:
            current = id_safe[0]
            id_safe.remove(current)

            query = game.query(current.row, current.col)
            kb.update(current.row, current.col, query[1], query[0])
            game_update(game, current.row, current.col)
            # game_full_update(game)

            if current.clue - current.num_mines == current.num_covered:
                for neighbor in current.neighbors:
                    if neighbor.covered:
                        id_mine.append(neighbor)
            elif len(current.neighbors) - current.clue - current.num_safe == current.num_covered:
                for neighbor in current.neighbors:
                    if neighbor.covered and neighbor not in id_safe:
                        id_safe.append(neighbor)

            for cell in id_mine:
                game.flag(cell.row, cell.col)
                kb.update(cell.row, cell.col, -1, True)
                game_update(game, cell.row, cell.col)
                id_mine.remove(cell)
        else:

            while True:
                row = random.randint(0, game._dim - 1)
                col = random.randint(0, game._dim - 1)

                if kb.knowledge_base[row][col].covered:
                    id_safe.append(kb.knowledge_base[row][col])
                    break
        if game.game_over():
            print(game.calculate_score())
            game_over = True

    pass

def game_full_update(game):
    game_updated = game.draw(screen_size)
    pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, ORIGIN)
    pygame.display.update()

def game_update(game, row, col):
    ret_draw = game.draw_single(screen_size, row, col)
    game_updated = ret_draw[0]
    img_size = ret_draw[1]
    # screen.fill(WHITE)
    # pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, (row * img_size, col * img_size))
    pygame.display.update((row * img_size, col * img_size, img_size, img_size))

if __name__ == '__main__':

    size = 30
    game = Minesweeper(size, 70)

    game_full_update(game)
    agent1(game)
    # game_full_update(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()
    quit()