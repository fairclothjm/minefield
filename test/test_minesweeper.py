import unittest
from src.minesweeper import Minesweeper 
from src.minesweeper import CellState
from types import MethodType


class TestMinesweeper(unittest.TestCase):

    def setUp(self):
        self.minesweeper = Minesweeper()
        self.expose_neighbors_of_called = False
        self.cells = []

    def new_expose_neighbors_of(self, null, row, col):
        self.expose_neighbors_of_called = True

    def new_expose_cell(self, null, row, col):
        self.cells.append((row, col))

    def test_canary(self):
        self.assertTrue(True)
    
    def test_expose_cell(self):
        self.minesweeper.expose_cell(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.exposed)

    def test_expose_already_exposed_cell(self):
        self.minesweeper.expose_cell(1, 2)
        self.minesweeper.expose_cell(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.exposed)

    def test_expose_two_unexposed_cells(self):
        self.minesweeper.expose_cell(1, 2)
        self.minesweeper.expose_cell(4, 5)

        self.assertEqual(self.minesweeper.field[1][2], CellState.exposed)
        self.assertEqual(self.minesweeper.field[4][5], CellState.exposed)
    
    def test_expose_neighbors_of_called(self):
        self.minesweeper.expose_neighbors_of = MethodType(
                self.new_expose_neighbors_of,
                self.minesweeper)

        self.minesweeper.expose_cell(3, 4)

        self.assertEqual(self.minesweeper.field[3][4], CellState.exposed)
        self.assertTrue(self.expose_neighbors_of_called)

    def test_expose_neighbors_of_called_once(self):
        self.minesweeper.expose_neighbors_of = MethodType(
                self.new_expose_neighbors_of,
                self.minesweeper)

        self.minesweeper.expose_cell(3, 4)
        self.assertTrue(self.expose_neighbors_of_called)
        self.expose_neighbors_of_called = False

        self.minesweeper.expose_cell(3, 4)
        self.assertEqual(self.minesweeper.field[3][4], CellState.exposed)
        self.assertFalse(self.expose_neighbors_of_called)

    def test_expose_neighbors_of_not_called_when_adjacent_cell_exposed(self):
        self.minesweeper.expose_neighbors_of_called = False
        self.minesweeper.expose_neighbors_of = MethodType(
                self.new_expose_neighbors_of,
                self.minesweeper)

        def new_adjacent_mine_count(self, row, col):
            return True
        self.minesweeper.adjacent_mine_count = MethodType(
                new_adjacent_mine_count,
                self.minesweeper)

        self.minesweeper.expose_cell(3, 4)
        self.assertEqual(self.minesweeper.field[3][4], CellState.exposed)
        self.assertFalse(self.expose_neighbors_of_called)

    def test_expose_neighbors_of_calls_expose_cell(self):
        test_cells = [(2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (3, 5), (2, 5), (2, 4)]

        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(3, 4)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_on_top_edge(self):
        test_cells = [(8, 4), (9, 4), (9, 6), (8, 6), (8, 5)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(9, 5)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_on_bottom_edge(self):
        test_cells = [(0, 4), (1, 4), (1, 5), (1, 6), (0, 6)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(0, 5)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_right_edge(self):
        test_cells = [(4, 8), (5, 8), (6, 8), (6, 9), (4, 9)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(5, 9)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_on_left_edge(self):
        test_cells = [(6, 0), (6, 1), (5, 1), (4, 1), (4, 0)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(5, 0)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_on_bottom_left_corner(self):
        test_cells = [(1, 0), (1, 1), (0, 1)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(0, 0)

        self.assertEqual(self.cells, test_cells)

    def test_expose_neighbors_on_top_right_corner(self):
        test_cells = [(8, 8), (9, 8), (8, 9)]
        self.minesweeper.expose_cell = MethodType(
            self.new_expose_cell,
            self.minesweeper)

        self.minesweeper.expose_neighbors_of(9, 9)

        self.assertEqual(self.cells, test_cells)

    def test_toggle_seal_seals_an_unexposed_cell(self):
        self.minesweeper.toggle_seal(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.sealed)

    def test_toggle_seal_unseals_a_sealed_cell(self):
        self.minesweeper.field[1][2] = CellState.sealed

        self.minesweeper.toggle_seal(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.unexposed)

    def test_toggle_seal_does_nothing_to_exposed_cells(self):
        self.minesweeper.field[1][2] = CellState.exposed

        self.minesweeper.toggle_seal(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.exposed)

    def test_expose_cell_does_not_expose_sealed_cells(self):
        self.minesweeper.field[1][2] = CellState.sealed

        self.minesweeper.expose_cell(1, 2)

        self.assertEqual(self.minesweeper.field[1][2], CellState.sealed)

    def test_adjacent_mine_count_returns_0_for_no_adjacent_mines(self):
        self.assertEqual(self.minesweeper.adjacent_mine_count(1, 2), 0)

    def test_adjacent_mine_count_returns_1_for_1_adjacent_mines(self):
        self.minesweeper.mines[1][3] = True

        self.assertEqual(self.minesweeper.adjacent_mine_count(1, 2), 1)

    def test_adjacent_mine_count_returns_2_for_2_adjacent_mines(self):
        self.minesweeper.mines[1][3] = True
        self.minesweeper.mines[2][2] = True

        self.assertEqual(self.minesweeper.adjacent_mine_count(1, 2), 2)

    def test_adjacent_mine_count_returns_8_for_max_adjacent_mines(self):
        self.minesweeper.mines = [[True for row in range(10)] for col in range(10)]
        self.minesweeper.mines[1][2] = False

        self.assertEqual(self.minesweeper.adjacent_mine_count(1, 2), 8)

    def test_starting_the_game_sets_game_state_to_playing(self):
        self.minesweeper.setup()

        self.assertEqual(self.minesweeper.game_state, 'playing')

    def test_game_state_doesnt_become_win_until_all_non_mine_cells_are_exposed(self):
        self.minesweeper.mines[0][1] = True
        self.minesweeper.mine_count = 1

        self.minesweeper.expose_cell(2, 2)
        self.minesweeper.toggle_seal(0, 1)

        self.assertEqual(self.minesweeper.game_state, 'playing')

    def test_exposing_all_non_mine_cells_wins_the_game(self):

        self.minesweeper.mines[0][1] = True
        self.minesweeper.mine_count = 1

        self.minesweeper.expose_cell(2, 2)
        self.minesweeper.expose_cell(0, 0)

        self.assertEqual(self.minesweeper.game_state, 'win')

    def test_exposing_a_mine_triggers_a_game_loss(self):
        self.minesweeper.game_state == 'playing'
        self.minesweeper.mines[1][2] = True

        self.minesweeper.expose_cell(1, 2)

        self.assertEqual(self.minesweeper.game_state, 'loss')

    def test_generate_mine_generates_a_mine(self):
        self.minesweeper.generate_mine()
        mines_found = 0

        for row in range (10):
            for col in range (10):
                if self.minesweeper.mines[row][col]:
                    mines_found += 1

        self.assertEqual(mines_found, 1)

    def test_setup_generates_mines_differently_each_time(self):
        board1 = Minesweeper()
        board2 = Minesweeper()

        board1.setup()
        board2.setup()

        self.assertFalse(board1.mines == board2.mines)

if __name__ == '__main__':
    unittest.main()
