// Game constants
const CELL_SIZE = 20;
const GRID_WIDTH = 28;
const GRID_HEIGHT = 31;
const PACMAN_SPEED = 2;
const GHOST_SPEED = 1.5;

// Game variables
let canvas, ctx;
let pacman = {
    x: 14 * CELL_SIZE,
    y: 23 * CELL_SIZE,
    direction: 0, // 0: right, 1: down, 2: left, 3: up
    mouthOpen: 0,
    mouthSpeed: 0.15,
};
let ghosts = [];
let dots = [];
let score = 0;
let lives = 3;
let gameLoop;
let isGameRunning = false;
let gameState = {
    score: 0,
    lives: 3,
    dots: [],
    pacman: { x: 14 * CELL_SIZE, y: 23 * CELL_SIZE, direction: 0 },
    ghosts: [],
};

// Initialize the game
function init() {
    canvas = document.getElementById("gameCanvas");
    ctx = canvas.getContext("2d");

    // Set canvas size
    canvas.width = GRID_WIDTH * CELL_SIZE;
    canvas.height = GRID_HEIGHT * CELL_SIZE;

    // Initialize dots
    initDots();

    // Initialize ghosts
    initGhosts();

    // Add event listeners for menu buttons
    document
        .getElementById("newGameBtn")
        .addEventListener("click", startNewGame);
    document
        .getElementById("continueBtn")
        .addEventListener("click", continueGame);

    // Start game loop
    startGame();

    // Add keyboard controls
    document.addEventListener("keydown", handleKeyPress);
}

// Save current game state
function saveGameState() {
    gameState = {
        score: score,
        lives: lives,
        dots: [...dots],
        pacman: { ...pacman },
        ghosts: ghosts.map((ghost) => ({ ...ghost })),
    };
}

// Load saved game state
function loadGameState() {
    score = gameState.score;
    lives = gameState.lives;
    dots = [...gameState.dots];
    pacman = { ...gameState.pacman };
    ghosts = gameState.ghosts.map((ghost) => ({ ...ghost }));

    // Update UI
    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
}

// Start the game
function startGame() {
    if (!isGameRunning) {
        isGameRunning = true;
        gameLoop = setInterval(update, 1000 / 60);
    }
}

// Show menu
function showMenu() {
    document.getElementById("menu").classList.remove("hidden");
    saveGameState();
}

// Hide menu
function hideMenu() {
    document.getElementById("menu").classList.add("hidden");
}

// Start new game
function startNewGame() {
    hideMenu();
    resetGame();
    startGame();
}

// Continue game
function continueGame() {
    hideMenu();
    loadGameState();
    startGame();
}

// Exit the game
function exitGame() {
    if (isGameRunning) {
        isGameRunning = false;
        clearInterval(gameLoop);
        showMenu();
    }
}

// Initialize dots
function initDots() {
    dots = [];
    for (let y = 0; y < GRID_HEIGHT; y++) {
        for (let x = 0; x < GRID_WIDTH; x++) {
            // Skip dots in the ghost house and walls
            if (!isWall(x, y)) {
                dots.push({ x, y });
            }
        }
    }
}

// Initialize ghosts
function initGhosts() {
    ghosts = [
        { x: 13 * CELL_SIZE, y: 11 * CELL_SIZE, direction: 0, color: "red" },
        { x: 14 * CELL_SIZE, y: 11 * CELL_SIZE, direction: 0, color: "pink" },
        { x: 13 * CELL_SIZE, y: 12 * CELL_SIZE, direction: 0, color: "cyan" },
        { x: 14 * CELL_SIZE, y: 12 * CELL_SIZE, direction: 0, color: "orange" },
    ];
}

// Check if position is a wall
function isWall(x, y) {
    // Simple wall layout - you can make this more complex
    return (
        x === 0 ||
        x === GRID_WIDTH - 1 ||
        y === 0 ||
        y === GRID_HEIGHT - 1 ||
        (x > 10 && x < 17 && y > 10 && y < 15)
    );
}

// Handle keyboard input
function handleKeyPress(e) {
    switch (e.key) {
        case "ArrowRight":
            if (isGameRunning) pacman.direction = 0;
            break;
        case "ArrowDown":
            if (isGameRunning) pacman.direction = 1;
            break;
        case "ArrowLeft":
            if (isGameRunning) pacman.direction = 2;
            break;
        case "ArrowUp":
            if (isGameRunning) pacman.direction = 3;
            break;
        case "Escape":
            if (isGameRunning) {
                exitGame();
            } else {
                continueGame();
            }
            break;
    }
}

// Update game state
function update() {
    // Move Pacman
    movePacman();

    // Move ghosts
    moveGhosts();

    // Check collisions
    checkCollisions();

    // Draw everything
    draw();
}

