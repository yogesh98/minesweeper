class A1:
    knowledge_base = []

    def __init__(self, game):
        # initializing knowledge base
        for row in range(game._dim):
            self.knowledge_base.append([])
            for col in range(game._dim):
                if (row == 0 and col == 0) or (row == game._dim - 1 and col == game._dim - 1):
                    self.knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 3))
                elif row == 0 or row == game._dim - 1 or col == 0 or col == game._dim - 1:
                    self.knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 5))
                else:
                    self.knowledge_base[row].append(A1_cell(True, None, -1, -1, -1, 8))

        for row in range(game._dim):
            for col in range(game._dim):
                dim = game._dim
                current = self.knowledge_base[row][col]

                # adding up and to the left cell to neighbor
                if row - 1 >= 0 and col - 1 >= 0:
                    current.neighbors.append(self.knowledge_base[row - 1][col - 1])

                # adding up cell to neighbor
                if row - 1 >= 0 and col < dim:
                    current.neighbors.append(self.knowledge_base[row - 1][col])

                # adding up and to the right cell to neighbor
                if row - 1 >= 0 and col + 1 < dim:
                    current.neighbors.append(self.knowledge_base[row - 1][col + 1])

                # adding left cell to neighbor
                if row >= 0 and col - 1 >= 0:
                    current.neighbors.append(self.knowledge_base[row][col - 1])

                # adding right cell to neighbor
                if row >= 0 and col + 1 < dim:
                    current.neighbors.append(self.knowledge_base[row][col + 1])

                # adding under and to the left cell to neighbor
                if row + 1 < dim and col - 1 >= 0:
                    current.neighbors.append(self.knowledge_base[row + 1][col - 1])

                # adding under cell to neighbor
                if row + 1 < dim and col >= 0:
                    current.neighbors.append(self.knowledge_base[row + 1][col])

                # adding under and to the right cell to neighbor
                if row + 1 < dim and col + 1 < dim:
                    current.neighbors.append(self.knowledge_base[row + 1][col + 1])

class A1_cell:
    covered = True
    mine = False
    clue = -1
    num_safe = 0
    num_mines = 0
    num_covered = 0
    neighbors = []

    def __init__(self, covered, mine, clue, num_safe, num_mines, num_covered):
        self.covered = covered
        self.mine = mine
        self.clue = clue
        self.num_safe = num_safe
        self.num_mines = num_mines
        self.num_covered = num_covered

class A2:
    safe = []
    unsafe = []

    def __init__(self):
        pass