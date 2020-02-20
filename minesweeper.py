from minecell import Minecell
from random import randint
import pygame


class Minesweeper:
    env = []
    dim = 0
    num_mines = 0

    def __init__(self, dim, num_mines):
        # making sure mines will fit
        if num_mines > dim**2:
            raise ValueError("Number of Mines Too High!!")

        self.env = list()
        self.dim = dim
        self.num_mines = num_mines

        # creating minesweeper environment
        for row in range(dim):
            self.env.append(list())
            for col in range(dim):
                self.env[row].append(Minecell())

        # setting mines in random places
        for i in range(num_mines):
            mine_set = False
            while not mine_set:
                row = randint(0, dim-1)
                col = randint(0, dim-1)
                if not self.env[row][col].mine:
                    self.env[row][col].mine = True
                    mine_set = True

        # Setting clue for each cell
        for row in range(dim):
            for col in range(dim):
                mine_counter = 0

                # Setting clue if cell contain mine to -1
                if self.env[row][col].mine:
                    self.env[row][col].value = -1
                    continue

                # incrementing mine count for above and to the left cell
                if row - 1 >= 0 and col - 1 >= 0 and self.env[row - 1][col - 1].mine:
                    mine_counter += 1


                # incrementing mine count for above cell
                if row - 1 >= 0 and col < dim and self.env[row - 1][col].mine:
                    mine_counter += 1

                # incrementing mine count for above and to the right cell
                if row - 1 >= 0 and col + 1 < dim and self.env[row - 1][col + 1].mine:
                    mine_counter += 1

                # incrementing mine count for the left cell
                if row >= 0 and col - 1 >= 0 and self.env[row][col - 1].mine:
                    mine_counter += 1

                # incrementing mine count for the right cell
                if row >= 0 and col + 1 < dim and self.env[row][col + 1].mine:
                    mine_counter += 1


                # incrementing mine count for below and to the left cell
                if row + 1 < dim and col - 1 >= 0 and self.env[row + 1][col - 1].mine:
                    mine_counter += 1

                # incrementing mine count for below cell
                if row + 1 < dim and col >= 0 and self.env[row + 1][col].mine:
                    mine_counter += 1

                # incrementing mine count for below and to the right cell
                if row + 1 < dim and col + 1 < dim and self.env[row + 1][col + 1].mine:
                    mine_counter += 1

                # setting mine count to the value of the cell
                self.env[row][col].value = mine_counter

    # function to query a cell that agent will use
    def query(self, row, col):
        return self.env[row][col].query()

    # function to flag a cell that agent will use
    def flag(self, row, col):
        self.env[row][col].flag()

    def draw(self, screen_size):
        d = pygame.image.load("Assets/bd.png")
        f = pygame.image.load("Assets/bf.png")
        m = pygame.image.load("Assets/bm.png")
        p = dict()
        p[0] = pygame.image.load("Assets/bp0.png")
        p[1] = pygame.image.load("Assets/bp1.png")
        p[2] = pygame.image.load("Assets/bp2.png")
        p[3] = pygame.image.load("Assets/bp3.png")
        p[4] = pygame.image.load("Assets/bp4.png")
        p[5] = pygame.image.load("Assets/bp5.png")
        p[6] = pygame.image.load("Assets/bp6.png")
        p[7] = pygame.image.load("Assets/bp7.png")
        p[8] = pygame.image.load("Assets/bp8.png")

        img_size = int(screen_size / self.dim)
        surface_dim = img_size * self.dim
        surface = pygame.Surface((surface_dim, surface_dim))

        for row in range(len(self.env)):
            for col in range(len(self.env)):
                cell = self.env[row][col]
                if not cell.queried and not cell.flagged:
                    surface.blit(pygame.transform.smoothscale(d, (img_size, img_size)), (row * img_size, col * img_size))
                elif cell.mine and cell.queried:
                    surface.blit(pygame.transform.smoothscale(m, (img_size, img_size)), (row * img_size, col * img_size))
                elif cell.flagged:
                    surface.blit(pygame.transform.smoothscale(f, (img_size, img_size)), (row * img_size, col * img_size))
                else:
                    surface.blit(pygame.transform.smoothscale(p[cell.value], (img_size, img_size)), (row * img_size, col * img_size))
        return surface

    # def draw(self):
    #     if self.dim < 16:
    #         size_factor = 64
    #         d = pygame.image.load("Assets/bd.png")
    #         f = pygame.image.load("Assets/bf.png")
    #         m = pygame.image.load("Assets/bm.png")
    #         p = dict()
    #         p[1] = pygame.image.load("Assets/bp1.png")
    #         p[2] = pygame.image.load("Assets/bp2.png")
    #         p[3] = pygame.image.load("Assets/bp3.png")
    #         p[4] = pygame.image.load("Assets/bp4.png")
    #         p[5] = pygame.image.load("Assets/bp5.png")
    #         p[6] = pygame.image.load("Assets/bp6.png")
    #         p[7] = pygame.image.load("Assets/bp7.png")
    #         p[8] = pygame.image.load("Assets/bp8.png")
    #     else:
    #         size_factor = 32
    #         d = pygame.image.load("Assets/sd.png")
    #         f = pygame.image.load("Assets/sf.png")
    #         m = pygame.image.load("Assets/sm.png")
    #         p = dict()
    #         p[1] = pygame.image.load("Assets/sp1.png")
    #         p[2] = pygame.image.load("Assets/sp2.png")
    #         p[3] = pygame.image.load("Assets/sp3.png")
    #         p[4] = pygame.image.load("Assets/sp4.png")
    #         p[5] = pygame.image.load("Assets/sp5.png")
    #         p[6] = pygame.image.load("Assets/sp6.png")
    #         p[7] = pygame.image.load("Assets/sp7.png")
    #         p[8] = pygame.image.load("Assets/sp8.png")
    #
    #     surface = pygame.Surface((self.dim * size_factor, self.dim * size_factor))
    #     for row in range(len(self.env)):
    #         for col in range(len(self.env)):
    #             cell = self.env[row][col]
    #             if not cell.queried:
    #                 surface.blit(d, (row * size_factor, col * size_factor))
    #             elif cell.mine:
    #                 surface.blit(m, (row * size_factor, col * size_factor))
    #             elif cell.flag:
    #                 surface.blit(f, (row * size_factor, col * size_factor))
    #             else:
    #                 surface.blit(p[cell.value], (row * size_factor, col * size_factor))
    #     return surface





