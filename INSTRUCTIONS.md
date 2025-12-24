# Project Setup and Execution Guide

This guide provides instructions on how to clone the repository and run both the Python and Java versions of the Pacman game.

## 1. Clone the Repository

To get started, clone the repository to your local machine using Git:

```bash
git clone <https://github.com/surajneela/Packman-game>
cd Packman
```

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

## 3. Java Version

This version is a standalone desktop application written in Java.

### Prerequisites
- Java Development Kit (JDK) installed (at least Java 8).

### Steps to Run

1.  **Navigate to the Java directory:**
    ```bash
    cd "Java version"
    ```

2.  **Compile the Code:**
    ```bash
    javac PacmanGame.java
    ```

3.  **Run the Game:**
    ```bash
    java PacmanGame
    ```

---

## Troubleshooting

- **Python Version:**
    - If you encounter a "module not found" error, ensure you have activated your virtual environment (if using one) and installed the requirements successfully.
    - If `python` command is not recognized, try using `python3` (on macOS/Linux) or check your system PATH variables.

- **Java Version:**
    - Ensure `javac` and `java` commands are in your system PATH.

