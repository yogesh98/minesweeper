class A1:

    def __init__(self, game):
        self.knowledge_base = []
        # initializing knowledge base
        for row in range(game._dim):
            self.knowledge_base.append([])
            for col in range(game._dim):
                if (row == 0 and col == 0) or (row == game._dim - 1 and col == game._dim - 1) or \
                        (row == 0 and col == game._dim - 1) or (row == 0 and col == game._dim - 1):
                    self.knowledge_base[row].append(A1_cell(row, col, True, None, -1, 0, 0, 3))
                elif row == 0 or row == game._dim - 1 or col == 0 or col == game._dim - 1:
                    self.knowledge_base[row].append(A1_cell(row, col, True, None, -1, 0, 0, 5))
                else:
                    self.knowledge_base[row].append(A1_cell(row, col, True, None, -1, 0, 0, 8))

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

    def update(self, row, col, clue, mine):
        current = self.knowledge_base[row][col]
        current.covered = False
        current.clue = clue
        current.mine = mine

        for cell in current.neighbors:
            cell.num_covered -= 1
            if not mine:
                cell.num_safe += 1
            else:
                cell.num_mines += 1

class A1_cell:

    def __init__(self, row, col, covered, mine, clue, num_safe, num_mines, num_covered):
        self.row = row
        self.col = col
        self.covered = covered
        self.mine = mine
        self.clue = clue
        self.num_safe = num_safe
        self.num_mines = num_mines
        self.num_covered = num_covered
        self.neighbors = []


class A2:

    def __init__(self, game):
        self.safe = []
        self.unsafe = []
        self.knowledge_base = []

        # initializing knowledge base
        for row in range(game._dim):
            self.knowledge_base.append([])
            for col in range(game._dim):
                    self.knowledge_base[row].append(A2Cell(row, col, True, None, -1))

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

    def simplify(self):
        # goes through each clue in unsafe to see if it is a subset of any other unsafe clue
        # if it is it will simplify both clues. For example if there are 2 mines in cells 1, 2 ,3
        # and another clue tells us there is 1 mine in cells 2,3 we can simplify this to
        # 1 mine in cell 1 (then go ahead and flag) and 1 mine in either cell 2 or 3
        for current in self.safe:
            for i in self.unsafe:
                if current in i:
                    i.remove(current)
                    if len(i) == 1:
                        self.unsafe.remove(i)

        # for i in range(len(self.unsafe)):
        #     for j in range(i + 1, len(self.unsafe)):
        #
        #         intersect = intersection(self.unsafe[i][1:], self.unsafe[j][1:])
        #         if self.unsafe[i][0] == self.unsafe[j][0] and len(intersect) == self.unsafe[i][0]:
        #             newclue = self.unsafe[i][0]
        #             intersect.insert(0, newclue)
        #             self.unsafe.remove(self.unsafe[i])
        #             self.unsafe.remove(self.unsafe[j])
        #             self.unsafe.append(intersect)


        remove_after = []
        for i in range(len(self.unsafe)):
            for j in range(i+1, len(self.unsafe)):

                # checking if it is a subset
                issubset = subset(self.unsafe[i], self.unsafe[j])

                # assigning first one as subset if it is
                if issubset == 1:
                    subscope = self.unsafe[i]
                    outerscope = self.unsafe[j]

                # assigning second one as subset if it is
                elif issubset == 2:
                    subscope = self.unsafe[j]
                    outerscope = self.unsafe[i]
                else:
                    continue
                # doing simplification of both of the clues
                outerscope[0] = outerscope[0] - subscope[0]
                for cell in subscope[1:]:
                    outerscope.remove(cell)
                if len(outerscope) == 1:
                    remove_after.append(outerscope)

        for i in remove_after:
            try:
                self.unsafe.remove(i)
            except ValueError:
                pass

    def update(self, row, col, clue, mine):
        current = self.knowledge_base[row][col]
        current.covered = False
        current.clue = clue
        current.mine = mine

        if not current.mine:
            for i in self.unsafe:
                if current in i:
                    i.remove(current)
            self.categorize(row, col, clue)
        else:
            for i in self.unsafe:
                if current in i:
                    i.remove(current)
                    i[0] = i[0] - 1
        self.simplify()

    def categorize(self, row, col, clue):
        current = self.knowledge_base[row][col]
        if clue == 0:
            for neighbor in current.neighbors:
                if neighbor.covered and neighbor not in self.safe:
                    self.safe.append(neighbor)
        else:
            lst = [clue]
            for neighbor in current.neighbors:
                if neighbor.mine:
                    lst[0] -= 1
                elif neighbor.covered and neighbor not in self.safe:
                    lst.append(neighbor)
            self.unsafe.append(lst)

class A2Cell:
    def __init__(self, row, col, covered, mine, clue):
        self.row = row
        self.col = col
        self.covered = covered
        self.mine = mine
        self.clue = clue
        self.neighbors = []

def intersection(list1, list2):
    list2_as_set = set(list2)
    intersect = [value for value in list1 if value in list2_as_set]
    if len(intersect) == 0:
        return None
    return intersect

def subset(first, second):
    one = set(first[1:])
    two = set(second[1:])

    if one.issubset(two):
        return 1
    if two.issubset(one):
        return 2
    return 0