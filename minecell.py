class Minecell:

    mine = False
    value = -1
    flag = False

    def __init__(self):
        None

    def __str__(self):
        return self.value

    def query(self):
        return self.mine, self.value