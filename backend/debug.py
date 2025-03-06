from chess_board import ChessBoard
from ai_player import AIPlayer

# Setup a fresh chessboard
board = ChessBoard()
ai = AIPlayer(board)

# Confirm the starting board state
print("🔍 Starting board state:")
board.draw_board()

# Check which pieces AI thinks belong to 'black'
print("\n🧠 AI identifying Black's pieces:")
black_pieces = board.get_pieces_with_legal_moves('black')
piece_names = {
    'P': 'Pawn', 'p': 'Pawn',
    'R': 'Rook', 'r': 'Rook',
    'T': 'Knight', 't': 'Knight',
    'B': 'Bishop', 'b': 'Bishop',
    'Q': 'Queen', 'q': 'Queen',
    'K': 'King', 'k': 'King'
  }

if not black_pieces:
    print("❌ AI found NO pieces for Black!")
else:
    for pos in black_pieces:
        col, row = pos
        piece_symbol = board.board[row][col]
        piece_name = piece_names.get(piece_symbol, 'Unknown Piece')
        print(f"🧩 AI sees a Black {piece_name} at {pos}")


# Check the AI's legal moves
print("\n🔎 AI's legal moves for Black:")
legal_moves = [(piece, move) for piece in black_pieces for move in board.get_list_of_legal_moves(piece)]

if not legal_moves:
    print("❌ AI found NO legal moves for Black!")
else:
    for piece, move in legal_moves:
        print(f"➡️ From {piece} to {move}")

# Optional: Test AI's best move
print("\n💡 AI's best move suggestion:")
best_move = ai.get_best_move('black', depth=1)  # Test with shallow depth for quick results
print(f"🏁 AI's best move: {best_move}")
