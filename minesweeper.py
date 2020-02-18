from minecell import Minecell
from random import randint
import pygame

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 00)
GREEN = (0, 250, 0)
BLUE = (0, 0, 255)


class Minesweeper:
    env = []
    dim = 0
    num_mines = 0

    def __init__(self, dim, num_mines):
        # Graphics Stuff

        # making sure mines will fit
        if num_mines > dim**2:
            raise ValueError("Number of Mines Too High!!")

        self.env = []
        self.dim = dim
        self.num_mines = num_mines

        # creating minesweeper environment
        for row in dim:
            self.env[row].append([])
            for col in dim:
                self.env[row].append(Minecell())

        # setting mines in random places
        for i in num_mines:
            mineset = False
            while not mineset:
                row = randint(0, dim-1)
                col = randint(0, dim-1)
                if not self.env[row][col].mine:
                    self.env[row][col] = True
                    mineset = True

        # Setting clue for each cell
        for row in dim:
            for col in dim:
                mine_counter = 0

                # Setting clue if cell contain mine to -1
                if self.env[row][col].mine:
                    self.env[row][col].value = -1
                    continue

                # incrementing mine count for above and to the left cell
                try:
                    if self.env[row - 1][col - 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for above cell
                try:
                    if self.env[row - 1][col].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for above and to the right cell
                try:
                    if self.env[row - 1][col + 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for the left cell
                try:
                    if self.env[row][col - 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for the right cell
                try:
                    if self.env[row][col + 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for below and to the left cell
                try:
                    if self.env[row + 1][col - 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for below cell
                try:
                    if self.env[row + 1][col].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # incrementing mine count for below and to the right cell
                try:
                    if self.env[row + 1][col + 1].mine:
                        mine_counter += 1
                except IndexError:
                    pass

                # setting mine count to the value of the cell
                self.env[row][col].value = mine_counter

    # function to query a cell that agent will use
    def query(self, row, col):
        return self.env[row][col].query()

    # function to flag a cell that agent will use
    def flag(self, row, col):
        self.env[row][col].flag = True

