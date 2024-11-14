import random
from typing import Literal

def find_random_move(gs):
    valid_moves = gs.get_valid_moves()
    if not valid_moves:
        return None  # Return None if no valid moves are available
    return valid_moves[random.randint(0, len(valid_moves) - 1)]
    
def find_move_negamax_memoization(gs, depth, turn: Literal[1, -1], alpha, beta, memo, max_depth=float('inf')):
    global counter
    counter += 1

    if counter % 100000 == 0:
        print(counter)

    key = normalized_board_key(gs, turn)
    if key in memo:
        return memo[key]
    
    game_over_status = gs.is_game_over()
    if game_over_status is not None:
        memo[key] = turn * game_over_status
        return turn * game_over_status
    
    if depth >= max_depth:
        return gs.score_board()

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    valid_moves = order_moves(gs, valid_moves, turn) #orders the moves so that the best moves are at the beginning of the list

    max_score = -float('inf')
    
    for move in valid_moves:
        gs.make_move(move[0], move[1])
        score = -find_move_negamax_memoization(gs, depth + 1, -turn, -beta, -alpha, memo, max_depth)
        gs.undo_move()
        
        max_score = max(max_score, score)
        alpha = max(alpha, score)

        if alpha >= beta:
            break
    memo[key] = max_score
    return max_score

def normalized_board_key(gs, turn): #chat gpt
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

def rotate_board(board):
    """Rotate board 90 degrees clockwise."""
    return [list(row) for row in zip(*board[::-1])]

def reflect_board(board):
    """Reflect board horizontally."""
    return [row[::-1] for row in board]

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
        

def find_best_move(gs, max_depth=float('inf')):
    global counter, move_score_log
    move_score_log = []
    counter = 0

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    turn = gs.turn
    list_of_moves = []
    memo = {}

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            print("1", move)
            gs.make_move(move[0], move[1])
            score = find_move_negamax_memoization(gs, 0, turn * -1, -float('inf'), float('inf'), memo, max_depth)
            gs.undo_move()
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
            score = find_move_negamax_memoization(gs, 0, turn * -1, -float('inf'), float('inf'), memo, max_depth)
            print("-1", move, score)
            gs.undo_move()
            if score < min_score:
                print(f"updating score {min_score} -> {score} for {move}")
                min_score = score
                list_of_moves = [move]
                move_score_log = [(move, score)]
            elif score == min_score:
                print(f"adding to list {min_score} -> {score} for {move}")
                list_of_moves.append(move)
                move_score_log.append((move, score))

    print(f"Counter: {counter}")
    print("Move scores log:", move_score_log)
    print("Memo size:", len(memo))
    return list_of_moves
