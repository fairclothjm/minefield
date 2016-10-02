from enum import Enum
import random

class CellState(Enum):
    unexposed = 0
    exposed = 1
    sealed = 2

class Minesweeper:

    def __init__(self):
        self.field = [[CellState.unexposed for row in range(10)]for col in range(10)]
        self.mines = [[False for row in range(10)] for col in range(10)]
        self.mine_count = 0
        self.checked_count = 0
        self.game_state = 'playing'

    def setup(self):
        for x in range(10):
            self.generate_mine()

    def expose_cell(self, row, col):
        if self.field[row][col] == CellState.unexposed:
            if self.mines[row][col]:
                self.end_game('loss')
            else:
                self.field[row][col] = CellState.exposed
                self.checked_count += 1
                if self.checked_count == (100 - self.mine_count):
                    self.end_game('win')
                if not self.adjacent_mine_count(row, col):
                    self.expose_neighbors_of(row, col)


#Venkat: Use loops instead of series of if else
    def expose_neighbors_of(self, row, col):
        if row > 0 and col > 0:
            self.expose_cell(row - 1, col - 1)
        if col > 0:
            self.expose_cell(row, col - 1)
        if row < 9 and col > 0:
            self.expose_cell(row + 1, col - 1)
        if row < 9:
            self.expose_cell(row + 1, col)
        if row < 9 and col < 9:
            self.expose_cell(row + 1, col + 1)
        if col < 9:
            self.expose_cell(row, col + 1)
        if row > 0 and col < 9:
            self.expose_cell(row - 1, col + 1)
        if row > 0:
            self.expose_cell(row - 1, col)

#Venkat: use loops
    def adjacent_mine_count(self, row, col):
        mine_count = 0
        if row > 0 and col > 0:
            if self.mines[row - 1][col - 1]:
                mine_count += 1
        if col > 0:
            if self.mines[row][col - 1]:
                mine_count += 1
        if row < 9 and col > 0:
            if self.mines[row + 1][col - 1]:
                mine_count += 1
        if row < 9:
            if self.mines[row + 1][col]:
                mine_count += 1
        if row < 9 and col < 9:
            if self.mines[row + 1][col + 1]:
                mine_count += 1
        if col < 9:
            if self.mines[row][col + 1]:
                mine_count += 1
        if row > 0 and col < 9:
            if self.mines[row - 1][col + 1]:
                mine_count += 1
        if row > 0:
            if self.mines[row - 1][col]:
                mine_count += 1

        return mine_count

    def toggle_seal(self, row, col):
        if self.field[row][col] == CellState.unexposed:
            self.field[row][col] = CellState.sealed
        else:
            if self.field[row][col] == CellState.sealed:
                self.field[row][col] = CellState.unexposed

    def end_game(self, game_state):
        self.game_state = game_state

    def generate_mine(self):
        mine_generated = False
        while not mine_generated:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if not self.mines[row][col]:
                self.mines[row][col] = True
                self.mine_count += 1
                mine_generated = True

