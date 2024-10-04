"""
handles the main game, including user and algorithm moves, and game display
"""

import game_engine
import pygame
import graphics

pygame.init()

if __name__ == "__main__":
    BOARD_SIZE = 6
    WIN_CONDITION = 4 #number of symbols in a row for a win
    gs = game_engine.GameState(BOARD_SIZE, WIN_CONDITION)
    graphics = graphics.Graphics(BOARD_SIZE)

    graphics.load_images()
    game_over = False
    running = True

    ai_thinking = False
    move_finder_process = None
    move_undone = False

    player_one = True  # If a human is playing X, this will be true. If it's an AI playing X, it will be false
    player_two = True  # Same as above but for O

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handlers
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    col = location[0] // graphics.SQ_SIZE
                    row = location[1] // graphics.SQ_SIZE
                    gs.make_move(row, col)
                # key handlers
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    game_over = False
                    result = None
                    
                if e.key == pygame.K_r:  # resets game when r is pressed
                    gs = game_engine.GameState(BOARD_SIZE, WIN_CONDITION)
                    game_over = False
                    result = None
        
        graphics.draw_game_state(gs.board)
        result = gs.is_game_over()
        if result != None:
            if result == 1:
                text = "X wins"
            elif result == -1:
                text = "O wins"
            elif result == 0:
                text = "Tie"
            graphics.draw_end_text(text)
            game_over = True

        pygame.display.flip()