// Move Pacman
function movePacman() {
    let newX = pacman.x;
    let newY = pacman.y;

    switch (pacman.direction) {
        case 0: // right
            newX += PACMAN_SPEED;
            break;
        case 1: // down
            newY += PACMAN_SPEED;
            break;
        case 2: // left
            newX -= PACMAN_SPEED;
            break;
        case 3: // up
            newY -= PACMAN_SPEED;
            break;
    }

    // Check if new position is valid
    const gridX = Math.floor(newX / CELL_SIZE);
    const gridY = Math.floor(newY / CELL_SIZE);

    if (!isWall(gridX, gridY)) {
        pacman.x = newX;
        pacman.y = newY;
    }

    // Update mouth animation
    pacman.mouthOpen += pacman.mouthSpeed;
    if (pacman.mouthOpen > 0.5 || pacman.mouthOpen < 0) {
        pacman.mouthSpeed = -pacman.mouthSpeed;
    }
}

// Move ghosts
function moveGhosts() {
    ghosts.forEach((ghost) => {
        // Simple random movement
        if (Math.random() < 0.02) {
            ghost.direction = Math.floor(Math.random() * 4);
        }

        let newX = ghost.x;
        let newY = ghost.y;

        switch (ghost.direction) {
            case 0: // right
                newX += GHOST_SPEED;
                break;
            case 1: // down
                newY += GHOST_SPEED;
                break;
            case 2: // left
                newX -= GHOST_SPEED;
                break;
            case 3: // up
                newY -= GHOST_SPEED;
                break;
        }

        // Check if new position is valid
        const gridX = Math.floor(newX / CELL_SIZE);
        const gridY = Math.floor(newY / CELL_SIZE);

        if (!isWall(gridX, gridY)) {
            ghost.x = newX;
            ghost.y = newY;
        } else {
            // Change direction if hit wall
            ghost.direction = Math.floor(Math.random() * 4);
        }
    });
}

// Check collisions
function checkCollisions() {
    // Check dot collisions
    const pacmanGridX = Math.floor(pacman.x / CELL_SIZE);
    const pacmanGridY = Math.floor(pacman.y / CELL_SIZE);

    dots = dots.filter((dot) => {
        if (dot.x === pacmanGridX && dot.y === pacmanGridY) {
            score += 10;
            document.getElementById("score").textContent = score;
            return false;
        }
        return true;
    });

    // Check ghost collisions
    ghosts.forEach((ghost) => {
        const distance = Math.sqrt(
            Math.pow(pacman.x - ghost.x, 2) + Math.pow(pacman.y - ghost.y, 2)
        );

        if (distance < CELL_SIZE) {
            lives--;
            document.getElementById("lives").textContent = lives;

            if (lives <= 0) {
                gameOver();
            } else {
                resetPositions();
            }
        }
    });

    // Check win condition
    if (dots.length === 0) {
        alert("You win!");
        resetGame();
    }
}

// Reset positions after collision
function resetPositions() {
    pacman.x = 14 * CELL_SIZE;
    pacman.y = 23 * CELL_SIZE;
    initGhosts();
}

// Reset game
function resetGame() {
    score = 0;
    lives = 3;
    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
    resetPositions();
    initDots();
}

// Game over
function gameOver() {
    clearInterval(gameLoop);
    isGameRunning = false;
    alert("Game Over!");
    resetGame();
    startGame();
}

// Draw everything
function draw() {
    // Clear canvas
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw walls
    ctx.fillStyle = "#2121de";
    for (let y = 0; y < GRID_HEIGHT; y++) {
        for (let x = 0; x < GRID_WIDTH; x++) {
            if (isWall(x, y)) {
                ctx.fillRect(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                );
            }
        }
    }

    // Draw dots
    ctx.fillStyle = "#fff";
    dots.forEach((dot) => {
        ctx.beginPath();
        ctx.arc(
            dot.x * CELL_SIZE + CELL_SIZE / 2,
            dot.y * CELL_SIZE + CELL_SIZE / 2,
            2,
            0,
            Math.PI * 2
        );
        ctx.fill();
    });

    // Draw Pacman
    ctx.fillStyle = "#ffff00";
    ctx.beginPath();
    ctx.arc(
        pacman.x + CELL_SIZE / 2,
        pacman.y + CELL_SIZE / 2,
        CELL_SIZE / 2,
        (0.25 + pacman.mouthOpen) * Math.PI + (pacman.direction * Math.PI) / 2,
        (1.75 - pacman.mouthOpen) * Math.PI + (pacman.direction * Math.PI) / 2
    );
    ctx.lineTo(pacman.x + CELL_SIZE / 2, pacman.y + CELL_SIZE / 2);
    ctx.fill();

    // Draw ghosts
    ghosts.forEach((ghost) => {
        ctx.fillStyle = ghost.color;
        ctx.beginPath();
        ctx.arc(
            ghost.x + CELL_SIZE / 2,
            ghost.y + CELL_SIZE / 2,
            CELL_SIZE / 2,
            Math.PI,
            0
        );
        ctx.lineTo(ghost.x + CELL_SIZE, ghost.y + CELL_SIZE);
        ctx.lineTo(ghost.x, ghost.y + CELL_SIZE);
        ctx.fill();
    });
}

// Start the game when the page loads
window.onload = init;
