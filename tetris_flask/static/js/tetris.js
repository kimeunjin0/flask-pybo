const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');

context.scale(20, 20);  // 블록 크기를 20x20으로 설정

let dropCounter = 0;
let dropInterval = 1000;

let lastTime = 0;

let linesCleared = 0;
let level = 1;
let isGameOver = false;
let animationFrameId;

function arenaSweep() {
    let rowCount = 0;
    outer: for (let y = arena.length - 1; y > 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) {
                continue outer;
            }
        }

        const row = arena.splice(y, 1)[0].fill(0);
        arena.unshift(row);
        ++y;

        rowCount++;
        player.score += rowCount * 10;

        linesCleared += 1;
        if (linesCleared >= 3) {  // 레벨업 조건 변경: 3줄
            levelUp();
        }
    }

    if (rowCount === 2) {
        linesCleared += 1;
        player.score += 10;
        showBonusMessage();
        const row = arena.splice(arena.length - 1, 1)[0].fill(0);
        arena.unshift(row);
    }
}

function showBonusMessage() {
    const bonusMessage = document.createElement('div');
    bonusMessage.style.position = 'fixed';
    bonusMessage.style.top = '10%';
    bonusMessage.style.left = '50%';
    bonusMessage.style.transform = 'translate(-50%, -50%)';
    bonusMessage.style.fontSize = '24px';
    bonusMessage.style.color = '#fff';
    bonusMessage.style.backgroundColor = '#000';
    bonusMessage.style.padding = '10px';
    bonusMessage.style.border = '2px solid #fff';
    bonusMessage.innerText = `Bonus Line!`;
    document.body.appendChild(bonusMessage);

    setTimeout(() => {
        document.body.removeChild(bonusMessage);
    }, 1000);
}

function collide(arena, player) {
    const m = player.matrix;
    const o = player.pos;
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
               (arena[y + o.y] &&
                arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

function createPiece(type) {
    if (type === 'T') {
        return [
            [0,0,0],
            [1,1,1],
            [0,1,0],
        ];
    } else if (type === 'O') {
        return [
            [2,2],
            [2,2],
        ];
    } else if (type === 'L') {
        return [
            [0,3,0],
            [0,3,0],
            [0,3,3],
        ];
    } else if (type === 'J') {
        return [
            [0,4,0],
            [0,4,0],
            [4,4,0],
        ];
    } else if (type === 'I') {
        return [
            [0,5,0,0],
            [0,5,0,0],
            [0,5,0,0],
            [0,5,0,0],
        ];
    } else if (type === 'S') {
        return [
            [0,6,6],
            [6,6,0],
            [0,0,0],
        ];
    } else if (type === 'Z') {
        return [
            [7,7,0],
            [0,7,7],
            [0,0,0],
        ];
    }
}

function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x,
                                 y + offset.y,
                                 1, 1);  // 블록 크기를 1x1으로 설정
            }
        });
    });
}

function draw() {
    context.fillStyle = '#000';
    context.fillRect(0, 0, canvas.width, canvas.height);

    drawMatrix(arena, {x: 0, y: 0});
    drawMatrix(player.matrix, player.pos);
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [
                matrix[x][y],
                matrix[y][x],
            ] = [
                matrix[y][x],
                matrix[x][y],
            ];
        }
    }

    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

function playerDrop() {
    player.pos.y++;
    if (collide(arena, player)) {
        player.pos.y--;
        merge(arena, player);
        playerReset();
        arenaSweep();
        updateScore();
        if (collide(arena, player)) {
            gameOver();
        }
    }
    dropCounter = 0;
}

function playerMove(offset) {
    player.pos.x += offset;
    if (collide(arena, player)) {
        player.pos.x -= offset;
    }
}

function playerReset() {
    const pieces = 'ILJOTSZ';
    player.matrix = createPiece(pieces[pieces.length * Math.random() | 0]);
    player.pos.y = 0;
    player.pos.x = (arena[0].length / 2 | 0) -
                   (player.matrix[0].length / 2 | 0);
    if (collide(arena, player)) {
        gameOver();
    }
}

function playerRotate(dir) {
    const pos = player.pos.x;
    let offset = 1;
    rotate(player.matrix, dir);
    while (collide(arena, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
            rotate(player.matrix, -dir);
            player.pos.x = pos;
            return;
        }
    }
}

