class Minecell:

    mine = False
    value = -1
    flagged = False
    queried = False

    def __init__(self):
        pass

    def __str__(self):
        return self.value

    def query(self):
        self.queried = True
        return self.mine, self.value

    def flag(self):
        if not self.queried:
            self.flagged = True

    def unflag(self):
        self.flagged = False
