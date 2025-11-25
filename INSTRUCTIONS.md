# Project Setup and Execution Guide

This guide provides instructions on how to clone the repository and run both the Python and JavaScript (React) versions of the Pacman game.

## 1. Clone the Repository

To get started, clone the repository to your local machine using Git:

```bash
git clone <https://github.com/surajneela/Packman-game>
cd Packman
```

*(Replace `<https://github.com/surajneela/Packman-game>` with the actual URL of this repository)*

---

## 2. Python Version

This version is a standalone desktop application written in Python.

### Prerequisites
- Python 3.x installed on your system.
- `pip` (Python package installer).

### Steps to Run

1.  **Navigate to the Python directory:**
    ```bash
    cd python_version
    ```

2.  **Install Dependencies:**
    Install the required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Game:**
    Execute the main script to start the game:
    ```bash
    python main.py
    ```

The game window should open immediately.

---

## 3. JavaScript (React) Version

This is a web-based version of the game built with React and Vite. 
*(Note: This corresponds to the web application source code found in the `src` directory).*

### Prerequisites
- Node.js and npm (Node Package Manager) installed.

### Steps to Run

1.  **Navigate to the project root:**
    If you are currently in the `python_version` directory, go back to the root:
    ```bash
    cd ..
    ```
    Otherwise, ensure you are in the root `Packman` directory.

2.  **Install Dependencies:**
    Install the necessary Node.js packages:
    ```bash
    npm install
    ```

3.  **Start the Development Server:**
    Run the following command to start the local development server:
    ```bash
    npm run dev
    ```

4.  **Open in Browser:**
    The terminal will display a local URL (usually `http://localhost:5173/`). Open this URL in your web browser to play the game.

---

## Troubleshooting

- **Python Version:**
    - If you encounter a "module not found" error, ensure you have activated your virtual environment (if using one) and installed the requirements successfully.
    - If `python` command is not recognized, try using `python3` (on macOS/Linux) or check your system PATH variables.

- **JavaScript Version:**
    - If `npm install` fails, ensure you have a recent version of Node.js installed.
    - If the port 5173 is already in use, Vite will automatically try the next available port. Check the terminal output for the correct URL.
