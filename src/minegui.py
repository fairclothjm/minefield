import pygame, sys
from minesweeper import Minesweeper, CellState
from pygame.locals import *


window_width = 322
window_height = 322
margin = 2
cell_width = 30
cell_height = 30
cell_dimensions = [cell_width, cell_height]

black = (0, 0, 0)
gray = (100, 100, 100)
light_gray = (200, 200, 200)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
minesweeper = Minesweeper() 
minesweeper.setup() 

pygame.init()
display_surface = pygame.display.set_mode([window_width, window_height])
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()

def get_cell(value):
    box = pygame.Surface((cell_width, cell_height))
    if value == -2:
        return pygame.image.load('img/redmine.png')
    if value == -1:
        return pygame.image.load('img/mine.png')
    if value == 0:
        return pygame.image.load('img/exposed.png')
    if value > 0:
        return pygame.image.load('img/' + str(value) + '.png')

def reveal_cluster():
    for row in range(10):
        for col in range(10):
            if minesweeper.field[row][col] == CellState.exposed:
                adjacency = minesweeper.adjacent_mine_count(row, col)
                display_surface.blit(get_cell(adjacency), (row*32 + margin, col*32 + margin))

def reveal_mines(x, y, game_state):
    for row in range(10):
        for col in range(10):
            if minesweeper.mines[row][col]: 
                display_surface.blit(get_cell(-1), (row*32 + margin, col*32 + margin))

    if game_state == 'loss':
        display_surface.blit(get_cell(-2), (x*32 + margin, y*32 + margin))

def draw_board():
    display_surface.fill(black)
    for row in range(10):
        for col in range(10):
            pygame.draw.rect(
                    display_surface, 
                    gray, 
                    ((cell_width + margin) * col + margin,
                        (cell_height + margin) * row + margin, 
                        cell_width, 
                        cell_height))

def main():
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if minesweeper.game_state != 'playing':
                    draw_board()
                    minesweeper.__init__()
                    minesweeper.setup()
                    pygame.display.set_caption('Minesweeper')
                else:
                    pos = pygame.mouse.get_pos()
                    x_pos = int(pos[0]/32)
                    y_pos = int(pos[1]/32)
                    minesweeper.expose_cell(x_pos, y_pos)
                    if minesweeper.game_state == 'loss':
                        reveal_mines(x_pos, y_pos, 'loss')
                        pygame.display.set_caption('You Lose!')
                    else:
                        if minesweeper.field[x_pos][y_pos] == CellState.exposed:
                            adjacency = minesweeper.adjacent_mine_count(x_pos, y_pos)
                            if adjacency > 0:
                                display_surface.blit(get_cell(adjacency), (x_pos*32 + margin, y_pos*32 + margin))
                            if adjacency == 0:
                                reveal_cluster()
                        if minesweeper.game_state == 'win':
                            pygame.display.set_caption('You Win!')
                            reveal_mines(0, 0, 'win')

            elif event.type == MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                x_pos = int(pos[0]/32)
                y_pos = int(pos[1]/32)
                minesweeper.toggle_seal(x_pos, y_pos)
                if minesweeper.field[x_pos][y_pos] == CellState.sealed:
                    display_surface.blit(get_cell('sealed'), (x_pos*32 + margin, y_pos*32 + margin))
                else:
                    display_surface.blit(get_cell('unexposed'), (x_pos*32 + margin, y_pos*32 + margin))

        clock.tick(60)
        pygame.display.update()

if __name__ == '__main__':
    main()
