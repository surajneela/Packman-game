import pygame
import sys
import math
import random

# Constants
CELL_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
PACMAN_SPEED = 2
GHOST_SPEED = 1.5
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
SCORE_HEIGHT = 60

# Colors
BLACK = (0, 0, 0)
BLUE = (33, 33, 222)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

def is_wall(x, y):
    # Outer walls
    if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
        return True

    # Ghost house (center)
    if 10 < x < 17 and 10 < y < 15:
        return True

    # S (Hollow-ish)
    # Top part (Left vertical, open right)
    if y == 3 and 2 <= x <= 5: return True # Top
    if x == 2 and 3 <= y <= 6: return True # Left Top
    if y == 6 and 2 <= x <= 5: return True # Mid

    # Bottom part (Right vertical, open left)
    if x == 5 and 6 <= y <= 9: return True # Right Bottom
    if y == 9 and 2 <= x <= 5: return True # Bottom

    # U (Hollow cup)
    if x == 7 and 3 <= y <= 9: return True
    if x == 10 and 3 <= y <= 9: return True
    if y == 9 and 7 <= x <= 10: return True

    # R (Hollow loop with leg)
    if x == 12 and 3 <= y <= 9: return True # Left spine
    if y == 3 and 12 <= x <= 15: return True # Top
    if x == 15 and 3 <= y <= 6: return True # Right loop
    if y == 6 and 14 <= x <= 15: return True # Mid (gap at 13)
    if x == 15 and 6 <= y <= 9: return True # Leg

    # A (Hollow arch)
    if x == 17 and 3 <= y <= 9: return True # Left leg
    if x == 20 and 3 <= y <= 9: return True # Right leg
    if y == 3 and 17 <= x <= 20: return True # Top
    if y == 6 and 19 <= x <= 20: return True # Crossbar (gap at 18)
    if y == 6 and x == 17: return True # Crossbar left bit

    # J (Hollow hook)
    if x == 24 and 3 <= y <= 9: return True # Right spine
    if y == 9 and 22 <= x <= 24: return True # Bottom
    if x == 22 and 7 <= y <= 9: return True # Hook tip

    # Bottom filler to keep game interesting
    if y == 20 and 4 <= x <= 23: return True
    if x == 13 and 20 <= y <= 25: return True
    if x == 14 and 20 <= y <= 25: return True

    if y == 25 and 2 <= x <= 8: return True
    if y == 25 and 19 <= x <= 25: return True

    return False

