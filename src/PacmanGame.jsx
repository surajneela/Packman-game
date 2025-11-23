import React, { useEffect, useRef, useState } from 'react';
import './PacmanGame.css';

// Game constants
const CELL_SIZE = 20;
const GRID_WIDTH = 28;
const GRID_HEIGHT = 31;
const PACMAN_SPEED = 2;
const GHOST_SPEED = 1.5;

// Check if position is a wall
function isWall(x, y) {
    // Outer walls
    if (x === 0 || x === GRID_WIDTH - 1 || y === 0 || y === GRID_HEIGHT - 1) {
        return true;
    }

    // Ghost house (center)
    if (x > 10 && x < 17 && y > 10 && y < 15) {
        return true;
    }

    // S (Hollow-ish)
    // Top part (Left vertical, open right)
    if (y === 3 && x >= 2 && x <= 5) return true; // Top
    if (x === 2 && y >= 3 && y <= 6) return true; // Left Top
    if (y === 6 && x >= 2 && x <= 5) return true; // Mid

    // Bottom part (Right vertical, open left)
    if (x === 5 && y >= 6 && y <= 9) return true; // Right Bottom
    if (y === 9 && x >= 2 && x <= 5) return true; // Bottom

    // U (Hollow cup)
    if (x === 7 && y >= 3 && y <= 9) return true;
    if (x === 10 && y >= 3 && y <= 9) return true;
    if (y === 9 && x >= 7 && x <= 10) return true;

    // R (Hollow loop with leg)
    if (x === 12 && y >= 3 && y <= 9) return true; // Left spine
    if (y === 3 && x >= 12 && x <= 15) return true; // Top
    if (x === 15 && y >= 3 && y <= 6) return true; // Right loop
    if (y === 6 && x >= 14 && x <= 15) return true; // Mid (gap at 13)
    if (x === 15 && y >= 6 && y <= 9) return true; // Leg

    // A (Hollow arch)
    if (x === 17 && y >= 3 && y <= 9) return true; // Left leg
    if (x === 20 && y >= 3 && y <= 9) return true; // Right leg
    if (y === 3 && x >= 17 && x <= 20) return true; // Top
    if (y === 6 && x >= 19 && x <= 20) return true; // Crossbar (gap at 18)
    if (y === 6 && x === 17) return true; // Crossbar left bit

    // J (Hollow hook)
    if (x === 24 && y >= 3 && y <= 9) return true; // Right spine
    if (y === 9 && x >= 22 && x <= 24) return true; // Bottom
    if (x === 22 && y >= 7 && y <= 9) return true; // Hook tip

    // Bottom filler to keep game interesting
    if (y === 20 && x >= 4 && x <= 23) return true;
    if (x === 13 && y >= 20 && y <= 25) return true;
    if (x === 14 && y >= 20 && y <= 25) return true;

    if (y === 25 && x >= 2 && x <= 8) return true;
    if (y === 25 && x >= 19 && x <= 25) return true;

    return false;
}

