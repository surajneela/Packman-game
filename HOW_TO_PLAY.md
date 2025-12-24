# How to Play Pacman on Your Laptop

This guide explains how to launch and control the Pacman game for both the Python and Java versions.

## 1. Universal Game Rules
The objective and rules are the same for both versions:
- **Goal**: Navigate Pacman through the maze and eat all the white dots.
- **Score**: Each dot eaten increases your score by 10 points.
- **Lives**: You start with **3 lives**.
- **Game Over**: If a ghost catches you, you lose a life. The game ends when you lose all lives.
- **Winning**: Clearing all dots resets the board (in some versions) or declares you a winner!

---

## 2. Python Version

### **How to Launch**
1. Open your terminal or command prompt.
2. Navigate to the Python folder: 
   `cd python_version`
3. Run the game:
   `python main.py`

### **Controls**
- **Arrow Up**    : Move Up
- **Arrow Down**  : Move Down
- **Arrow Left**  : Move Left
- **Arrow Right** : Move Right
- **ESC Key**     : Pause game / Return to Menu
- **Mouse Click** : Select "New Game" or "Continue" from the menu.

---

## 3. Java Version

### **How to Launch**
1. Open your terminal or command prompt.
2. Navigate to the Java folder:
   `cd "Java version"`
3. Compile (first time only):
   `javac PacmanGame.java`
4. Run the game:
   `java PacmanGame`

### **Controls**
- **Arrow Up**    : Move Up
- **Arrow Down**  : Move Down
- **Arrow Left**  : Move Left
- **Arrow Right** : Move Right
- **ESC Key**     : return to Menu
- **Mouse Click** : Select "New Game" or "Continue" from the menu.

---

## Tips for Success
- **Tunneling**: Use the side tunnels (if available in the map) to warp to the other side of the screen.
- **Ghost Personalities**: 
    - **Red**: Chases you directly.
    - **Pink**: Tries to ambush you.
    - **Cyan/Orange**: Have more random or patrolling behaviors.
