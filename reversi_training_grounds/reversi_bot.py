import tempfile
# import numpy as np
import random as rand
import reversi
import math
import copy

DNA = []

class ReversiBot:
    def __init__(self, move_num, dna):
        self.move_num = move_num
        self.dna = dna

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move.

        The parameter "state" is of type ReversiGameState and has two useful
        member variables. The first is "board", which is an 8x8 numpy array
        of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If
        there is a 1 that means the spot has one of player 1's stones. If
        there is a 2 on the spot that means that spot has one of player 2's
        stones. The other useful member variable is "turn", which is 1 if it's
        player 1's turn and 2 if it's player 2's turn.

        ReversiGameState objects have a nice method called get_valid_moves.
        When you invoke it on a ReversiGameState object a list of valid
        moves for that state is returned in the form of a list of tuples.

        Move should be a tuple (row, col) of the move you want the bot to make.
        '''

        # have it get its dna from a file? or just copy and paste all this in so it can change globals...
        # DNA = self.dna

        valid_moves = state.get_valid_moves()

        # we need some way to evaluate the moves value... look in reversi.py gamestate

        move = rand.choice(valid_moves) # Moves randomly...for now

        move = alpha_beta(state, self.dna)

        
        return move


def alpha_beta(state, dna):
    iter = 0
    move = max_val(state, -math.inf, math.inf, iter, dna)[1] # returns a tuple, (val, move)
    return move # the action in ACTIONS(state) with value val


def terminal_test(state, iter):
    valid_moves = state.get_valid_moves()

    #  think of edge cases
    if len(valid_moves) == 1:
        return True
    elif iter > 7: # how deep it will go
        return True
    else:
        return False


def update_board(state, move):
    board = state.board
    row = move[0]
    col = move[1]

    # we know pieces are capturable, so we need to see which direction(s) we need to go
        # get current position number
        # check above, check below, right, left, and the four diagonals
        # for each, if the next is white, add it to a list and if another player of your team shows up, change them all
    board[row][col] = state.turn
    turn = board[row][col]

    # right
    temp = []
    for i in range(1, 8): # adding 1
        if row + i < 8:
            opp = board[row + i][col]
            if opp != turn:
                temp.append((row + i, col))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn
    
    # left
    temp = []
    for i in range(1, 8): # adding 1
        if row - i >= 0:
            opp = board[row - i][col]
            if opp != turn:
                temp.append((row - i, col))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn

    # up
    temp = []
    for i in range(1, 8): # adding 1
        if col + i < 8:
            opp = board[row][col + i]
            if opp != turn:
                temp.append((row, col + i))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn

    # down
    temp = []
    for i in range(1, 8): # adding 1
        if col - i >= 0:
            opp = board[row][col - i]
            if opp != turn:
                temp.append((row, col - i))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn


    # diags
    # up right
    temp = []
    for i in range(1, 8): # adding 1
        if col + i < 8 and row + i < 8:
            opp = board[row + i][col + i]
            if opp != turn:
                temp.append((row + i, col + i))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn

    # down right
    temp = []
    for i in range(1, 8): # adding 1
        if col - i >= 0 and row + i < 8:
            opp = board[row + i][col - i]
            if opp != turn:
                temp.append((row + i, col - i))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn

    # up left
    temp = []
    for i in range(1, 8): # adding 1
        if col + i < 8 and row - i >= 0:
            opp = board[row - i][col + i]
            if opp != turn:
                temp.append((row - i, col + i))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn
    
    # down left
    temp = []
    for i in range(1, 8): # adding 1
        if col - i >= 0 and row - i >= 0:
            opp = board[row - i][col - i]
            if opp != turn:
                temp.append((row - i, col - 1))
            if len(temp) >= 1 and opp == turn:
                # convert everything
                for n in temp:
                    board[n[0]][n[1]] = turn


    return board


# looks at how many we can get in a move
def get_num_captured(state):
    valid_moves = state.get_valid_moves()

    greatest_captured = -1
    best_move = None

    for move in valid_moves:
        captured = 0

        board = state.board
        row = move[0]
        col = move[1]

        # we know pieces are capturable, so we need to see which direction(s) we need to go
            # get current position number
            # check above, check below, right, left, and the four diagonals
            # for each, if the next is white, add it to a list and if another player of your team shows up, change them all
        turn = board[row][col]

        # right
        temp = []
        for i in range(1, 8): # adding 1
            if row + i < 8:
                opp = board[row + i][col]
                if opp != turn:
                    temp.append((row + i, col))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn
        
        # left
        temp = []
        for i in range(1, 8): # adding 1
            if row - i >= 0:
                opp = board[row - i][col]
                if opp != turn:
                    temp.append((row - i, col))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn

        # up
        temp = []
        for i in range(1, 8): # adding 1
            if col + i < 8:
                opp = board[row][col + i]
                if opp != turn:
                    temp.append((row, col + i))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn

        # down
        temp = []
        for i in range(1, 8): # adding 1
            if col - i >= 0:
                opp = board[row][col - i]
                if opp != turn:
                    temp.append((row, col - i))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn


        # diags
        # up right
        temp = []
        for i in range(1, 8): # adding 1
            if col + i < 8 and row + i < 8:
                opp = board[row + i][col + i]
                if opp != turn:
                    temp.append((row + i, col + i))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn

        # down right
        temp = []
        for i in range(1, 8): # adding 1
            if col - i >= 0 and row + i < 8:
                opp = board[row + i][col - i]
                if opp != turn:
                    temp.append((row + i, col - i))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn

        # up left
        temp = []
        for i in range(1, 8): # adding 1
            if col + i < 8 and row - i >= 0:
                opp = board[row - i][col + i]
                if opp != turn:
                    temp.append((row - i, col + i))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn
        
        # down left
        temp = []
        for i in range(1, 8): # adding 1
            if col - i >= 0 and row - i >= 0:
                opp = board[row - i][col - i]
                if opp != turn:
                    temp.append((row - i, col - 1))
                    captured += 1
                if len(temp) >= 1 and opp == turn:
                    # convert everything
                    for n in temp:
                        board[n[0]][n[1]] = turn

        if captured > greatest_captured:
            greatest_captured = captured
            best_move = move
    
    return (greatest_captured, best_move)
        

# looks at how many pieces we have
def total_pieces(state, move):

    valid_moves = state.get_valid_moves()

    greatest_captured = -1
    best_move = None

    old_state = copy.deepcopy(state)

    for move in valid_moves:
        temp_board = update_board(old_state, move)
        counter = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if temp_board[i][j] == state.turn:
                    counter += 1


 

        final_val = counter # + grid_value

        if final_val > greatest_captured:
            greatest_captured = final_val
            best_move = move

    return (greatest_captured, best_move)


def utility(state, dna):
    valid_moves = state.get_valid_moves()

    # I'm thinking use the grid to target key spots, this works pretty well
    grid = [
    [999, -8,  8,  6,  6,  8, -8, 999],
    [-8,-24, -4, -3, -3, -4,-24, -8],
    [ 8, -4,  7,  4,  4,  7, -4, 8],
    [ 6, -3,  4,  0,  0,  4,  3, 6],
    [ 6, -3,  4,  0,  0,  4,  3, 6],
    [ 8, -4,  7,  4,  4,  7, -4, 8],
    [-8,-24, -4, -3, -3, -4,-24, -8],
    [999, -8,  8,  6,  6,  8, -8, 999]
    ]

    largest = -999
    largest_iter = 0
    for i in range(0, len(valid_moves)):
        temp = valid_moves[i]
        value = grid[temp[0]][temp[1]]
        if value >= largest:
            largest = value
            largest_iter = i

    if len(valid_moves) == 0:
        largest = 0
        move = None
    else:
        move = valid_moves[largest_iter]

    grand_total = -9999

    # different way to choose...
    cap_tuple = get_num_captured(state) # deep copy?
    # return cap_tuple

    
    #return tot_tuple

    # print(dna)

    grid_score = dna[0] * largest
    cap_score = dna[1] * cap_tuple[0]

    if grid_score > cap_score:
        tot_tuple = total_pieces(state, move) # returns val and move
        grand_total = grid_score + dna[2] * tot_tuple[0]
    else:
        tot_tuple = total_pieces(state, cap_tuple[1]) # returns val and move
        grand_total = cap_score + dna[2] * tot_tuple[0]


    # [0] is for the grid, [1] is for the number captured, [2] is for the total pieces
    # grand_total = dna[0] * largest + dna[1] * cap_tuple[0] + dna[2] * tot_tuple[0]
    print(dna)
    print(grand_total, move)


    return (grand_total, move)


def result(state, move):
    # we can change the state board, 1 for p1 and 2 for p2
    row = move[0]
    col = move[1]

    state.board[row][col] = state.turn

    state.board = update_board(state, move)

    # switch turns
    if state.turn == 1:
        state.turn = 2
    elif state.turn == 2:
        state.turn = 1

    return state


def max_val(state, alpha, beta, iter, dna):
    # define terminal test: when in n in depth, or if there are no more decisions to be made it is terminal
    iter += 1

    if terminal_test(state, iter):
        return utility(state, dna)
    val = -math.inf

    # move = None # just in case?
    best_move = None
    valid_moves = state.get_valid_moves()
    for move in valid_moves: # I'm assuming where we can go
        min_result = min_val(result(copy.deepcopy(state), move), alpha, beta, iter, dna)
        if min_result[0] > val:
            val = min_result[0]# results would be what the new state will be
            best_move = min_result[1]

        if val >= beta:
            return (val, move) # same here? added tuple
        alpha = max(alpha, val)
        
    return (val, best_move) # I think we want to return a move... and the terminal test returns a value? TUPLES!!!


def min_val(state, alpha, beta, iter, dna):
    iter += 1
    if terminal_test(state, iter):
        return utility(state, dna)
    val = math.inf

    
    best_move = None # just in case?
    valid_moves = state.get_valid_moves()
    for move in valid_moves: # I'm assuming where we can go?
        #val = min(val, max_val(result(state, move), alpha, beta, iter)[0])
        max_result = max_val(result(copy.deepcopy(state), move), alpha, beta, iter, dna)
        if max_result[0] > val: # BUG?
            val = max_result[0]# results would be what the new state will be
            best_move = max_result[1]

        if val <= alpha:
            return (val, move)
        beta = min(beta, val)

    return (val, best_move)


