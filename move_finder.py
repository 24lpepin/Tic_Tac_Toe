import random
from typing import Literal

def find_random_move(gs):
    valid_moves = gs.get_valid_moves()
    if not valid_moves:
        return None  # Return None if no valid moves are available
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_move_minimax(gs, depth, turn: Literal[1, -1], max_depth=float('inf')):
    global counter
    counter += 1

    if gs.is_game_over() is not None:
        return gs.is_game_over()
    
    if depth >= max_depth:
        return 0

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, depth + 1, turn * -1, max_depth)
            gs.undo_move()
            max_score = max(score, max_score)
        return max_score

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, depth + 1, turn * -1, max_depth)
            gs.undo_move()
            min_score = min(score, min_score)
        return min_score

def find_move_minimax_alpha_beta(gs, depth, turn: Literal[1, -1], alpha, beta, max_depth=float('inf')):
    global counter
    counter += 1
    
    if gs.is_game_over() is not None:
        return gs.is_game_over()
    
    if depth >= max_depth:
        return 0

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_alpha_beta(gs, depth + 1, turn * -1, alpha, beta, max_depth)
            gs.undo_move()
            max_score = max(score, max_score)
            alpha = max(score, alpha)
            if beta <= alpha:
                break
        return max_score

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_alpha_beta(gs, depth + 1, turn * -1, alpha, beta, max_depth)
            gs.undo_move()
            min_score = min(score, min_score)
            beta = min(score, beta)
            if beta <= alpha:
                break
        return min_score
    
def find_move_minimax_move_ordering(gs, depth, turn: Literal[1, -1], alpha, beta, max_depth=float('inf')):
    global counter
    counter += 1

    if counter % 100000 == 0:
        print(counter)
    
    if gs.is_game_over() is not None:
        return gs.is_game_over()
    
    if depth >= max_depth:
        return gs.score_board()

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    valid_moves = order_moves(gs, valid_moves, turn) #orders the moves so that the best moves are at the beginning of the list

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_move_ordering(gs, depth + 1, turn * -1, alpha, beta, max_depth)
            gs.undo_move()
            max_score = max(score, max_score)
            alpha = max(score, alpha)
            if beta <= alpha:
                break
        return max_score

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_move_ordering(gs, depth + 1, turn * -1, alpha, beta, max_depth)
            gs.undo_move()
            min_score = min(score, min_score)
            beta = min(score, beta)
            if beta <= alpha:
                break
        return min_score

def order_moves(gs, valid_moves, turn):
    move_scores = []

    for move in valid_moves:
        gs.make_move(move[0], move[1])
        score = turn * gs.score_move(move) #Updates the score based on the last move
        move_scores.append((move, score))
        gs.undo_move()
    
    move_scores.sort(key=lambda x: x[1], reverse=(turn == 1)) #do i need to reverse this? the numbers are negative when turn is O
    
    moves = []
    for move, score in move_scores:
        moves.append(move)
    return moves
        

def find_best_move(gs, max_depth=float('inf')):
    global counter
    counter = 0

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    turn = gs.turn
    list_of_moves = []

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_move_ordering(gs, 0, turn * -1, -float('inf'), float('inf'), max_depth)
            gs.undo_move()
            if score > max_score:
                max_score = score
                list_of_moves = [move]
            elif score == max_score:
                list_of_moves.append(move)

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax_move_ordering(gs, 0, turn * -1, -float('inf'), float('inf'), max_depth)
            gs.undo_move()
            if score < min_score:
                min_score = score
                list_of_moves = [move]
            elif score == min_score:
                list_of_moves.append(move)
    
    print(list_of_moves, counter)
    return list_of_moves
