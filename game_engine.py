"""
handles the game state, i.e. board state and board updates
"""

class GameState:
    def __init__(self, n=3):
        self.n = n #board size
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.turn = 1 #1 => X to move, -1 => O to move
        self.game_over = None
    
    def make_move(self, row, col):
        row = int(row)
        col = int(col)
        if self.board[row][col] == 0:
            self.board[row][col] = self.turn
            self.turn *= -1

        self.game_over = self.check_game_over(row, col)
    
    def is_game_over(self):
        return self.game_over
    
    def check_game_over(self, row_moved, col_moved):
        player = self.board[row_moved][col_moved]

        # Check the row of the last move
        if all(self.board[row_moved][col] == player for col in range(self.n)):
            return player  # Player wins

        # Check the column of the last move
        if all(self.board[row][col_moved] == player for row in range(self.n)):
            return player  # Player wins

        # Check the main diagonal if the move is on it (row == col)
        if row_moved == col_moved:
            if all(self.board[i][i] == player for i in range(self.n)):
                return player  # Player wins

        # Check the anti-diagonal if the move is on it (row + col == n - 1)
        if row_moved + col_moved == self.n - 1:
            if all(self.board[i][self.n - 1 - i] == player for i in range(self.n)):
                return player  # Player wins

        # Check if the board is full (tie condition)
        if all(self.board[row][col] != 0 for row in range(self.n) for col in range(self.n)):
            return 0

        # Game is not over yet
        return None
    
