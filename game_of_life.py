import numpy
import time

def pp_array(board):
    output = ''
    for row in board:
        for elem in row:
            if elem:
                output += ' o'
            else:
                output += ' .'
        output += '\n'
    print(output)


def inbounds(loc, shape):
    x = loc[0]
    y = loc[1]
    max_x = shape[1] - 1
    max_y = shape[0] - 1
    if x < 0 or x > max_x:
        return False
    if y < 0 or y > max_y:
        return False
    else:
        return True


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
            new_loc = [loc for loc in neighbor_loc if inbounds(loc, shape)]
            n_neighbors = sum(board[y,x] for y,x in new_loc)
            if elem:
                # there's life here!
                if n_neighbors >= 2 and n_neighbors <= 3:
                    new_board[r_ind][c_ind] = 1
            else:
                # no life
                if n_neighbors == 3:
                    # reproduction
                    new_board[r_ind][c_ind] = 1
    return new_board

def new_board():
    width = 50
    height = 50
    options = [0, 1]
    probability = [.8, .2]
    board = numpy.random.choice(
        options,
        size=(height, width),
        p=probability
    )
    return board

def line_oscillator():
    board = numpy.array([
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
    ])
    return board

def new_game():
    board = new_board()

    while True:
        pp_array(board)
        time.sleep(1)
        board = update_board(board)

if __name__ == '__main__':
    new_game()
