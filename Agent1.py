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


def agent1(game):

    # initializing knowledge base
    kb = KB(game)

    # variable to stop querying if the game is over (All mines have been queried or flagged
    game_over = False

    # list to hold the cells that have been identified as a mine
    id_mine = []

    #list to hold the cells that have been identified as safe
    id_safe = []

    # game loop, queries till game is over
    while not game_over:

        # checks if any identified safe or identified mine if so goes in otherwise adds random
        # cell to safe so it will query it
        if len(id_safe) > 0 or len(id_mine) > 0:

            # Querying all safe cells and adding clues to knowledge base
            while len(id_safe) > 0:
                # taking cell out of list and storing it to be queried
                current = id_safe.pop(0)

                # querying that cell returns if it was a mine and clue
                query = game.query(current.row, current.col)

                # updating knowledgebase
                kb.update(current.row, current.col, query[1], query[0])

                # Updating pygame window (Graphics)
                game_update(game, current.row, current.col)

            # flagging all mine cells and adding information to knowledge base
            while len(id_mine) > 0:
                # taking cell out of list and storing it to be flagged
                cell = id_mine.pop(0)

                # flagging cell
                game.flag(cell.row, cell.col)

                # updating knowledgebase
                kb.update(cell.row, cell.col, -1, True)

                # Updating pygame window (Graphics)
                game_update(game, cell.row, cell.col)

            # using newly gained clues to update add new cells to identified safe or identified mine,
            # if none are found in the next iteration one random
            # cell will be added to safe so that queries may continue
            # Goes through every clue in the knowledge base
            for row in kb.knowledge_base:
                for current in row:
                    # for each clue checks if
                    # the total number of mines (the clue) minus the number of
                    # revealed mines is the number of hidden neighbors, every hidden neighbor is a mine.
                    if current.clue - current.num_mines == current.num_covered:
                        for neighbor in current.neighbors:
                            if neighbor.covered:
                                id_mine.append(neighbor)

                    # for each clue checks if
                    # the total number of safe neighbors (8 - clue) minus the number of revealed
                    # safe neighbors is the number of hidden neighbors, every hidden neighbor is safe.
                    elif len(current.neighbors) - current.clue - current.num_safe == current.num_covered:
                        for neighbor in current.neighbors:
                            if neighbor.covered and neighbor not in id_safe:
                                id_safe.append(neighbor)

            # checks if game is over if so prints score and ends game
            if game.game_over():
                game_full_update(game)
                score = game.calculate_score()
                return score
                game_over = True

        # if there were no definitive safe cells or mine cells it picks a random one
        else:
            while True:
                # picks random row and col
                row = random.randint(0, game._dim - 1)
                col = random.randint(0, game._dim - 1)

                # checks to make sure random row and col is covered if so adds it to safe
                if kb.knowledge_base[row][col].covered:
                    id_safe.append(kb.knowledge_base[row][col])
                    break


# for graphics: will update full screen
def game_full_update(game):
    game_updated = game.draw(screen_size)
    pygame.display.set_mode((game_updated.get_size()[0], game_updated.get_size()[1]))
    screen.blit(game_updated, ORIGIN)
    pygame.display.update()

# for graphics: will update part of screen specified by the row and col
def game_update(game, row, col):
    ret_draw = game.draw_single(screen_size, row, col)
    game_updated = ret_draw[0]
    img_size = ret_draw[1]
    screen.blit(game_updated, (col * img_size, row * img_size))
    pygame.display.update((col * img_size, row * img_size, img_size, img_size))
    pygame.event.get()

if __name__ == '__main__':

    density = 0
    total_score = 0
    while density < .70:
        size = 60
        num_tests = 100
        for i in range(num_tests):
            game = Minesweeper(size, int(60**2 * density))
            score = agent1(game)
            game_full_update(game)
            total_score += score
        print(total_score/num_tests)
        total_score = 0
        density += 0.1



        # game_full_update(game)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()
    quit()