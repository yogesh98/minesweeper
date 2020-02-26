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


def subset(first, second):
    one = set(first[1:])
    two = set(second[1:])

    if one.issubset(two):
        return 1
    if two.issubset(one):
        return 2
    return 0


# class A2:
#     safe = []
#     unsafe = []
#
#     def __init__(self):
#         pass
#
#     def simplify(self):
#         # goes through each clue in unsafe to see if it is a subset of any other unsafe clue
#         # if it is it will simplify both clues. For example if there are 2 mines in cells 1, 2 ,3
#         # and another clue tells us there is 1 mine in cells 2,3 we can simplify this to
#         # 1 mine in cell 1 (then go ahead and flag) and 1 mine in either cell 2 or 3
#         for i in range(len(self.unsafe)):
#             for j in range(i, len(self.unsafe)):
#                 # checking if it is a subset
#                 issubset = subset(self.unsafe[i], self.unsafe[j])
#
#                 # assigning first one as subset if it is
#                 if issubset == 1:
#                     subscope = self.unsafe[i]
#                     outerscope = self.unsafe[j]
#
#                 # assigning second one as subset if it is
#                 elif issubset == 2:
#                     subscope = self.unsafe[j]
#                     outerscope = self.unsafe[i]
#                 else:
#                     continue
#
#                 # doing simplification of both of the clues
#                 outerscope[0] = outerscope[0] - subscope[0]
#                 for cell in subscope[1:]:
#                     outerscope.remove(cell)
#
#         # next checking if any clue in unsafe has 0 mines in it, if so it moves that over to safe
#         for i in range(len(self.unsafe)):
#             if self.unsafe[i][0] == 0:
#                 put_in_safe = self.unsafe.pop(i)
#                 for j in range(1, len(put_in_safe)):
#                     self.safe.append(put_in_safe[j])
