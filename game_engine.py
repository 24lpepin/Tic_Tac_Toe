"""
handles the game state, i.e. board state and board updates
"""

class GameState:
    def __init__(self, n=3, win_condition=3):
        self.board_size = n #board size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.move_log = []
        self.turn = 1 #1 => X to move, -1 => O to move
        self.game_over = None
        self.win_condition = win_condition #number of squares in a row needed to win
        self.score = 0
    
    def make_move(self, row, col):
        row = int(row)
        col = int(col)
        if self.board[row][col] == 0:
            self.move_log.append((row,col))
            self.board[row][col] = self.turn
            self.turn *= -1

        self.game_over = self.check_game_over(row, col)

    def undo_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log[len(self.move_log)-1]
            self.board[last_move[0]][last_move[1]] = 0
            self.turn *= -1
            self.game_over = None
            self.move_log.pop()

    def is_game_over(self):
        return self.game_over
    
    def check_game_over(self, row_moved, col_moved):
        player = self.board[row_moved][col_moved]

        # Check the row of the last move
        row = self.board[row_moved]
        if self.count_consecutive(row, self.win_condition):
            return player  

        # Check the column of the last move
        column = [self.board[row][col_moved] for row in range(self.board_size)]
        if self.count_consecutive(column, self.win_condition):
            return player  

        # Check the main diagonal
        main_diagonal = []
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
        anti_diagonal = []
        while row_moved >= 0 and col_moved <= self.board_size - 1: #moving to top right of diagonal
            row_moved -= 1
            col_moved += 1
        while row_moved < self.board_size - 1 and col_moved > 0: #creating list from top right to bottom left of diagonal
            row_moved += 1
            col_moved -= 1
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

    def get_valid_moves(self):
        valid_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    valid_moves.append((row,col))

        return valid_moves
    
    def get_board(self):
        return self.board
    
    def score_board(self): #TODO     
        return self.score
    
    def score_move(self, move):
        score = 0
        #1) winning move
        if self.check_game_over(move[0], move[1]):
            return 10000
        
        #2) blocking move
        if self.is_blocking_move(move):
            score += 90
        
        #3) location (central vs diagonals vs edges)
        score += self.evaluate_centrality(move)

        #4) winning chances (# in a row currently)

        #5) threats
        return score
    
    def evaluate_centrality(self, move):
        row, col = move
        score = 0

        center_row = len(self.board) // 2
        center_col = len(self.board[0]) // 2
        distance_to_center = abs(row - center_row) + abs(col - center_col)

        board_size = len(self.board) * len(self.board[0])
    
        
        if board_size <= 16:  
            central_importance = 75  
        elif board_size <= 36:  
            central_importance = 50
        else:
            central_importance = 30  

        score += (len(self.board) + len(self.board[0]) - distance_to_center) * central_importance / (board_size/2)
        return score



    def is_blocking_move(self, move):
        row, col = move
        opponent_turn = -self.turn  # Opponent's turn is the opposite of current turn (if self.turn is 1, opponent is -1)

        # Temporarily make the opponent's move in the given position
        self.board[row][col] = opponent_turn

        # Check if this move would have resulted in a win for the opponent
        if self.check_game_over(row, col) == opponent_turn:  
            # Undo the opponent's move
            return True  # It's a blocking move

        # Undo the opponent's move if it's not a winning move
        return False
    
    def print_board(self):
        for row in self.board:
            r = ""
            for col in row:
                r += f"{col}, "
            print(r)
