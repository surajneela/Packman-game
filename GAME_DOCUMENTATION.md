# Pacman Game Documentation

This document provides comprehensive instructions on how to set up, run, and play the Pacman game. The project includes both a Python desktop version and a React web version.

## 1. Cloning the Repository

To get started, you need to clone the repository to your local machine. Open your terminal or command prompt and run:

```bash
git clone <repository-url>
cd Packman-game
```

*(Replace `<repository-url>` with the actual URL of this repository)*

---

## 2. Python Version (Desktop Game)

The Python version is a standalone desktop application using `pygame`.

### Prerequisites
- Python 3.x installed.
- `pip` (Python package manager).

### Setup and Execution

1.  **Navigate to the Python directory:**
    ```bash
    cd python_version
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Game:**
    ```bash
    python main.py
    ```

### How to Play (Python)
- **Objective:** Eat all the dots while avoiding the ghosts.
- **Controls:**
    - **Arrow Keys:** Move Pacman (Up, Down, Left, Right).
    - **ESC:** Pause the game and open the menu.
    - **Mouse:** Click on "New Game" or "Continue" in the menu.
- **Scoring:**
    - Each dot is worth 10 points.
- **Lives:** You start with 3 lives. Colliding with a ghost loses a life.

---

## 3. React Version (Web Game)

The React version is a web-based implementation using Vite.

### Prerequisites
- Node.js and npm installed.

### Setup and Execution

1.  **Navigate to the project root:**
    (If you are in `python_version`, go back up one level: `cd ..`)
    Ensure you are in the `Packman-game` folder.

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Start the Development Server:**
    ```bash
    npm run dev
    ```

4.  **Play:**
    Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:5173/`).

### How to Play (Web)
*(Note: Controls for the web version typically mirror the desktop version, but refer to the on-screen instructions if available.)*
- **Arrow Keys:** Move Pacman.

---

## Troubleshooting

- **Python:** If `pygame` fails to install, ensure you have the necessary system build tools or try upgrading pip: `pip install --upgrade pip`.
- **React:** If `npm run dev` fails, try deleting `node_modules` and running `npm install` again.
