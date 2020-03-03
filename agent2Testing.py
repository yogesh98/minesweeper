import random
import pygame
from minesweeper import Minesweeper
from knowledgebase import A2 as KB

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

# TODO comment code
# TODO pick better way of picking a square besides random for the first one


def agent2(game):
    #initializing knowledge base
    knowledge_base = KB(game)
    game_over = False

    analyze_kb(game, knowledge_base)
    while not game_over:
        while len(knowledge_base.safe) > 0:
            cell = knowledge_base.safe.pop(0)
            clue = game.query(cell.row, cell.col)
            # game_full_update(game)
            game_update(game, cell.row, cell.col)
            knowledge_base.update(cell.row, cell.col, clue[1], clue[0])
            analyze_kb(game, knowledge_base)
        # checks if game is over if so prints score and ends game
        if game.game_over():
            score = game.calculate_score()
            game_over = True
            return score

def analyze_kb(game, kb):
    # Need to check if any clue becomes 0 if it does move all the squares to safe,
    # check if those squares are in any other set if they are remove them

    # next checking if any clue in unsafe has 0 mines in it, if so it moves that over to safe
    put_in_safe = []
    remove_after = []
    update_as_flagged = []
    for i in range(len(kb.unsafe)):
        if kb.unsafe[i][0] == 0:
            put_in_safe = kb.unsafe[i]
            remove_after.append(put_in_safe)
            for j in range(1, len(put_in_safe)):
                kb.safe.append(put_in_safe[j])
        else:
            if len(kb.unsafe[i][1:]) == kb.unsafe[i][0]:
                remove_after.append(kb.unsafe[i])
                for cell in kb.unsafe[i][1:]:
                    game.flag(cell.row, cell.col)
                    game_update(game, cell.row, cell.col)
                    update_as_flagged.append(cell)
    for i in remove_after:
        kb.unsafe.remove(i)
    for cell in update_as_flagged:
        kb.update(cell.row, cell.col, -1, True)


    # TODO Change this to be more smarter than just picking a random one

    if len(kb.safe) == 0:
        if len(kb.safe) != 0:
            min_prob = 100
            best_chance = None
            for i in range(len(kb.unsafe)):
                current = kb.unsafe[i]
                num_mines = current[0]
                possible_squares = len(current[1:])
                probability = (num_mines/possible_squares) * 100

                if min_prob > probability:
                    min_prob = probability
                    best_chance = current

            rand = random.randint(1, len(best_chance))
            kb.safe.append(best_chance[rand])

        else:
            while True:
                if game.game_over():
                    break
                # picks random row and col
                row = random.randint(0, game._dim - 1)
                col = random.randint(0, game._dim - 1)

                # checks to make sure random row and col is covered if so adds it to safe
                if kb.knowledge_base[row][col].covered and not kb.knowledge_base[row][col].mine:
                    kb.safe.append(kb.knowledge_base[row][col])
                    break


    # if len(kb.safe) == 0:
    #     while True:
    #         if game.game_over():
    #             break
    #         # picks random row and col
    #         row = random.randint(0, game._dim - 1)
    #         col = random.randint(0, game._dim - 1)
    #
    #         # checks to make sure random row and col is covered if so adds it to safe
    #         if kb.knowledge_base[row][col].covered and not kb.knowledge_base[row][col].mine:
    #             kb.safe.append(kb.knowledge_base[row][col])
    #             break



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

    # density = 0
    # total_score = 0
    # while density < .70:
    #     size = 60
    #     num_tests = 1
    #     for i in range(num_tests):
    #         game = Minesweeper(size, int(60**2 * density))
    #         game_full_update(game)
    #         score = agent2(game)
    #         total_score += score
    #     print(total_score/num_tests)
    #     total_score = 0
    #     density += 0.1

    for i in range(30):
        size = 30
        game = Minesweeper(size, 120)

        game_full_update(game)
        print(agent2(game))

    # for i in range(30):
    #     size = 5
    #     game = Minesweeper(size, 7)
    #
    #     game_full_update(game)
    #     agent2(game)
    #     # game_full_update(game)

    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

        size = 30
        game = Minesweeper(size, 120)

        game_full_update(game)
        agent2(game)

    pygame.quit()
    quit()