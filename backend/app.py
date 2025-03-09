import time
from flask import Flask, jsonify, request, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Serve the main HTML file for the frontend
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# Serve static files (like JS, CSS, images) from the frontend directory
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Attempt to import the chess board and AI modules
try:
    from chess_board import ChessBoard
    from ai_player import AIPlayer
    print("[INFO] Board and AI imported successfully!")
except Exception as e:
    print(f"[ERROR] Error importing board or AI: {e}")

# Create instances of the chess board and AI player
try:
    board = ChessBoard()
    ai = AIPlayer(board)
    print("[INFO] Board and AI instances created successfully!")
except Exception as e:
    print(f"[ERROR] Error creating board or AI instances: {e}")

# Simple route to confirm Flask is running
@app.route('/home')
def home():
    return "Flask is working!"

# Endpoint to get the current state of the chess board
@app.route('/state', methods=['GET'])
def get_state():
    try:
        board_state = board.get_state()  # Get current board state
        print("[INFO] Board state fetched successfully!")
        return jsonify({'board': board_state})
    except Exception as e:
        print(f"[ERROR] Error fetching board state: {e}")
        return jsonify({'error': str(e)}), 500

# Endpoint to handle a player's move
@app.route('/move', methods=['POST'])
def make_move():
    try:
        data = request.json
        # Expecting coordinates in (row, col) order
        from_pos = tuple(data['from'])
        to_pos = tuple(data['to'])
        
        print(f"[INFO] Player move received: {from_pos} -> {to_pos}")

        # Validate the player's move without swapping indices,
        # since our board now uses (row, col) order consistently.
        if not board.is_move_legal(from_pos, to_pos):
            print("[ERROR] Invalid player move attempted")
            return jsonify({'status': 'error', 'message': 'Invalid move'})

        # Execute the player's move
        board.move_piece(from_pos, to_pos)
        print(f"[INFO] Moving piece: from {from_pos} to {to_pos}")
        print(f"[INFO] ✅ Board after player move:\n{board.get_state()}")

        # Return the updated board state
        return jsonify({'status': 'success', 
                        'board': board.get_state(),
                        'message': 'Player move complete'})

    except Exception as e:
        print(f"[ERROR] 💥 Error processing move: {e}")
        return jsonify({'status': 'error',
                         'message': str(e)}), 500

# Endpoint to handle the AI's move
@app.route('/ai-move', methods=['POST'])
def ai_move():
    try:
        print("[INFO] 🤖 AI is thinking...")

        # AI determines its best move; expected as (from_pos, to_pos) in (row, col) order
        best_move = ai.get_best_move('black', depth=4)
        if best_move:
            from_pos, to_pos = best_move
            print(f"[INFO] 🤖 AI move: {from_pos} -> {to_pos}")

            # Validate and execute the AI's move
            if board.is_move_legal(from_pos, to_pos):
                time.sleep(1)  # Optional delay for visual effect
                board.move_piece(from_pos, to_pos)
                print(f"[INFO] ✅ Board after AI move:\n{board.get_state()}")
                print(f"[INFO] AI move completed: {from_pos} -> {to_pos}")
            else:
                print(f"[ERROR] 🚨 AI attempted invalid move: {from_pos} -> {to_pos}")

            # Return the updated board state along with the AI move
            return jsonify({
                'status': 'success', 
                'board': board.get_state(), 
                'message': 'AI move complete', 
                'move': {'from': from_pos, 'to': to_pos}
            })
        else:
            return jsonify({'status': 'error', 'message': 'No legal moves available'}), 400

    except Exception as e:
        print(f"[ERROR] 💥 Error processing AI move: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Endpoint to reset the board to its starting position
@app.route('/reset', methods=['POST'])
def reset_board():
    try:
        board.setup_default()  # Reset the board
        print("[INFO] Board reset to default setup")
        return jsonify({'status': 'success', 'board': board.get_state()})
    except Exception as e:
        print(f"[ERROR] Error resetting board: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    print("[INFO] Starting Flask server...")
    app.run(debug=True)
