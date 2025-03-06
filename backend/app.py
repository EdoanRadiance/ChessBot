from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Test importing the board and AI
try:
    from chess_board import ChessBoard
    from ai_player import AIPlayer
    print("Board and AI imported successfully!")
except Exception as e:
    print(f"Error importing board or AI: {e}")

# Create instances of board and AI
try:
    board = ChessBoard()
    ai = AIPlayer(board)
    print("Board and AI instances created successfully!")
except Exception as e:
    print(f"Error creating board or AI instances: {e}")

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/state', methods=['GET'])
def get_state():
    try:
        board_state = board.get_state()
        print("Board state fetched successfully!")
        return jsonify({'board': board_state})
    except Exception as e:
        print(f"Error fetching board state: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/move', methods=['POST'])
def make_move():
    try:
        data = request.json
        from_pos = tuple(data['from'])
        to_pos = tuple(data['to'])

        print(f"Player move received: {from_pos} -> {to_pos}")

        # Human move
        if board.move_piece((from_pos[1], from_pos[0]), (to_pos[1], to_pos[0])):  # (row, col) — FIXED

            print(f"✅ Board after player move:\n{board.get_state()}")

            # AI responds
            ai_move = ai.get_best_move('black', depth=4)
            if ai_move:
                piece, move = ai_move
                print(f"🤖 AI move: {piece} -> {move}")

                if board.is_move_legal(piece, move):
                    board.move_piece(piece, move)
                    print(f"✅ Board after ai move:\n{board.get_state()}")
                else:
                    print(f"🚨 AI attempted invalid move: {piece} -> {move}")

            return jsonify({'status': 'success', 'board': board.get_state()})

        print("❌ Invalid player move attempted")
        return jsonify({'status': 'error', 'message': 'Invalid move'})

    except Exception as e:
        print(f"💥 Error processing move: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500





@app.route('/reset', methods=['POST'])
def reset_board():
    try:
        board.setup_default()  # Reset the board to its starting state
        print("Board reset to default setup")
        return jsonify({'status': 'success', 'board': board.get_state()})
    except Exception as e:
        print(f"Error resetting board: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
