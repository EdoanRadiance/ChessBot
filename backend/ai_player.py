import copy

class AIPlayer:
    def __init__(self, board):
        """Initialize AI player with access to the board."""
        self.board = board

    def evaluate(self, player):
        """Evaluate the board and assign scores based on piece strength and game state."""
        white_score = 0
        black_score = 0

        # Piece values for evaluation
        piece_values = {
            'p': 1, 't': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 1000,  # Black pieces
            'P': 1, 'T': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000   # White pieces
        }

        # Calculate total score for both sides
        for row in self.board.board:
            for piece in row:
                if piece in piece_values:
                    if piece.isupper():
                        white_score += piece_values[piece]
                    else:
                        black_score += piece_values[piece]

        enemy = 'black' if player == 'white' else 'white'

        # Add bonus for check and checkmate
        if self.board.is_in_check(enemy):
            white_score += 5 if player == 'white' else -5
        if self.board.is_checkmate(enemy):
            white_score += 100 if player == 'white' else -100

        for row in self.board.board:
            for piece in row:
                if(piece == 'P' and row == 0):
                    white_score += 7
                if(piece == 'p' and row == 7):
                    black_score += 7

        # Return evaluation based on the player
        return white_score - black_score if player == 'white' else black_score - white_score

    def get_best_move(self, player, depth=4):
        """Find the best possible move using MinMax with Alpha-Beta pruning."""
        print(f"AI thinking for {player} at depth {depth}")

        pieces = self.board.get_pieces_with_legal_moves(player)
        legal_moves = []

        # Ensure AI only considers legal moves
        for piece in pieces:
            moves = self.board.get_list_of_legal_moves(piece)
            for move in moves:
                if self.board.is_move_legal(piece, move):  # Double-check legality
                    legal_moves.append((piece, move))

        print(f"🧠 AI legal moves: {legal_moves}")

        if not legal_moves:
            print(f"No legal moves available for {player}")
            return None

        # Run MinMax algorithm to determine the best move
        best_move, best_score = self.minmax(player, depth, float('-inf'), float('inf'), True)
        print(f"AI chose move: {best_move} with score: {best_score}")

        print("👀 Board before AI move:")
        self.board.draw_board()

        return best_move

    def minmax(self, player, depth, alpha, beta, maximizing):
        """MinMax algorithm with Alpha-Beta pruning."""
        enemy = 'black' if player == 'white' else 'white'

        # Base case: stop when depth reaches 0 or checkmate
        if depth == 0 or self.board.is_checkmate(player):
            return None, self.evaluate(player)

        best_score = float('-inf') if maximizing else float('inf')
        best_move = None

        pieces = self.board.get_pieces_with_legal_moves(player)

        for from_pos in pieces:
            possible_moves = self.board.get_list_of_legal_moves(from_pos)
            for to_pos in possible_moves:
                if not self.board.is_move_legal(from_pos, to_pos):  # Extra safety check
                    print(f"❌ Skipping illegal move: {from_pos} -> {to_pos}")
                    continue

                # Save board state
                temp_board = copy.deepcopy(self.board.board)

                # Make the move
                self.board.move_piece(from_pos, to_pos)

                # Recursively call MinMax
                _, score = self.minmax(enemy, depth - 1, alpha, beta, not maximizing)

                # Restore the board state
                self.board.board = temp_board

                # Update best move and score
                if maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = (from_pos, to_pos)
                    alpha = max(alpha, best_score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (from_pos, to_pos)
                    beta = min(beta, best_score)

                # Alpha-beta pruning
                if beta <= alpha:
                    break
            if beta <= alpha:
                break

        return best_move, best_score
