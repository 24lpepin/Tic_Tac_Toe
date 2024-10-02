"""
handles the game state, i.e. board state and board updates
"""

class GameState:
    def __init__(self, n=3, win_condition=3):
        self.board_size = n #board size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.turn = 1 #1 => X to move, -1 => O to move
        self.game_over = None
        self.win_condition = win_condition #number of squares in a row needed to win
    
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
        if self.count_consecutive(self.board[row_moved], self.win_condition):
            return player  

        # Check the column of the last move
        if self.count_consecutive([self.board[row][col_moved] for row in range(self.board_size)], self.win_condition):
            return player  

        # Check the main diagonal
        main_diagonal = [self.board[row_moved][col_moved]]
        row_moved_copy = row_moved
        col_moved_copy = col_moved
        while row_moved >= 0 and col_moved >= 0: #move to the top left of diagonal
            row_moved -= 1
            col_moved -= 1
        while row_moved < self.board_size-1 and col_moved < self.board_size-1: #creating list from top left to bottom right of diagonal
            row_moved += 1
            col_moved += 1
            main_diagonal.append(self.board[row_moved][col_moved])
        if self.count_consecutive(main_diagonal, self.win_condition):
            return player
        
        # Check the anti-diagonal
        row_moved = row_moved_copy
        col_moved = col_moved_copy
        anti_diagonal = [self.board[row_moved][col_moved]]
        while row_moved < self.board_size-1 and col_moved >= 0: #moving to top right of diagonal
            row_moved += 1
            col_moved -= 1
        while row_moved >= 0 and col_moved < self.board_size-1: #creating list from top right to bottom left of diagonal
            row_moved -= 1
            col_moved += 1
            anti_diagonal.append(self.board[row_moved][col_moved])
        if self.count_consecutive(anti_diagonal, self.win_condition):
            return player

        # Check for a tie condition
        if all(self.board[row][col] != 0 for row in range(self.board_size) for col in range(self.board_size)):
            return 0  

        # Game is not over yet
        return None

    def count_consecutive(self, list, num_in_a_row):
        """
        Counts if there are num_in_a_row numbers consecutively in a given list of numbers.
        """
        count = 1
        for i in range(1, len(list)):
            if list[i] != 0 and list[i] == list[i-1]: #checks if two consecutive squares are occupied and have the same value 
                count += 1 
                if count == num_in_a_row: 
                    return True
            else:
                count = 1 
        return False 