function update(time = 0) {
    if (isGameOver) {
        return;
    }

    const deltaTime = time - lastTime;
    lastTime = time;

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }

    draw();
    animationFrameId = requestAnimationFrame(update);
}

function updateScore() {
    document.getElementById('score').innerText = player.score;
    document.getElementById('level').innerText = level;
}

function levelUp() {
    linesCleared = 0;
    level += 1;
    dropInterval *= 0.9;  // 속도를 10% 증가시킵니다.
    showLevelUpMessage();
}

function showLevelUpMessage() {
    const levelUpMessage = document.createElement('div');
    levelUpMessage.style.position = 'fixed';
    levelUpMessage.style.top = '10%';
    levelUpMessage.style.left = '50%';
    levelUpMessage.style.transform = 'translate(-50%, -50%)';
    levelUpMessage.style.fontSize = '24px';
    levelUpMessage.style.color = '#fff';
    levelUpMessage.style.backgroundColor = '#000';
    levelUpMessage.style.padding = '10px';
    levelUpMessage.style.border = '2px solid #fff';
    levelUpMessage.innerText = `Level ${level}`;
    document.body.appendChild(levelUpMessage);

    setTimeout(() => {
        document.body.removeChild(levelUpMessage);
    }, 1000);
}

function gameOver() {
    isGameOver = true;
    cancelAnimationFrame(animationFrameId);
    showGameOverMessage();
}

function showGameOverMessage() {
    const gameOverMessage = document.createElement('div');
    gameOverMessage.id = 'gameOverMessage'; // ID 추가
    gameOverMessage.style.position = 'fixed';
    gameOverMessage.style.top = '50%';
    gameOverMessage.style.left = '50%';
    gameOverMessage.style.transform = 'translate(-50%, -50%)';
    gameOverMessage.style.fontSize = '48px';
    gameOverMessage.style.color = '#fff';
    gameOverMessage.style.backgroundColor = '#000';
    gameOverMessage.style.padding = '20px';
    gameOverMessage.style.border = '2px solid #fff';
    gameOverMessage.innerText = `Game Over`;

    document.body.appendChild(gameOverMessage);
}

function removeGameOverMessage() {
    const gameOverElem = document.getElementById('gameOverMessage');
    if (gameOverElem) {
        gameOverElem.remove();
    }
}

function showStartButton() {
    const startButton = document.createElement('button');
    startButton.id = 'startButton'; // ID 추가
    startButton.innerText = 'Start';
    startButton.style.position = 'fixed';
    startButton.style.top = '50%';
    startButton.style.left = '50%';
    startButton.style.transform = 'translate(-50%, -50%)';
    startButton.style.fontSize = '24px';
    startButton.style.padding = '10px';
    startButton.style.cursor = 'pointer';
    startButton.onclick = () => {
        removeGameOverMessage();
        const startElem = document.getElementById('startButton');
        if (startElem) {
            startElem.remove();
        }
        init();
    };
    document.body.appendChild(startButton);
}

function init() {
    removeGameOverMessage();
    const startElem = document.getElementById('startButton');
    if (startElem) {
        startElem.remove();
    }
    arena.forEach(row => row.fill(0));
    player.score = 0;
    linesCleared = 0;
    level = 1;
    dropInterval = 1000;
    isGameOver = false;
    playerReset();
    updateScore();
    lastTime = 0;
    dropCounter = 0;
    animationFrameId = requestAnimationFrame(update);
}

const colors = [
    null,
    '#FF0D72',
    '#0DC2FF',
    '#0DFF72',
    '#F538FF',
    '#FF8E0D',
    '#FFE138',
    '#3877FF',
];

const arena = createMatrix(12, 20);

const player = {
    pos: {x: 0, y: 0},
    matrix: null,
    score: 0,
};

document.addEventListener('keydown', event => {
    if (event.keyCode === 37) { // 왼쪽 방향키
        playerMove(-1);
    } else if (event.keyCode === 39) { // 오른쪽 방향키
        playerMove(1);
    } else if (event.keyCode === 40) { // 아래 방향키
        playerDrop();
    } else if (event.keyCode === 81) { // Q 키
        playerRotate(-1);
    } else if (event.keyCode === 38) { // 위 방향키
        playerRotate(1);
    }
});

// 처음에 Start 버튼을 표시합니다.
showStartButton();
