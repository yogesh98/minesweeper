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


def agent2(game):
    #initializing knowledge base
    knowledge_base = KB(game)

    # variable to stop querying if the game is over (All mines have been queried or flagged
    game_over = False

    # Picks first move
    analyze_kb(game, knowledge_base)

    # game loop, queries till game is over
    while not game_over:

        # Checks if there is any cells that are safe and can be queried
        while len(knowledge_base.safe) > 0:

            # Takes off the first cell to query
            cell = knowledge_base.safe.pop(0)

            # querying that cell returns if it was a mine and clue
            clue = game.query(cell.row, cell.col)

            # Updating pygame window (Graphics)
            game_update(game, cell.row, cell.col)

            # Updating Knowledgebase (consists of updating information about querried cells and making deductions)
            knowledge_base.update(cell.row, cell.col, clue[1], clue[0])

            # Using Deductions to add safe cells to safe
            analyze_kb(game, knowledge_base)

        # checks if game is over if so prints score and ends game
        if game.game_over():
            score = game.calculate_score()
            game_over = True
            return score

# This function analyzes the current state of the knowledge base. It looks to see if any cells can be moved to safe
# and if a cell is 100% a mine it will flag it and update the knowledge base
def analyze_kb(game, kb):

    # Variable to tell if an action has been made.
    action = True

    # knowledgebase analysis will happen again with the new deductions from each action
    while action:
        action = False
        # List of Lists in unsafe to be removed
        remove_after = []

        # List of cells that have been flagged and need to be removed
        update_as_flagged = []

        # Using deductions made in knowledgebase to make choice on which cells can be querried
        for i in range(len(kb.unsafe)):
            # Checking each list in Unsafe and seeing if there is 0 mines within those cells
            if kb.unsafe[i][0] == 0:
                action = True
                # if there are no mines within those cells it will add them to safe and add them
                # to a remove_after list to remove them. Can not remove on the spot because it will mess up the for loop
                remove_after.append(kb.unsafe[i])
                for j in range(1, len(kb.unsafe[i])):
                    kb.safe.append(kb.unsafe[i][j])

            # If there is still mines within those cells it will check if the number of cells is equal to the number of
            # mines. If so it will flag all those cells
            elif len(kb.unsafe[i][1:]) == kb.unsafe[i][0]:
                action = True
                # adds to remove after list
                remove_after.append(kb.unsafe[i])

                # for each cell in the list it will flag those cells
                for cell in kb.unsafe[i][1:]:
                    # Flag cell
                    game.flag(cell.row, cell.col)
                    # Update pygame window (Graphics)
                    game_update(game, cell.row, cell.col)
                    # Add cell to a list so that the KB can be updated
                    update_as_flagged.append(cell)
        # Removing all lists in unsafe that need to be removed
        for i in remove_after:
            kb.unsafe.remove(i)

        # Updates KB with cells that have been flagged and makes new deductions based on these
        for cell in update_as_flagged:
            kb.update(cell.row, cell.col, -1, True)


    # If after knowledgebase analysis there are no safe cells it will find the cell with the least probability
    if len(kb.safe) == 0:

        # if unsafe list is not 0 it can find cell with least probability otherwise has to pick random
        if len(kb.unsafe) != 0:
            # variable to hold the min probability
            min_prob = 100
            # varaible to hold list from unsafe that gives best chance to pick a cell without a mine
            best_chance = None
            # checks probability of selecting a mine from all lists in unsafe
            for i in range(len(kb.unsafe)):

                # calculating probability from the list
                current = kb.unsafe[i]
                num_mines = current[0]
                possible_squares = len(current[1:])
                probability = (num_mines/possible_squares) * 100

                # if this probability is less the one stored in min swaps min and best chance for this one
                if min_prob > probability:
                    min_prob = probability
                    best_chance = current

            # Picks random cell from the best chance and adds it to safe so that the agent will query it
            rand = random.randint(1, len(best_chance) - 1)
            kb.safe.append(best_chance[rand])

        # picks random cell if the above did not happen
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