class Pacman:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = 14 * CELL_SIZE
        self.y = 17 * CELL_SIZE
        self.direction = 0 # 0: Right, 1: Down, 2: Left, 3: Up
        self.next_direction = 0
        self.mouth_open = 0
        self.mouth_speed = 0.15

    def check_collision(self, x, y):
        # Check all 4 corners of the Pacman rect (slightly smaller than cell to avoid edge cases)
        # We use a 1-pixel buffer to be safe, or just check the exact corners
        # Top-Left
        if is_wall(int(x // CELL_SIZE), int(y // CELL_SIZE)): return True
        # Top-Right (x + width - 1)
        if is_wall(int((x + CELL_SIZE - 1) // CELL_SIZE), int(y // CELL_SIZE)): return True
        # Bottom-Left
        if is_wall(int(x // CELL_SIZE), int((y + CELL_SIZE - 1) // CELL_SIZE)): return True
        # Bottom-Right
        if is_wall(int((x + CELL_SIZE - 1) // CELL_SIZE), int((y + CELL_SIZE - 1) // CELL_SIZE)): return True
        return False

    def update(self):
        # Handle Turning
        if self.direction != self.next_direction:
            # Check if we are close to the center of a tile to allow turning
            # We allow a small margin of error (SPEED)
            pixel_offset_x = self.x % CELL_SIZE
            pixel_offset_y = self.y % CELL_SIZE
            
            # Check if we are roughly aligned
            if pixel_offset_x < PACMAN_SPEED and pixel_offset_y < PACMAN_SPEED:
                # Snap to exact grid position
                aligned_x = round(self.x / CELL_SIZE) * CELL_SIZE
                aligned_y = round(self.y / CELL_SIZE) * CELL_SIZE
                
                # Check if the new direction is valid from the aligned position
                check_x, check_y = aligned_x, aligned_y
                if self.next_direction == 0: check_x += PACMAN_SPEED
                elif self.next_direction == 1: check_y += PACMAN_SPEED
                elif self.next_direction == 2: check_x -= PACMAN_SPEED
                elif self.next_direction == 3: check_y -= PACMAN_SPEED
                
                if not self.check_collision(check_x, check_y):
                    self.direction = self.next_direction
                    self.x = aligned_x
                    self.y = aligned_y

        # Move in current direction
        new_x = self.x
        new_y = self.y

        if self.direction == 0: new_x += PACMAN_SPEED
        elif self.direction == 1: new_y += PACMAN_SPEED
        elif self.direction == 2: new_x -= PACMAN_SPEED
        elif self.direction == 3: new_y -= PACMAN_SPEED

        # Check collision for the new position
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # If we hit a wall, we stop. 
            pass

        self.mouth_open += self.mouth_speed
        if self.mouth_open > 0.5 or self.mouth_open < 0:
            self.mouth_speed = -self.mouth_speed

    def draw(self, screen):
        center_x = int(self.x + CELL_SIZE / 2)
        center_y = int(self.y + CELL_SIZE / 2)
        radius = CELL_SIZE // 2
        
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        
        # Draw mouth
        angle_offset = self.mouth_open * 45 # Degrees
        base_angle = self.direction * 90
        
        p1 = (center_x, center_y)
        p2 = (center_x + radius * math.cos(math.radians(base_angle + angle_offset)),
              center_y + radius * math.sin(math.radians(base_angle + angle_offset)))
        p3 = (center_x + radius * math.cos(math.radians(base_angle - angle_offset)),
              center_y + radius * math.sin(math.radians(base_angle - angle_offset)))
        
        pygame.draw.polygon(screen, BLACK, [p1, p2, p3])


class Ghost:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.color_code = color
        self.color = self.get_color_rgb(color)
        self.reset()

    def get_color_rgb(self, name):
        if name == "red": return RED
        if name == "pink": return PINK
        if name == "cyan": return CYAN
        if name == "orange": return ORANGE
        return RED

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = 0
    
    def check_collision(self, x, y):
        # Same collision logic as Pacman
        if is_wall(int(x // CELL_SIZE), int(y // CELL_SIZE)): return True
        if is_wall(int((x + CELL_SIZE - 1) // CELL_SIZE), int(y // CELL_SIZE)): return True
        if is_wall(int(x // CELL_SIZE), int((y + CELL_SIZE - 1) // CELL_SIZE)): return True
        if is_wall(int((x + CELL_SIZE - 1) // CELL_SIZE), int((y + CELL_SIZE - 1) // CELL_SIZE)): return True
        return False
    
    def update(self):
        # Simple random movement AI
        # Try to continue in current direction, or turn
        
        # Align to grid for turning decisions
        if self.x % CELL_SIZE == 0 and self.y % CELL_SIZE == 0:
            if random.random() < 0.2: # Chance to change direction at intersection
                self.direction = random.randint(0, 3)

        new_x = self.x
        new_y = self.y

        if self.direction == 0: new_x += GHOST_SPEED
        elif self.direction == 1: new_y += GHOST_SPEED
        elif self.direction == 2: new_x -= GHOST_SPEED
        elif self.direction == 3: new_y -= GHOST_SPEED

        # Check collision
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            self.direction = random.randint(0, 3)

    def draw(self, screen):
        # Draw ghost body (circle top, rect bottom)
        x = int(self.x)
        y = int(self.y)
        
        pygame.draw.circle(screen, self.color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
        pygame.draw.rect(screen, self.color, (x, y + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE // 2))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + SCORE_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_font = pygame.font.SysFont('Arial', 48)
        self.button_font = pygame.font.SysFont('Arial', 32)
        
        self.reset_game()
        self.is_menu_visible = True
        self.is_game_running = False

    def init_dots(self):
        dots = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if not is_wall(x, y):
                    dots.append({'x': x, 'y': y})
        return dots

    def init_ghosts(self):
        return [
            Ghost(13 * CELL_SIZE, 11 * CELL_SIZE, "red"),
            Ghost(14 * CELL_SIZE, 11 * CELL_SIZE, "pink"),
            Ghost(13 * CELL_SIZE, 12 * CELL_SIZE, "cyan"),
            Ghost(14 * CELL_SIZE, 12 * CELL_SIZE, "orange"),
        ]

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.dots = self.init_dots()
        self.pacman = Pacman()
        self.ghosts = self.init_ghosts()
        self.reset_positions()

    def reset_positions(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()

    def start_new_game(self):
        self.is_menu_visible = False
        self.reset_game()
        self.is_game_running = True

    def continue_game(self):
        self.is_menu_visible = False
        self.is_game_running = True

    def game_over(self):
        self.is_game_running = False
        # In a real game we might show a message, here we just go back to menu
        # But let's show "Game Over" briefly or just reset
        print("Game Over!")
        self.reset_game()
        self.is_menu_visible = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.is_menu_visible:
                    # Simple menu navigation with keys or just click
                    pass
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.is_game_running = False
                        self.is_menu_visible = True
                    elif event.key == pygame.K_RIGHT: self.pacman.next_direction = 0
                    elif event.key == pygame.K_DOWN: self.pacman.next_direction = 1
                    elif event.key == pygame.K_LEFT: self.pacman.next_direction = 2
                    elif event.key == pygame.K_UP: self.pacman.next_direction = 3

            if event.type == pygame.MOUSEBUTTONDOWN and self.is_menu_visible:
                mouse_pos = event.pos
                # Check button clicks
                # New Game Button
                if self.new_game_rect.collidepoint(mouse_pos):
                    self.start_new_game()
                # Continue Button
                elif self.continue_rect.collidepoint(mouse_pos):
                    self.continue_game()

    def update(self):
        if not self.is_game_running:
            return

        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update()

        # Check collisions
        # Dots
        p_grid_x = int(self.pacman.x // CELL_SIZE)
        p_grid_y = int(self.pacman.y // CELL_SIZE)
        
        # Filter dots
        new_dots = []
        for dot in self.dots:
            if dot['x'] == p_grid_x and dot['y'] == p_grid_y:
                self.score += 10
            else:
                new_dots.append(dot)
        self.dots = new_dots

        if len(self.dots) == 0:
            print("You win!")
            self.reset_game()
            self.is_game_running = False
            self.is_menu_visible = True
            return

        # Ghosts
        for ghost in self.ghosts:
            distance = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
            if distance < CELL_SIZE:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.reset_positions()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw Score Area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WINDOW_WIDTH, SCORE_HEIGHT))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (WINDOW_WIDTH - 100, 20))

        # Draw Game Area Offset
        game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        game_surface.fill(BLACK)

        # Draw Walls
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if is_wall(x, y):
                    pygame.draw.rect(game_surface, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Dots
        for dot in self.dots:
            pygame.draw.circle(game_surface, WHITE, 
                             (dot['x'] * CELL_SIZE + CELL_SIZE // 2, dot['y'] * CELL_SIZE + CELL_SIZE // 2), 
                             2)

        # Draw Entities
        # We need to pass the surface to draw on, but our classes draw on 'screen'.
        # Let's adjust the classes to accept a surface and offsets, or just translate the context.
        # Actually, let's just draw directly on screen with offset.
        
        offset_y = SCORE_HEIGHT
        self.screen.blit(game_surface, (0, offset_y))
        
        # We need to draw dynamic elements with offset
        # Redefine draw methods to take offset? Or just move the surface blit after?
        # If we draw pacman on game_surface, it will be easier.
        
        self.pacman.draw(game_surface)
        for ghost in self.ghosts:
            ghost.draw(game_surface)
            
        self.screen.blit(game_surface, (0, offset_y))

        # Draw Menu
        if self.is_menu_visible:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + SCORE_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230)) # Semi-transparent black
            self.screen.blit(overlay, (0, 0))
            
            title_text = self.menu_font.render("Pacman", True, YELLOW)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)
            
            # Buttons
            button_width = 200
            button_height = 50
            
            self.new_game_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 250, button_width, button_height)
            self.continue_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 320, button_width, button_height)
            
            pygame.draw.rect(self.screen, BLUE, self.new_game_rect, border_radius=5)
        y = int(self.y)
        
        pygame.draw.circle(screen, self.color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2)
        pygame.draw.rect(screen, self.color, (x, y + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE // 2))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + SCORE_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_font = pygame.font.SysFont('Arial', 48)
        self.button_font = pygame.font.SysFont('Arial', 32)
        
        self.reset_game()
        self.is_menu_visible = True
        self.is_game_running = False

    def init_dots(self):
        dots = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if not is_wall(x, y):
                    dots.append({'x': x, 'y': y})
        return dots

    def init_ghosts(self):
        return [
            Ghost(13 * CELL_SIZE, 11 * CELL_SIZE, "red"),
            Ghost(14 * CELL_SIZE, 11 * CELL_SIZE, "pink"),
            Ghost(13 * CELL_SIZE, 12 * CELL_SIZE, "cyan"),
            Ghost(14 * CELL_SIZE, 12 * CELL_SIZE, "orange"),
        ]

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.dots = self.init_dots()
        self.pacman = Pacman()
        self.ghosts = self.init_ghosts()
        self.reset_positions()

    def reset_positions(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()

    def start_new_game(self):
        self.is_menu_visible = False
        self.reset_game()
        self.is_game_running = True

    def continue_game(self):
        self.is_menu_visible = False
        self.is_game_running = True

    def game_over(self):
        self.is_game_running = False
        # In a real game we might show a message, here we just go back to menu
        # But let's show "Game Over" briefly or just reset
        print("Game Over!")
        self.reset_game()
        self.is_menu_visible = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.is_menu_visible:
                    # Simple menu navigation with keys or just click
                    pass
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.is_game_running = False
                        self.is_menu_visible = True
                    elif event.key == pygame.K_RIGHT: self.pacman.next_direction = 0
                    elif event.key == pygame.K_DOWN: self.pacman.next_direction = 1
                    elif event.key == pygame.K_LEFT: self.pacman.next_direction = 2
                    elif event.key == pygame.K_UP: self.pacman.next_direction = 3

            if event.type == pygame.MOUSEBUTTONDOWN and self.is_menu_visible:
                mouse_pos = event.pos
                # Check button clicks
                # New Game Button
                if self.new_game_rect.collidepoint(mouse_pos):
                    self.start_new_game()
                # Continue Button
                elif self.continue_rect.collidepoint(mouse_pos):
                    self.continue_game()

    def update(self):
        if not self.is_game_running:
            return

        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update()

        # Check collisions
        # Dots
        p_grid_x = int(self.pacman.x // CELL_SIZE)
        p_grid_y = int(self.pacman.y // CELL_SIZE)
        
        # Filter dots
        new_dots = []
        for dot in self.dots:
            if dot['x'] == p_grid_x and dot['y'] == p_grid_y:
                self.score += 10
            else:
                new_dots.append(dot)
        self.dots = new_dots

        if len(self.dots) == 0:
            print("You win!")
            self.reset_game()
            self.is_game_running = False
            self.is_menu_visible = True
            return

        # Ghosts
        for ghost in self.ghosts:
            distance = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
            if distance < CELL_SIZE:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.reset_positions()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw Score Area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WINDOW_WIDTH, SCORE_HEIGHT))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (WINDOW_WIDTH - 100, 20))

        # Draw Game Area Offset
        game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        game_surface.fill(BLACK)

        # Draw Walls
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if is_wall(x, y):
                    pygame.draw.rect(game_surface, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Dots
        for dot in self.dots:
            pygame.draw.circle(game_surface, WHITE, 
                             (dot['x'] * CELL_SIZE + CELL_SIZE // 2, dot['y'] * CELL_SIZE + CELL_SIZE // 2), 
                             2)

        # Draw Entities
        # We need to pass the surface to draw on, but our classes draw on 'screen'.
        # Let's adjust the classes to accept a surface and offsets, or just translate the context.
        # Actually, let's just draw directly on screen with offset.
        
        offset_y = SCORE_HEIGHT
        self.screen.blit(game_surface, (0, offset_y))
        
        # We need to draw dynamic elements with offset
        # Redefine draw methods to take offset? Or just move the surface blit after?
        # If we draw pacman on game_surface, it will be easier.
        
        self.pacman.draw(game_surface)
        for ghost in self.ghosts:
            ghost.draw(game_surface)
            
        self.screen.blit(game_surface, (0, offset_y))

        # Draw Menu
        if self.is_menu_visible:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + SCORE_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230)) # Semi-transparent black
            self.screen.blit(overlay, (0, 0))
            
            title_text = self.menu_font.render("Pacman", True, YELLOW)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title_text, title_rect)
            
            # Buttons
            button_width = 200
            button_height = 50
            
            self.new_game_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 250, button_width, button_height)
            self.continue_rect = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 320, button_width, button_height)
            
            pygame.draw.rect(self.screen, BLUE, self.new_game_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLUE, self.continue_rect, border_radius=5)
            
            new_game_text = self.button_font.render("New Game", True, WHITE)
            continue_text = self.button_font.render("Continue", True, WHITE)
            
            self.screen.blit(new_game_text, new_game_text.get_rect(center=self.new_game_rect.center))
            self.screen.blit(continue_text, continue_text.get_rect(center=self.continue_rect.center))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()