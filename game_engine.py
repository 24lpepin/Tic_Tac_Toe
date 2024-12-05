"""
handles the game state, i.e. board state and board updates
"""

class GameState:
    def __init__(self, n=3, win_condition=3):
        self.board_size = n #board size
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.empty_squares = n * n
        self.move_log = []
        self.turn = 1 #1 => X to move, -1 => O to move
        self.game_over = None
        self.win_condition = win_condition #number of squares in a row needed to win
        self.score = 0
        self.centrality_scores = self.centrality_scores = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.compute_centrality_scores()
        self.board_score = 0
        self.board_score_log = [0]

    def print_board(self):
        for row in self.board:
            r = ""
            for col in row:
                r += f"{col}, "
            print(r)

    def get_valid_moves(self):
        valid_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    valid_moves.append((row,col))

        return valid_moves
    
    def get_board(self):
        return self.board
    
    def get_board_size(self):
        return (self.board_size, self.board_size)
    
    def is_game_over(self):
        return self.game_over
    
    def compute_centrality_scores(self):

        center_row = len(self.board) // 2
        center_col = len(self.board[0]) // 2
        board_size = len(self.board) * len(self.board[0])

        if board_size <= 16:  
            central_importance = 250  
        elif board_size <= 36:  
            central_importance = 150
        elif board_size <= 64:
            central_importance = 75
        else:
            central_importance = 50 

        for row in range(self.board_size):
            for col in range(self.board_size):
                distance_to_center = abs(row - center_row) + abs(col - center_col)
                score = (2 * self.board_size - distance_to_center) * central_importance / (board_size / 2)
                self.centrality_scores[row][col] = score

    def make_move(self, row, col):
        row = int(row)
        col = int(col)
        if self.board[row][col] == 0:
            # Log the move
            self.move_log.append((row, col))
            
            # Update the board and score before switching the turn
            self.board[row][col] = self.turn
            self.board_score += self.turn * self.score_move((row, col))  # Add the current move's contribution to the board score
            self.board_score_log.append(self.board_score)
            self.empty_squares -= 1
            
            # Switch turns
            self.turn *= -1

            # Check if the game is over
            self.game_over = self.check_game_over(row, col)

    def undo_move(self):
        if len(self.move_log) != 0:
            # Undo the last move
            last_move = self.move_log.pop()
            row, col = last_move

            # Restore the board and score
            self.board[row][col] = 0
            self.board_score = self.board_score_log.pop()  # Restore the previous score
            self.empty_squares += 1

            # Switch turns back
            self.turn *= -1

            # Reset game-over status
            self.game_over = None
    
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
        if self.empty_squares == 0:
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
    
    def score_board(self):
        score = 0

        # Evaluate centrality
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                score += self.board[row][col] * self.centrality_scores[row][col]

        # Evaluate winning chances
        score += self.evaluate_winning_chances() * 50 

        return round(score, 2)
    
    def evaluate_winning_chances(self):
        """
        Checks if it is possible for X or O to win in a given row/column/diagonal
        """
        winning_chances = 0

        for row_moved in range(len(self.board)): #iterate through each square in the board
            for col_moved in range(len(self.board[0])):

                player = self.board[row_moved][col_moved]
                
                row = self.board[row_moved]
                # Check the row of the square
                if self.count_winning_chances(row, player) >= self.win_condition:
                    winning_chances += 1

                # Check the column of the last move
                col = [self.board[row][col_moved] for row in range(self.board_size)]
                if self.count_winning_chances(col, player) >= self.win_condition:
                    winning_chances += 1

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
                if self.count_winning_chances(main_diagonal, player) >= self.win_condition:
                    winning_chances += 1
                
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
                if self.count_winning_chances(anti_diagonal, player) >= self.win_condition:
                    winning_chances += 1

        return winning_chances
    
    def count_winning_chances(self, line, player):
        """
        Counts the number of squares in a row that are the player or empty
        """
        consecutive = 0
        max_consecutive = 0
        for cell in line:
            if cell == player or cell == 0:
                consecutive += 1
            else:
                max_consecutive = max(max_consecutive, consecutive)
                consecutive = 0  # Opponent's piece blocks the sequence

        return consecutive
    
    def score_move(self, move):
        if move == None: #score_board() function
            move = self.move_log[-1]

        score = 0
        #1) winning move
        if self.check_game_over(move[0], move[1]):
            return 10000
        
        #2) blocking move
        if self.is_blocking_move(move):
            score += 5000
        
        #3) location (central vs diagonals vs edges)
        score += self.evaluate_centrality(move)

        #4) winning chances (# in a row currently)
        score += 100 * self.max_number_in_a_row(move)

        #5) threats
        return round(score, 2)
    
    def evaluate_centrality(self, move):
        row, col = move
        score = self.centrality_scores[row][col]
        return score

    def max_number_in_a_row(self, move):
        row, col = move
        symbol = self.turn

        max_in_a_row = max(
            self.count_in_direction(row, col, 0, 1, symbol),  # Row
            self.count_in_direction(row, col, 1, 0, symbol),  # Column
            self.count_in_direction(row, col, 1, 1, symbol),  # Main diagonal
            self.count_in_direction(row, col, 1, -1, symbol)  # Anti-diagonal
        )

        return max_in_a_row

    def count_in_direction(self, row, col, d_row, d_col, symbol):
        count = 0
        for direction in [-1, 1]:
            r, c = row, col
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == symbol:
                count += 1
                r += d_row * direction
                c += d_col * direction
        return count - 1 
            
    def is_blocking_move(self, move):
        row, col = move
        opponent = -self.turn
        self.board[row][col] = opponent #what if opponent had made that move?
        blocking = self.check_game_over(row, col) == opponent
        self.board[row][col] = self.turn
        return blocking
    
