"""
an algorithm that finds the best move
"""

import random
import game_engine

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]
