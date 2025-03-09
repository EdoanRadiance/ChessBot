# backend/chess_board.py
import copy

class ChessBoard:
    def __init__(self):
        """Initialize the board and set up the default layout."""
        self.board = []
        self.setup_default()
        self.debug_count = 0

    def setup_default(self):
        """Set up the board with the standard chess layout."""
        # Note: row 0 is the top and row 7 is the bottom.
        self.board = [
            ['r', 't', 'b', 'q', 'k', 'b', 't', '.'],  # Row 0: Black major pieces
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', '.'],  # Row 1: Black pawns
            ['.', '.', '.', '.', '.', '.', '.', 'P'],  # Row 2
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Row 3
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Row 4
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Row 5
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],  # Row 6: White pawns
            ['R', 'T', 'B', 'Q', 'K', 'B', 'T', 'R']   # Row 7: White major pieces
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
        """Move a piece if the move is legal.
        
        Coordinates in from_pos and to_pos are in (row, col) order.
        """
        # Unpack coordinates as (row, col)
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]

        # Debug message (will print only the first 20 calls)
        if self.debug_count < 20:
            print(f"[DEBUG] Moving piece from {from_pos} (board[{from_row}][{from_col}]) "
                  f"to {to_pos} (board[{to_row}][{to_col}]), piece: {piece}")
            self.debug_count += 1

        if self.is_move_legal(from_pos, to_pos):
            # Perform the move
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = '.'

            # Promotion conditions:
            # White pawn ('P') promotes when reaching row 0 (top)
            if piece == 'P' and to_row == 0:
                #print("White pawn promoted!")
                self.promote_pawn((to_row, to_col), 'Q')
            # Black pawn ('p') promotes when reaching row 7 (bottom)
            elif piece == 'p' and to_row == 7:
                #print("Black pawn promoted!")
                self.promote_pawn((to_row, to_col), 'q')

            return True
        else:
            return False

    def promote_pawn(self, position, promo_piece):
        """Promote a pawn at the given (row, col) position."""
        row, col = position
        if self.board[row][col] == 'P':
            self.board[row][col] = promo_piece.upper()
        elif self.board[row][col] == 'p':
            self.board[row][col] = promo_piece.lower()

    def is_move_legal(self, from_square, to_square):
        """Determine if a move is legal for the piece at from_square.
        
        Coordinates are expected in (row, col) order.
        """
        from_row, from_col = from_square
        to_row, to_col = to_square
        from_piece = self.board[from_row][from_col]
        to_piece = self.board[to_row][to_col]
        is_white = from_piece.isupper()
        # is_black is not used further, so we can omit it if desired.
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
        from_row, from_col = from_square
        to_row, to_col = to_square
        to_piece = self.board[to_row][to_col]

        if is_white:
            # White pawns move upward (to lower row numbers)
            # Move forward one square
            if from_row - to_row == 1 and from_col == to_col and to_piece == '.':
                return True
            # Move forward two squares from starting position (row 6)
            elif (from_row - to_row == 2 and from_col == to_col and from_row == 6 and 
                  to_piece == '.' and self.board[from_row - 1][from_col] == '.' and 
                  self.is_clear_path(from_square, to_square)):
                return True
            # Capture diagonally
            elif from_row - to_row == 1 and abs(to_col - from_col) == 1 and to_piece != '.' and to_piece.islower():
                return True
        else:
            # Black pawns move downward (to higher row numbers)
            # Move forward one square
            if to_row - from_row == 1 and from_col == to_col and to_piece == '.':
                return True
            # Move forward two squares from starting position (row 1)
            elif (to_row - from_row == 2 and from_col == to_col and from_row == 1 and 
                  to_piece == '.' and self.board[from_row + 1][from_col] == '.' and 
                  self.is_clear_path(from_square, to_square)):
                return True
            # Capture diagonally
            elif to_row - from_row == 1 and abs(to_col - from_col) == 1 and to_piece != '.' and to_piece.isupper():
                return True
        return False

    def is_rook_move_legal(self, from_square, to_square, is_white):
        from_row, from_col = from_square
        to_row, to_col = to_square
        to_piece = self.board[to_row][to_col]

        if (to_row == from_row or to_col == from_col) and self.is_clear_path(from_square, to_square):
            if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                return True
        return False

    def is_bishop_move_legal(self, from_square, to_square, is_white):
        from_row, from_col = from_square
        to_row, to_col = to_square
        to_piece = self.board[to_row][to_col]

        if abs(to_row - from_row) == abs(to_col - from_col) and self.is_clear_path(from_square, to_square):
            if to_piece == '.' or (is_white and to_piece.islower()) or (not is_white and to_piece.isupper()):
                return True
        return False

    def is_queen_move_legal(self, from_square, to_square, is_white):
        return self.is_rook_move_legal(from_square, to_square, is_white) or self.is_bishop_move_legal(from_square, to_square, is_white)

    def is_knight_move_legal(self, from_square, to_square, is_white):
        from_row, from_col = from_square
        to_row, to_col = to_square
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
        from_row, from_col = from_square
        to_row, to_col = to_square
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

        # Find the king's position (use (row, col))
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        # Check if any opposing piece can attack the king
        enemy_is_white = (player == 'black')
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (enemy_is_white and piece.isupper()) or (not enemy_is_white and piece.islower()):
                    if self.is_move_legal((row, col), king_pos):
                        return True
        return False

    def is_checkmate(self, player):
        """Check if the current player is in checkmate."""
        if self.is_in_check(player):
            if not self.get_pieces_with_legal_moves(player):
                return True
        return False

    def does_move_put_player_in_check(self, player, from_square, to_square):
        """Simulate a move on a copy of the board to check if it leaves the player in check."""
        board_copy = copy.deepcopy(self)
        from_row, from_col = from_square
        to_row, to_col = to_square
        
        board_copy.board[to_row][to_col] = board_copy.board[from_row][from_col]
        board_copy.board[from_row][from_col] = '.'
        
        return board_copy.is_in_check(player)

    # --- Move generation ---

    def get_list_of_legal_moves(self, from_square):
        """Get a list of legal moves for the piece at from_square.
           Coordinates are in (row, col) order.
        """
        legal_moves = []
        from_row, from_col = from_square
        piece = self.board[from_row][from_col]

        if piece.isupper():
            player = 'white'
        else:
            player = 'black'
            
        if piece == '.':
            return []

        for row in range(8):
            for col in range(8):
                to_square = (row, col)
                if self.is_move_legal(from_square, to_square) and not self.does_move_put_player_in_check(player, from_square, to_square):
                    legal_moves.append(to_square)

        return legal_moves

    def get_pieces_with_legal_moves(self, player):
        """Get a list of pieces (their positions in (row, col)) that have at least one legal move."""
        legal_pieces = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                pos = (row, col)
                if player == 'white':
                    if piece.isupper() and self.get_list_of_legal_moves(pos):
                        legal_pieces.append(pos)
                elif player == 'black':
                    if piece.islower() and self.get_list_of_legal_moves(pos):
                        legal_pieces.append(pos)
        return legal_pieces

    def is_clear_path(self, from_square, to_square):
        """Check if there is an unobstructed path between two squares.
           Coordinates are in (row, col) order.
        """
        from_row, from_col = from_square
        to_row, to_col = to_square

        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        current_row, current_col = from_row + row_step, from_col + col_step
        while (current_row, current_col) != (to_row, to_col):
            if self.board[current_row][current_col] != '.':
                return False
            current_row += row_step
            current_col += col_step

        return True
