# backend/chess_board.py
import copy

class ChessBoard:
    def __init__(self):
        """Initialize the board and set up the default layout."""
        self.board = []
        self.setup_default()

    def setup_default(self):
        """Set up the board with the standard chess layout."""
        self.board = [
            ['r', 't', 'b', 'q', 'k', 'b', 't', '.'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', '.'],
            ['.', '.', '.', '.', '.', '.', '.', 'P'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],
            ['R', 'T', 'B', 'Q', 'K', 'B', 'T', 'R']
        ]

    def get_state(self):
        """Return the current board state."""
        return self.board

    def draw_board(self):
        """Print the current board state."""
        for row in self.board:
            print(" ".join(row))
        print()

    def move_piece(self, from_pos, to_pos):
        """Move a piece if the move is legal."""
        from_col, from_row = from_pos
        to_col, to_row = to_pos
        piece = self.board[from_row][from_col]
        
        if self.is_move_legal(from_pos, to_pos):
            # Perform the move
            
            

            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = '.'

            if (piece == 'P' and to_row == 0):
                print("White pawn promoted!")
                self.promote_pawn((to_col, to_row), 'Q')
            elif (piece == 'p' and to_row == 0):
                #print("Black pawn promoted!")
                self.promote_pawn((to_col, to_row), 'q')

            return True
        else:
            
            return False


    def promote_pawn(self, position, promo_piece):
        col,row = position
        if self.board[row][col] == 'P':
            self.board[row][col] = promo_piece.upper()
        if self.board[row][col] == 'p':
            self.board[row][col] = promo_piece.lower()
        



    def is_move_legal(self, from_square, to_square):
        """Determine if a move is legal for the piece at from_square."""
        from_col, from_row = from_square
        to_col, to_row = to_square
        from_piece = self.board[from_row][from_col]
        to_piece = self.board[to_row][to_col]
        is_white = from_piece.isupper()
        is_black = from_piece.islower()
        if from_square == to_square:
            return False

        if from_piece.lower() == 'p':
            return self.is_pawn_move_legal(from_square, to_square, is_white, log_rejection=False)
        if from_piece.lower() == 'r':
            return self.is_rook_move_legal(from_square, to_square, is_white)
        if from_piece.lower() == 'b':
            return self.is_bishop_move_legal(from_square, to_square, is_white)
        if from_piece.lower() == 'q':
            return self.is_queen_move_legal(from_square, to_square, is_white)
        if from_piece.lower() == 't':
            return self.is_knight_move_legal(from_square, to_square, is_white)
        if from_piece.lower() == 'k':
            return self.is_king_move_legal(from_square, to_square, is_white)
        return False

    # --- Piece movement rules ---
    def is_pawn_move_legal(self, from_square, to_square, is_white, log_rejection=False):
        from_col, from_row = from_square
        to_col, to_row = to_square
        to_piece = self.board[to_row][to_col]

        if is_white:
        # Move forward one square
            if from_row - to_row == 1 and from_col == to_col and to_piece == '.':
                return True
            # Move forward two squares from starting position
            elif from_row - to_row == 2 and from_col == to_col and from_row == 6 and to_piece == '.' and self.board[from_row - 1][from_col] == '.' and self.is_clear_path(from_square, to_square):
                return True
            # Capture diagonally
            elif from_row - to_row == 1 and abs(to_col - from_col) == 1 and to_piece != '.' and to_piece.islower():
                return True
        else:
        # Move forward one square
            if to_row - from_row == 1 and from_col == to_col and to_piece == '.':
                return True
            # Move forward two squares from starting position
            elif to_row - from_row == 2 and from_col == to_col and from_row == 1 and to_piece == '.' and self.board[from_row + 1][from_col] == '.' and self.is_clear_path(from_square, to_square):
                return True
            # Capture diagonally
            elif to_row - from_row == 1 and abs(to_col - from_col) == 1 and to_piece != '.' and to_piece.isupper():
                return True
        return False






    def is_rook_move_legal(self, from_square, to_square, is_white):
        from_col, from_row = from_square
        to_col, to_row = to_square
        to_piece = self.board[to_row][to_col]

        if (to_row == from_row or to_col == from_col) and self.is_clear_path(from_square, to_square):
            if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                return True
        return False

    def is_bishop_move_legal(self, from_square, to_square, is_white):
        from_col, from_row = from_square
        to_col, to_row = to_square
        to_piece = self.board[to_row][to_col]

        if abs(to_row - from_row) == abs(to_col - from_col) and self.is_clear_path(from_square, to_square):
            if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                return True
        return False

    def is_queen_move_legal(self, from_square, to_square, is_white):
        return self.is_rook_move_legal(from_square, to_square, is_white) or self.is_bishop_move_legal(from_square, to_square, is_white)

    def is_knight_move_legal(self, from_square, to_square, is_white):
        from_col, from_row = from_square
        to_col, to_row = to_square
        to_piece = self.board[to_row][to_col]

        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for move in knight_moves:
            if (to_row == from_row + move[0]) and (to_col == from_col + move[1]):
                if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                    return True
        return False

    def is_king_move_legal(self, from_square, to_square, is_white):
        from_col, from_row = from_square
        to_col, to_row = to_square
        to_piece = self.board[to_row][to_col]

        if abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1:
            if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                return True
        return False

    # --- Helper functions ---

    def is_in_check(self, player):
        """Check if the current player's king is in check."""
        king_piece = 'K' if player == 'white' else 'k'
        king_pos = None

        # Find the king's position
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    king_pos = (col, row)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        # Check if any opposing piece can attack the king
        enemy_is_white = player == 'black'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (enemy_is_white and piece.isupper()) or (not enemy_is_white and piece.islower()):
                    if self.is_move_legal((col, row), king_pos):
                        return True
        return False



    def is_checkmate(self, player):
        """Check if the current player is in checkmate."""
        if self.is_in_check(player):
            if not self.get_pieces_with_legal_moves(player):
                return True
        return False

    import copy

    def does_move_put_player_in_check(self, player, from_square, to_square):
        """Simulate a move on a copy of the board to check if it leaves the player in check."""
        # Create a deep copy of the entire board object (self)
        board_copy = copy.deepcopy(self)
        
        # Extract coordinates for clarity
        from_col, from_row = from_square
        to_col, to_row = to_square
        
        # Simulate the move on the copied board state:
        board_copy.board[to_row][to_col] = board_copy.board[from_row][from_col]
        board_copy.board[from_row][from_col] = '.'
        
        # Now use the copied board's is_in_check() to determine if the move leaves the player in check.
        return board_copy.is_in_check(player)


    # --- Move generation ---
    def get_list_of_legal_moves(self, from_square):
        """Get a list of legal moves for the piece at from_square."""
        legal_moves = []
        from_col, from_row = from_square
        piece = self.board[from_row][from_col]


        if piece.isupper():
            player = 'white'
        else:
            player = 'black'
            
        if piece == '.':
            return []

        

        for row in range(8):
            for col in range(8):
                to_square = (col, row)
                if self.is_move_legal(from_square, to_square) and not self.does_move_put_player_in_check(player, from_square, to_square):
                    legal_moves.append(to_square)

        return legal_moves

    def get_pieces_with_legal_moves(self, player):
        """Get a list of pieces that have at least one legal move."""
        legal_pieces = []

        for row in range(8):
            for col in range(8):
                from_square = self.board[col][row]
                from_co = (row, col)


                if(player == 'white'):
                    if(from_square.isupper()):
                        if self.get_list_of_legal_moves(from_co):
                            legal_pieces.append(from_co)
                else:
                    if(player == 'black'):
                        if(from_square.islower()):
                            if self.get_list_of_legal_moves(from_co):
                                legal_pieces.append(from_co)


               

        return legal_pieces
    





    
    def is_clear_path(self, from_square, to_square):
        from_col, from_row = from_square
        to_col, to_row = to_square

        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        current_row, current_col = from_row + row_step, from_col + col_step
        while (current_row, current_col) != (to_row, to_col):
            if self.board[current_row][current_col] != '.':
                return False
            current_row += row_step
            current_col += col_step

        return True
