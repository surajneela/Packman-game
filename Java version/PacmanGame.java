import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class PacmanGame extends JPanel implements ActionListener, KeyListener {

    // Constants
    private static final int CELL_SIZE = 20;
    private static final int GRID_WIDTH = 28;
    private static final int GRID_HEIGHT = 31;
    private static final int WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE;
    private static final int WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE;
    private static final int SCORE_HEIGHT = 60;
    private static final int PACMAN_SPEED = 2;
    private static final int GHOST_SPEED = 2; // Approximating 1.5 as 2 for simplicity in integer grid, or use float pos

    // Colors
    private static final Color COLOR_BLACK = Color.BLACK;
    private static final Color COLOR_BLUE = new Color(33, 33, 222);
    private static final Color COLOR_WHITE = Color.WHITE;
    private static final Color COLOR_YELLOW = Color.YELLOW;
    private static final Color COLOR_RED = Color.RED;
    private static final Color COLOR_PINK = new Color(255, 182, 193);
    private static final Color COLOR_CYAN = Color.CYAN;
    private static final Color COLOR_ORANGE = Color.ORANGE;

    // Game State
    private int score = 0;
    private int lives = 3;
    private boolean isMenuVisible = true;
    private boolean isGameRunning = false;
    private Timer timer;
    
    private Pacman pacman;
    private List<Ghost> ghosts;
    private List<Point> dots;

    // Buttons
    private Rectangle newGameRect;
    private Rectangle continueRect;

    public PacmanGame() {
        setPreferredSize(new Dimension(WINDOW_WIDTH, WINDOW_HEIGHT + SCORE_HEIGHT));
        setBackground(COLOR_BLACK);
        setFocusable(true);
        addKeyListener(this);

        // Initialize simplified buttons
        int buttonWidth = 200;
        int buttonHeight = 50;
        newGameRect = new Rectangle((WINDOW_WIDTH - buttonWidth) / 2, 250, buttonWidth, buttonHeight);
        continueRect = new Rectangle((WINDOW_WIDTH - buttonWidth) / 2, 320, buttonWidth, buttonHeight);

        // Mouse Listener for Menu
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (isMenuVisible) {
                    if (newGameRect.contains(e.getPoint())) {
                        startNewGame();
                    } else if (continueRect.contains(e.getPoint())) {
                        continueGame();
                    }
                }
            }
        });

        pacman = new Pacman();
        ghosts = new ArrayList<>();
        dots = new ArrayList<>();

        timer = new Timer(16, this); // ~60 FPS
        timer.start();
        
        resetGame();
    }

    private void resetGame() {
        score = 0;
        lives = 3;
        dots = initDots();
        initGhosts();
        resetPositions();
    }

    private void resetPositions() {
        pacman.reset();
        for (Ghost g : ghosts) {
            g.reset();
        }
    }

    private void startNewGame() {
        isMenuVisible = false;
        resetGame();
        isGameRunning = true;
    }

    private void continueGame() {
        isMenuVisible = false;
        isGameRunning = true;
    }

    private List<Point> initDots() {
        List<Point> d = new ArrayList<>();
        for (int y = 0; y < GRID_HEIGHT; y++) {
            for (int x = 0; x < GRID_WIDTH; x++) {
                if (!isWall(x, y, false)) {
                    d.add(new Point(x, y));
                }
            }
        }
        return d;
    }

    private void initGhosts() {
        ghosts.clear();
        ghosts.add(new Ghost(13 * CELL_SIZE, 11 * CELL_SIZE, "red"));
        ghosts.add(new Ghost(14 * CELL_SIZE, 11 * CELL_SIZE, "pink"));
        ghosts.add(new Ghost(13 * CELL_SIZE, 12 * CELL_SIZE, "cyan"));
        ghosts.add(new Ghost(14 * CELL_SIZE, 12 * CELL_SIZE, "orange"));
    }

    private boolean isWall(int x, int y, boolean isGhost) {
        // Outer walls
        if (x == 0 || x == GRID_WIDTH - 1 || y == 0 || y == GRID_HEIGHT - 1) return true;

        // Ghost house (center)
        if (x > 10 && x < 17 && y > 10 && y < 15) return !isGhost;

        // Map Design from Python version
        // S
        if (y == 3 && x >= 2 && x <= 5) return true;
        if (x == 2 && y >= 3 && y <= 6) return true;
        if (y == 6 && x >= 2 && x <= 5) return true;
        if (x == 5 && y >= 6 && y <= 9) return true;
        if (y == 9 && x >= 2 && x <= 5) return true;

        // U
        if (x == 7 && y >= 3 && y <= 9) return true;
        if (x == 10 && y >= 3 && y <= 9) return true;
        if (y == 9 && x >= 7 && x <= 10) return true;

        // R
        if (x == 12 && y >= 3 && y <= 9) return true;
        if (y == 3 && x >= 12 && x <= 15) return true;
        if (x == 15 && y >= 3 && y <= 6) return true;
        if (y == 6 && x >= 14 && x <= 15) return true;
        if (x == 15 && y >= 6 && y <= 9) return true;

        // A
        if (x == 17 && y >= 3 && y <= 9) return true;
        if (x == 20 && y >= 3 && y <= 9) return true;
        if (y == 3 && x >= 17 && x <= 20) return true;
        if (y == 6 && x >= 19 && x <= 20) return true;
        if (y == 6 && x == 17) return true;

        // J
        if (x == 24 && y >= 3 && y <= 9) return true;
        if (y == 9 && x >= 22 && x <= 24) return true;
        if (x == 22 && y >= 7 && y <= 9) return true;

        // Bottom filler
        if (y == 20 && x >= 4 && x <= 23) return true;
        if (x == 13 && y >= 20 && y <= 25) return true;
        if (x == 14 && y >= 20 && y <= 25) return true;
        if (y == 25 && x >= 2 && x <= 8) return true;
        if (y == 25 && x >= 19 && x <= 25) return true;

        return false;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (!isGameRunning) {
            repaint();
            return;
        }

        pacman.update();
        for (Ghost ghost : ghosts) {
            ghost.update();
        }

        // Check Dot Collisions
        int pGridX = pacman.x / CELL_SIZE;
        int pGridY = pacman.y / CELL_SIZE;
        
        // Remove collided dot
        for (int i = 0; i < dots.size(); i++) {
            Point d = dots.get(i);
            if (d.x == pGridX && d.y == pGridY) {
                dots.remove(i);
                score += 10;
                break; 
            }
        }

        if (dots.isEmpty()) {
            System.out.println("You win!");
            resetGame();
            isGameRunning = false;
            isMenuVisible = true;
        }

        // Check Ghost Collisions
        for (Ghost ghost : ghosts) {
            double distance = Math.sqrt(Math.pow(pacman.x - ghost.x, 2) + Math.pow(pacman.y - ghost.y, 2));
            if (distance < CELL_SIZE) {
                lives--;
                if (lives <= 0) {
                    System.out.println("Game Over!");
                    resetGame();
                    isMenuVisible = true;
                    isGameRunning = false;
                } else {
                    resetPositions();
                }
            }
        }

        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        
        // Offset everything by SCORE_HEIGHT
        g.translate(0, SCORE_HEIGHT);

        // Draw Walls
        g.setColor(COLOR_BLUE);
        for (int y = 0; y < GRID_HEIGHT; y++) {
            for (int x = 0; x < GRID_WIDTH; x++) {
                if (isWall(x, y, false)) {
                    g.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                }
            }
        }

        // Draw Dots
        g.setColor(COLOR_WHITE);
        for (Point dot : dots) {
            g.fillOval(dot.x * CELL_SIZE + CELL_SIZE / 2 - 2, dot.y * CELL_SIZE + CELL_SIZE / 2 - 2, 4, 4);
        }

        // Draw Pacman
        pacman.draw(g);

        // Draw Ghosts
        for (Ghost ghost : ghosts) {
            ghost.draw(g);
        }

        // Undo translation for UI
        g.translate(0, -SCORE_HEIGHT);

        // Draw Score UI
        g.setColor(COLOR_BLACK);
        g.fillRect(0, 0, WINDOW_WIDTH, SCORE_HEIGHT);
        g.setColor(COLOR_WHITE);
        g.setFont(new Font("Arial", Font.PLAIN, 24));
        g.drawString("Score: " + score, 20, 35);
        g.drawString("Lives: " + lives, WINDOW_WIDTH - 120, 35);

        // Draw Menu
        if (isMenuVisible) {
            drawMenu(g);
        }
    }

    private void drawMenu(Graphics g) {
        g.setColor(new Color(0, 0, 0, 200));
        g.fillRect(0, 0, getWidth(), getHeight());

        g.setColor(COLOR_YELLOW);
        g.setFont(new Font("Arial", Font.BOLD, 48));
        String title = "Pacman";
        int titleW = g.getFontMetrics().stringWidth(title);
        g.drawString(title, (getWidth() - titleW) / 2, 150);

        // Draw Buttons
        g.setColor(COLOR_BLUE);
        g.fillRect(newGameRect.x, newGameRect.y, newGameRect.width, newGameRect.height);
        g.fillRect(continueRect.x, continueRect.y, continueRect.width, continueRect.height);

        g.setColor(COLOR_WHITE);
        g.setFont(new Font("Arial", Font.PLAIN, 32));
        
        String startText = "New Game";
        int startW = g.getFontMetrics().stringWidth(startText);
        g.drawString(startText, newGameRect.x + (newGameRect.width - startW) / 2, newGameRect.y + 35);

        String contText = "Continue";
        int contW = g.getFontMetrics().stringWidth(contText);
        g.drawString(contText, continueRect.x + (continueRect.width - contW) / 2, continueRect.y + 35);
    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (!isGameRunning && !isMenuVisible) return;
        
        if (isMenuVisible) {
            // Can add menu navigation here
            return;
        }

        if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
            isGameRunning = false;
            isMenuVisible = true;
        } else if (e.getKeyCode() == KeyEvent.VK_RIGHT) pacman.nextDirection = 0;
        else if (e.getKeyCode() == KeyEvent.VK_DOWN) pacman.nextDirection = 1;
        else if (e.getKeyCode() == KeyEvent.VK_LEFT) pacman.nextDirection = 2;
        else if (e.getKeyCode() == KeyEvent.VK_UP) pacman.nextDirection = 3;
    }

    @Override
    public void keyReleased(KeyEvent e) {}
    @Override
    public void keyTyped(KeyEvent e) {}

    // Inner Classes

    class Pacman {
        int x, y;
        int direction = 0; // 0: Right, 1: Down, 2: Left, 3: Up
        int nextDirection = 0;
        double mouthOpen = 0;
        double mouthSpeed = 0.15;
        
        public Pacman() {
            reset();
        }

        public void reset() {
            x = 14 * CELL_SIZE;
            y = 17 * CELL_SIZE;
            direction = 0;
            nextDirection = 0;
            mouthOpen = 0;
        }

        public void update() {
            // Turning logic
            if (direction != nextDirection) {
                if (x % CELL_SIZE < PACMAN_SPEED && y % CELL_SIZE < PACMAN_SPEED) {
                    int alignedX = Math.round((float)x / CELL_SIZE) * CELL_SIZE;
                    int alignedY = Math.round((float)y / CELL_SIZE) * CELL_SIZE;
                    
                    int checkX = alignedX;
                    int checkY = alignedY;
                    if (nextDirection == 0) checkX += PACMAN_SPEED;
                    if (nextDirection == 1) checkY += PACMAN_SPEED;
                    if (nextDirection == 2) checkX -= PACMAN_SPEED;
                    if (nextDirection == 3) checkY -= PACMAN_SPEED;

                    if (!checkCollision(checkX, checkY)) {
                        direction = nextDirection;
                        x = alignedX;
                        y = alignedY;
                    }
                }
            }

            int newX = x;
            int newY = y;
            if (direction == 0) newX += PACMAN_SPEED;
            if (direction == 1) newY += PACMAN_SPEED;
            if (direction == 2) newX -= PACMAN_SPEED;
            if (direction == 3) newY -= PACMAN_SPEED;

            if (!checkCollision(newX, newY)) {
                x = newX;
                y = newY;
            }

            // Animate mouth
            mouthOpen += mouthSpeed;
            if (mouthOpen > 0.5 || mouthOpen < 0) {
                mouthSpeed = -mouthSpeed;
            }
        }

        public boolean checkCollision(int tx, int ty) {
            if (isWall(tx / CELL_SIZE, ty / CELL_SIZE, false)) return true;
            if (isWall((tx + CELL_SIZE - 1) / CELL_SIZE, ty / CELL_SIZE, false)) return true;
            if (isWall(tx / CELL_SIZE, (ty + CELL_SIZE - 1) / CELL_SIZE, false)) return true;
            if (isWall((tx + CELL_SIZE - 1) / CELL_SIZE, (ty + CELL_SIZE - 1) / CELL_SIZE, false)) return true;
            return false;
        }

        public void draw(Graphics g) {
            g.setColor(COLOR_YELLOW);
            int cx = x + CELL_SIZE / 2;
            int cy = y + CELL_SIZE / 2;
            int r = CELL_SIZE / 2;

            // Simplified mouth drawing using arc
            int startAngle = 0;
            int arcAngle = 360;
            
            int angleOffset = (int)(mouthOpen * 45 * 2); // full open angle
            int baseFace = 0;
            if (direction == 0) baseFace = 0; // Right
            if (direction == 1) baseFace = 270; // Down
            if (direction == 2) baseFace = 180; // Left
            if (direction == 3) baseFace = 90; // Up

            startAngle = baseFace + angleOffset / 2;
            arcAngle = 360 - angleOffset;

            g.fillArc(x, y, CELL_SIZE, CELL_SIZE, startAngle, arcAngle);
        }
    }

    class Ghost {
        int x, y;
        int startX, startY;
        Color color;
        int direction = 0;
        
        public Ghost(int sx, int sy, String colorName) {
            startX = sx;
            startY = sy;
            this.color = getColor(colorName);
            reset();
        }

        private Color getColor(String name) {
            switch(name) {
                case "red": return COLOR_RED;
                case "pink": return COLOR_PINK;
                case "cyan": return COLOR_CYAN;
                case "orange": return COLOR_ORANGE;
                default: return COLOR_RED;
            }
        }

        public void reset() {
            x = startX;
            y = startY;
            direction = 0;
        }

        public void update() {
            if (x % CELL_SIZE == 0 && y % CELL_SIZE == 0) {
                 if (Math.random() < 0.2) {
                     direction = (int)(Math.random() * 4);
                 }
            }

            int newX = x;
            int newY = y;
            if (direction == 0) newX += GHOST_SPEED;
            if (direction == 1) newY += GHOST_SPEED;
            if (direction == 2) newX -= GHOST_SPEED;
            if (direction == 3) newY -= GHOST_SPEED;

            if (!checkCollision(newX, newY)) {
                x = newX;
                y = newY;
            } else {
                direction = (int)(Math.random() * 4);
            }
        }

        public boolean checkCollision(int tx, int ty) {
            if (isWall(tx / CELL_SIZE, ty / CELL_SIZE, true)) return true;
            if (isWall((tx + CELL_SIZE - 1) / CELL_SIZE, ty / CELL_SIZE, true)) return true;
            if (isWall(tx / CELL_SIZE, (ty + CELL_SIZE - 1) / CELL_SIZE, true)) return true;
            if (isWall((tx + CELL_SIZE - 1) / CELL_SIZE, (ty + CELL_SIZE - 1) / CELL_SIZE, true)) return true;
            return false;
        }

        public void draw(Graphics g) {
            g.setColor(color);
            g.fillOval(x, y, CELL_SIZE, CELL_SIZE);
            g.fillRect(x, y + CELL_SIZE / 2, CELL_SIZE, CELL_SIZE / 2);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Pacman Java Version");
            PacmanGame game = new PacmanGame();
            frame.add(game);
            frame.pack();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}
