import numpy
import time
import pygame
import sys


class Cell(object):
    """base class for a cell"""

    __slots__ = ('value')

    def __init__(self, value):
        super(Cell, self).__init__()
        self.value = value


def pp_array(board):
    output = ''
    for row in board:
        for elem in row:
            if elem == 1:
                output += ' o'
            elif elem == 2:
                output += ' x'
            else:
                output += ' .'
        output += '\n'
    print(output)


def loop_around(loc, shape):
    # Note that this is a torus!
    # https://kotaku.com/classic-jrpg-worlds-are-actually-donuts-1239882216
    x = loc[0]
    y = loc[1]
    max_x = shape[1] - 1
    max_y = shape[0] - 1
    if x < 0:
        x = max_y
    elif x > max_y:
        x = 0
    if y < 0:
        y = max_x
    elif y > max_x:
        y = 0
    return (x, y)


def conway_rules(curr, neighbors):
    n_neighbors = sum(neighbors)
    if curr:
        # there's life here!
        if n_neighbors in [2, 3]:
            return 1
    else:
        # no life
        if n_neighbors in [3]:
            # reproduction
            return 1
    return 0


def b1_s12_rules(curr, neighbors):
    n_neighbors = sum(neighbors)
    if curr:
        # there's life here!
        if n_neighbors in [1, 2]:
            return 1
    else:
        # no life
        if n_neighbors in [1]:
            # reproduction
            return 1
    return 0


def immigration_rules(curr, neighbors):
    n_ones = sum([1 for n in neighbors if n == 1])
    n_twos = sum([1 for n in neighbors if n == 2])
    if n_twos > n_ones:
        curr_val = 2
    elif n_ones > n_twos:
        curr_val = 1
    n_neighbors = n_ones + n_twos
    if curr:
        # there's life here!
        if n_neighbors in [2, 3]:
            return curr
    else:
        # no life
        if n_neighbors in [3]:
            # reproduction
            return curr_val
    return 0


def update_board(board):
    shape = board.shape
    new_board = numpy.zeros(shape)
    for r_ind, row in enumerate(board):
        for c_ind, elem in enumerate(row):
            neighbor_loc = [
                (r_ind - 1, c_ind - 1),
                (r_ind - 1, c_ind),
                (r_ind - 1, c_ind + 1),
                (r_ind, c_ind - 1),
                (r_ind, c_ind + 1),
                (r_ind + 1, c_ind - 1),
                (r_ind + 1, c_ind),
                (r_ind + 1, c_ind + 1),
            ]
            neighbors = [board[loop_around(loc, shape)]
                         for loc in neighbor_loc]
            new_board[r_ind, c_ind] = immigration_rules(elem, neighbors)
    return new_board


def random_board():
    width = 100
    height = 100
    options = [0, 1]
    probability = [.8, .2]
    board = numpy.random.choice(
        options,
        size=(height, width),
        p=probability
    )
    return board


def random_immigration_board():
    width = 50
    height = 50
    options = [0, 1, 2]
    probability = [.8, .1, .1]
    board = numpy.random.choice(
        options,
        size=(height, width),
        p=probability
    )
    return board


def line_oscillator():
    board = numpy.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ])
    return board


def basic_glider():
    board = numpy.array([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ])
    return board


def single_cell():
    board = numpy.zeros((50, 50))
    board[25][25] = 1
    return board


def new_game():
    board = random_board()

    pygame.init()
    scale_factor = 5
    screen = pygame.display.set_mode((board.shape[0]*scale_factor,board.shape[1]*scale_factor))
    pygame.display.set_caption("Tea's Game of Life")

    clock = pygame.time.Clock()
    while True:
        clock.tick(50)
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Thank you for playing!')
                sys.exit()

        screen.fill((0, 0, 0))
        board = update_board(board)
        surface = pygame.surfarray.make_surface(board)
        surface = pygame.transform.scale(surface, (100*scale_factor, 100*scale_factor))  # Scaled a bit.
        screen.blit(surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    new_game()