const PacmanGame = () => {
    const canvasRef = useRef(null);
    const [score, setScore] = useState(0);
    const [lives, setLives] = useState(3);
    const [isMenuVisible, setIsMenuVisible] = useState(true);
    const [isGameRunning, setIsGameRunning] = useState(false);

    // Game state refs (mutable, no re-renders)
    const gameState = useRef({
        pacman: {
            x: 14 * CELL_SIZE,
            y: 17 * CELL_SIZE,
            direction: 0,
            mouthOpen: 0,
            mouthSpeed: 0.15,
        },
        ghosts: [],
        dots: [],
        score: 0,
        lives: 3,
    });

    const gameLoopRef = useRef(null);

    const initDots = () => {
        const dots = [];
        for (let y = 0; y < GRID_HEIGHT; y++) {
            for (let x = 0; x < GRID_WIDTH; x++) {
                if (!isWall(x, y)) {
                    dots.push({ x, y });
                }
            }
        }
        return dots;
    };

    const initGhosts = () => {
        return [
            { x: 13 * CELL_SIZE, y: 11 * CELL_SIZE, direction: 0, color: "red" },
            { x: 14 * CELL_SIZE, y: 11 * CELL_SIZE, direction: 0, color: "pink" },
            { x: 13 * CELL_SIZE, y: 12 * CELL_SIZE, direction: 0, color: "cyan" },
            { x: 14 * CELL_SIZE, y: 12 * CELL_SIZE, direction: 0, color: "orange" },
        ];
    };

    const resetGame = () => {
        gameState.current.score = 0;
        gameState.current.lives = 3;
        gameState.current.dots = initDots();
        resetPositions();
        setScore(0);
        setLives(3);
    };

    const resetPositions = () => {
        gameState.current.pacman = {
            x: 14 * CELL_SIZE,
            y: 17 * CELL_SIZE,
            direction: 0,
            mouthOpen: 0,
            mouthSpeed: 0.15,
        };
        gameState.current.ghosts = initGhosts();
    };

    const startNewGame = () => {
        setIsMenuVisible(false);
        resetGame();
        setIsGameRunning(true);
    };

    const continueGame = () => {
        setIsMenuVisible(false);
        setIsGameRunning(true);
    };

    const gameOver = () => {
        setIsGameRunning(false);
        alert("Game Over!");
        resetGame();
        setIsMenuVisible(true);
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        canvas.width = GRID_WIDTH * CELL_SIZE;
        canvas.height = GRID_HEIGHT * CELL_SIZE;

        // Initial setup
        if (gameState.current.dots.length === 0) {
            gameState.current.dots = initDots();
            gameState.current.ghosts = initGhosts();
        }

        const handleKeyPress = (e) => {
            if (!isGameRunning) return;
            switch (e.key) {
                case "ArrowRight": gameState.current.pacman.direction = 0; break;
                case "ArrowDown": gameState.current.pacman.direction = 1; break;
                case "ArrowLeft": gameState.current.pacman.direction = 2; break;
                case "ArrowUp": gameState.current.pacman.direction = 3; break;
                case "Escape":
                    setIsGameRunning(false);
                    setIsMenuVisible(true);
                    break;
            }
        };

        window.addEventListener("keydown", handleKeyPress);

        const update = () => {
            if (!isGameRunning) return;

            const { pacman, ghosts } = gameState.current;

            // Move Pacman
            let newX = pacman.x;
            let newY = pacman.y;

            switch (pacman.direction) {
                case 0: newX += PACMAN_SPEED; break;
                case 1: newY += PACMAN_SPEED; break;
                case 2: newX -= PACMAN_SPEED; break;
                case 3: newY -= PACMAN_SPEED; break;
            }

            const gridX = Math.floor(newX / CELL_SIZE);
            const gridY = Math.floor(newY / CELL_SIZE);

            if (!isWall(gridX, gridY)) {
                pacman.x = newX;
                pacman.y = newY;
            }

            pacman.mouthOpen += pacman.mouthSpeed;
            if (pacman.mouthOpen > 0.5 || pacman.mouthOpen < 0) {
                pacman.mouthSpeed = -pacman.mouthSpeed;
            }

            // Move Ghosts
            ghosts.forEach((ghost) => {
                if (Math.random() < 0.02) {
                    ghost.direction = Math.floor(Math.random() * 4);
                }

                let gNewX = ghost.x;
                let gNewY = ghost.y;

                switch (ghost.direction) {
                    case 0: gNewX += GHOST_SPEED; break;
                    case 1: gNewY += GHOST_SPEED; break;
                    case 2: gNewX -= GHOST_SPEED; break;
                    case 3: gNewY -= GHOST_SPEED; break;
                }

                const gGridX = Math.floor(gNewX / CELL_SIZE);
                const gGridY = Math.floor(gNewY / CELL_SIZE);

                if (!isWall(gGridX, gGridY)) {
                    ghost.x = gNewX;
                    ghost.y = gNewY;
                } else {
                    ghost.direction = Math.floor(Math.random() * 4);
                }
            });

            // Check Collisions
            // Dots
            const pGridX = Math.floor(pacman.x / CELL_SIZE);
            const pGridY = Math.floor(pacman.y / CELL_SIZE);

            const initialDotsCount = gameState.current.dots.length;
            gameState.current.dots = gameState.current.dots.filter(dot => {
                if (dot.x === pGridX && dot.y === pGridY) {
                    gameState.current.score += 10;
                    return false;
                }
                return true;
            });

            if (gameState.current.dots.length !== initialDotsCount) {
                setScore(gameState.current.score);
            }

            if (gameState.current.dots.length === 0) {
                alert("You win!");
                resetGame();
                setIsGameRunning(false);
                setIsMenuVisible(true);
                return;
            }

            // Ghosts
            ghosts.forEach(ghost => {
                const distance = Math.sqrt(
                    Math.pow(pacman.x - ghost.x, 2) + Math.pow(pacman.y - ghost.y, 2)
                );

                if (distance < CELL_SIZE) {
                    gameState.current.lives--;
                    setLives(gameState.current.lives);
                    if (gameState.current.lives <= 0) {
                        gameOver();
                    } else {
                        resetPositions();
                    }
                }
            });

            draw();
        };

        const draw = () => {
            // Clear canvas
            ctx.fillStyle = "#000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw walls
            ctx.fillStyle = "#2121de";
            for (let y = 0; y < GRID_HEIGHT; y++) {
                for (let x = 0; x < GRID_WIDTH; x++) {
                    if (isWall(x, y)) {
                        ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                    }
                }
            }

            // Draw dots
            ctx.fillStyle = "#fff";
            gameState.current.dots.forEach(dot => {
                ctx.beginPath();
                ctx.arc(
                    dot.x * CELL_SIZE + CELL_SIZE / 2,
                    dot.y * CELL_SIZE + CELL_SIZE / 2,
                    2, 0, Math.PI * 2
                );
                ctx.fill();
            });

            // Draw Pacman
            const { pacman } = gameState.current;
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
            gameState.current.ghosts.forEach(ghost => {
                ctx.fillStyle = ghost.color;
                ctx.beginPath();
                ctx.arc(
                    ghost.x + CELL_SIZE / 2,
                    ghost.y + CELL_SIZE / 2,
                    CELL_SIZE / 2,
                    Math.PI, 0
                );
                ctx.lineTo(ghost.x + CELL_SIZE, ghost.y + CELL_SIZE);
                ctx.lineTo(ghost.x, ghost.y + CELL_SIZE);
                ctx.fill();
            });
        };

        gameLoopRef.current = setInterval(update, 1000 / 60);

        return () => {
            clearInterval(gameLoopRef.current);
            window.removeEventListener("keydown", handleKeyPress);
        };
    }, [isGameRunning]); // Re-run effect when game running state changes

    return (
        <div className="game-container">
            <div className="score-container">
                <div className="score">Score: <span>{score}</span></div>
                <div className="lives">Lives: <span>{lives}</span></div>
            </div>
            <canvas ref={canvasRef} id="gameCanvas"></canvas>
            <div className={`menu ${isMenuVisible ? '' : 'hidden'}`}>
                <div className="menu-content">
                    <h2>Pacman</h2>
                    <button onClick={startNewGame}>New Game</button>
                    <button onClick={continueGame}>Continue</button>
                </div>
            </div>
        </div>
    );
};

export default PacmanGame;
