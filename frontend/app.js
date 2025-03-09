const boardElement = document.getElementById('chessboard');
const moveLogElement = document.getElementById('move-log');
let selectedSquare = null;
let turn = 'player'

const pieceImages = {
    'r': 'assets/pieces/rook-b.svg',
    't': 'assets/pieces/knight-b.svg',
    'b': 'assets/pieces/bishop-b.svg',
    'q': 'assets/pieces/queen-b.svg',
    'k': 'assets/pieces/king-b.svg',
    'p': 'assets/pieces/pawn-b.svg',
    'R': 'assets/pieces/rook-w.svg',
    'T': 'assets/pieces/knight-w.svg',
    'B': 'assets/pieces/bishop-w.svg',
    'Q': 'assets/pieces/queen-w.svg',
    'K': 'assets/pieces/king-w.svg',
    'P': 'assets/pieces/pawn-w.svg',
    '.': 'assets/pieces/empty.png'  // You may leave empty squares blank or use a placeholder.
  };
  



async function fetchBoard() {
    try {
        const response = await fetch('/state');
        const data = await response.json();
        drawBoard(data.board);
    } catch (error) {
        console.error('Error fetching board:', error);
    }
}

function drawBoard(board) {
    boardElement.innerHTML = '';
  
    board.forEach((row, rowIndex) => {
      row.forEach((piece, colIndex) => {
        const square = document.createElement('div');
        square.className = `square ${(rowIndex + colIndex) % 2 === 0 ? 'light' : 'dark'}`;
  
        if (piece !== '.') {
          const img = document.createElement('img');
          img.src = pieceImages[piece] || '';
          img.alt = piece;
          square.appendChild(img);
        }
  
        square.addEventListener('click', () => selectSquare(rowIndex, colIndex));
        boardElement.appendChild(square);
      });
    });
  }
  

function selectSquare(row, col) {
    if(turn != 'player') {
        addToLog(`❌ Its not your turn.`);
        return;
    }
        
    if (selectedSquare) {
        makeMove(selectedSquare, [row, col]);
        selectedSquare = null;
    } else {
        selectedSquare = [row, col];
    }
}

async function makeMove(from, to) {
    addToLog(`✅ Processing move`);
    // Show player’s move right away

    try {
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from, to })
        });

        const data = await response.json();
        if (data.status === 'success') { 
            
            drawMove(from, to);
            addToLog(`👤 Player move: ${formatMove(from, to)}`);
            
            turn = 'ai';
            fetchAiMove();
        } else {
            addToLog(`❌ Invalid Move`);
            alert(data.message);
            
        }
    } catch (error) {
        console.error('Error making move:', error);
    }
}

async function fetchAiMove(){
    try{
        const response = await fetch('/ai-move', {
            method: 'POST', })
        const data = await response.json();
        const {from, to } = data.move
        
        if(data.status === 'success') {
            addToLog(`🤖 AI move: ${formatAIMove(from, to)}`);
            
            fetchBoard();
            turn = 'player'
        } else {
            alert(data.message)

        }

    

    } catch(error){console.error('💥 Error making AI move:', error);}
}





function drawMove(from, to) {
    const fromIndex = from[0] * 8 + from[1];
    const toIndex = to[0] * 8 + to[1];
  
    const fromSquare = boardElement.children[fromIndex];
    const toSquare = boardElement.children[toIndex];
  
    
    const pieceImg = fromSquare.querySelector('img');
    if (pieceImg) {
      
      fromSquare.removeChild(pieceImg);
      
      
      toSquare.innerHTML = '';
      
      toSquare.appendChild(pieceImg);
    }
  }
  

function addToLog(message) {
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    moveLogElement.appendChild(logEntry);
    moveLogElement.scrollTop =  moveLogElement.scrollHeight;
}

function formatMove(from, to) {
    const cols = 'abcdefgh';
    

    return `${cols[from[1]]}${8 - from[0]} ➡️ ${cols[to[1]]}${8 - to[0]}`;
}
function formatAIMove(from, to) {
    const cols = 'abcdefgh';
    

    return `${cols[from[0]]}${8 - from[1]} ➡️ ${cols[to[0]]}${8 - to[1]}`;
}

async function resetBoard() {
    try {
        const response = await fetch('/reset', { method: 'POST' });
        const data = await response.json();
        if (data.status === 'success') {
            fetchBoard();
            moveLogElement.innerHTML = ''; // Clear log on reset
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error resetting board:', error);
    }
}

fetchBoard();
