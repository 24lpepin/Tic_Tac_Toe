"""
Handles the graphics (drawing) of the game
"""
import game_engine
import pygame

class Graphics:
    def __init__(self, board_size=3, screen_size=512) -> None:
        self.BOARD_SIZE = board_size #board size
        self.SCREEN_WIDTH = self.SCREEN_HEIGHT = screen_size
        self.SQ_SIZE = self.SCREEN_HEIGHT/self.BOARD_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.IMAGES = {}

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.screen.fill(pygame.Color("white"))

    def load_images(self):
        self.IMAGES[0] = (pygame.transform.scale(pygame.image.load("images\\tic_tac_toe_o.png"), (self.SQ_SIZE, self.SQ_SIZE)))
        self.IMAGES[1] = (pygame.transform.scale(pygame.image.load("images\\tic_tac_toe_x.png"), (self.SQ_SIZE, self.SQ_SIZE)))

    def draw_board(self):
        global colors
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.screen, color, pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_game_state(self, board):
        """
        Responsible for all the graphics within a current game state
        """
        self.draw_board()  # draws squares on the board
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if board[r][c] != 0:
                    self.screen.blit(self.IMAGES[0 if board[r][c] == -1 else 1], pygame.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def draw_end_text(self, text):
        font = pygame.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, 0, pygame.Color('Gray'))
        text_location = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT).move(self.SCREEN_WIDTH / 2 - text_object.get_width() / 2,
                                                                    self.SCREEN_HEIGHT / 2 - text_object.get_height() / 2)
        self.screen.blit(text_object, text_location)
        text_object = font.render(text, 0, pygame.Color('Black'))
        self.screen.blit(text_object, text_location.move(-2, -2))

        