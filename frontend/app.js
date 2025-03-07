const boardElement = document.getElementById('chessboard');
const moveLogElement = document.getElementById('move-log');
let selectedSquare = null;

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
            square.textContent = piece !== '.' ? piece : '';

            square.addEventListener('click', () => selectSquare(rowIndex, colIndex));
            boardElement.appendChild(square);
        });
    });
}

function selectSquare(row, col) {
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
            fetchBoard();
            addToLog(`👤 Player move: ${formatMove(from, to)}`);
            drawMove(from, to);
        } else {
            addToLog(`❌ Invalid Move`);
            alert(data.message);
        }
    } catch (error) {
        console.error('Error making move:', error);
    }
}

function drawMove(from, to) {
    const piece = boardElement.children[from[0] * 8 + from[1]].textContent;
    boardElement.children[to[0] * 8 + to[1]].textContent = piece;
    boardElement.children[from[0] * 8 + from[1]].textContent = '';
}

function addToLog(message) {
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    moveLogElement.appendChild(logEntry);
}

function formatMove(from, to) {
    const cols = 'abcdefgh';
    return `${cols[from[1]]}${8 - from[0]} ➡️ ${cols[to[1]]}${8 - to[0]}`;
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
