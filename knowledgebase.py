class A1:
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

