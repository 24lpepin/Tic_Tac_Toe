import random
from typing import Literal
import math

def find_random_move(gs):
    valid_moves = gs.get_valid_moves()
    if not valid_moves:
        return None  # Return None if no valid moves are available
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

def find_best_move(gs):
    global counter, move_score_log
    move_score_log = []
    counter = 0

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    turn = gs.turn
    list_of_moves = []
    memo = {}
    max_depth = dynamic_depth(valid_moves, gs.get_board_size()[0], gs.get_board_size()[0])

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_memoization(gs, 0, turn * -1, -float('inf'), float('inf'), memo, max_depth)
            gs.undo_move()
            print(f"Move: {move}, Score: {score}")
            if score > max_score:
                max_score = score
                list_of_moves = [move]
                move_score_log = [(move, score)]
            elif score == max_score:
                list_of_moves.append(move)
                move_score_log.append((move, score))

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_memoization(gs, 0, turn * -1, -float('inf'), float('inf'), memo, max_depth)
            gs.undo_move()
            print(f"Move: {move}, Score: {score}")
            if score < min_score:
                #print(f"updating score {min_score} -> {score} for {move}")
                min_score = score
                list_of_moves = [move]
                move_score_log = [(move, score)]
            elif score == min_score:
                #print(f"adding to list {min_score} -> {score} for {move}")
                list_of_moves.append(move)
                move_score_log.append((move, score))

    print(f"Counter: {counter}")
    print("Move scores log:", move_score_log)
    print("Memo size:", len(memo))
    print("Max Depth: ", max_depth)
    return list_of_moves

def find_move_minimax_memoization(gs, depth, turn: Literal[1, -1], alpha, beta, memo, max_depth=float('inf')):
    global counter
    counter += 1

    if counter % 100000 == 0:
        print(counter)

    key = gs_to_key(gs, turn, depth)
    if key in memo:
        return memo[key]
    
    game_over_status = gs.is_game_over()
    if game_over_status is not None:
        memo[key] = game_over_status * 10000
        return game_over_status * 10000
    
    if depth >= max_depth:
        #board_score = gs.score_board()
        return gs.board_score

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    valid_moves = order_moves(gs, valid_moves, turn) #orders the moves so that the best moves are at the beginning of the list
    max_depth = dynamic_depth(valid_moves, gs.get_board_size()[0], gs.get_board_size()[1])

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_memoization(gs, depth + 1, -turn, alpha, beta, memo, max_depth)
            gs.undo_move()
            max_score = max(score, max_score)
            alpha = max(score, alpha)
            if beta <= alpha:
                break
        memo[key] = max_score
        return max_score

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_memoization(gs, depth + 1, -turn, alpha, beta, memo, max_depth)
            gs.undo_move()
            min_score = min(score, min_score)
            beta = min(score, beta)
            if beta <= alpha:
                break
        memo[key] = min_score
        return min_score

def normalized_board_key(gs, turn): #chat gpt
    def rotate_board(board):
        """Rotate board 90 degrees clockwise."""
        return [list(row) for row in zip(*board[::-1])]

    def reflect_board(board):
        """Reflect board horizontally."""
        return [row[::-1] for row in board]
    
    board = gs.get_board()
    
    # Get all rotations and reflections of the board
    transformations = [
        board,
        rotate_board(board),
        rotate_board(rotate_board(board)),
        rotate_board(rotate_board(rotate_board(board))),
        reflect_board(board),
        reflect_board(rotate_board(board)),
        reflect_board(rotate_board(rotate_board(board))),
        reflect_board(rotate_board(rotate_board(rotate_board(board))))
    ]
    
    # Convert each transformation to a string and select the lexicographically smallest one
    canonical_form = min(''.join(str(col) for row in transformed for col in row) for transformed in transformations)
    return canonical_form + f"_{turn}"

def order_moves(gs, valid_moves, turn):
    move_scores = []

    for move in valid_moves:
        gs.make_move(move[0], move[1])
        score = turn * gs.score_move(move) #Updates the score based on the last move
        move_scores.append((move, score))
        gs.undo_move()
    
    move_scores.sort(key=lambda x: x[1], reverse=(turn == 1)) 
    
    return [move for move, score in move_scores]

def gs_to_key(gs, turn, depth):
    board = gs.get_board()
    key = ""
    for row in board:
        for col in row:
            key += f"{col}"
        key += " "
    key += f"{turn} {depth}"
    
    return key
        
def dynamic_depth(valid_moves, board_length, board_width):
    early_game_size = math.ceil(board_length * board_width / 1.5)
    mid_game_size = math.ceil(board_length * board_width / 2.5)
    num_moves = len(valid_moves)

    if math.sqrt(board_length * board_width) <= 3.1: #if the board is small, max depth is 10
        return 10
    elif math.sqrt(board_length * board_width) <= 5.1: #medium board size
        if num_moves > early_game_size:
            return 5
        elif num_moves > mid_game_size:
            return 7
        else:
            return 10
    else:
        if num_moves > early_game_size:
            return 4
        elif num_moves > mid_game_size:
            return 6
        else:
            return 8


