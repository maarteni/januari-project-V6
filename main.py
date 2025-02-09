import pygame
import os
from settings import *  # Import settings like SCREEN_WIDTH, TILE_SIZE, colors

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to load the maze from a text file
def load_maze(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)  # Ensure correct file path
    with open(file_path, "r") as file:
        maze = [line.strip() for line in file]  # Read each line, removing extra spaces
    return maze

# Load the maze BEFORE using it
maze = load_maze("levels/level1.txt")

# List of levels
levels = ["levels/level1.txt", "levels/level2.txt", "levels/level3.txt", "levels/level4.txt", "levels/level5.txt"]
    
current_level = 0  # Start at Level 1
score = 0  # Keeps track of the player's score

def load_next_level():
    """Load the next level or show the final win screen after level 5."""
    global current_level, maze, player, goal, coins, enemies

    current_level += 1  # Move to the next level

    if current_level >= len(levels):  # If all levels are completed
        win_screen_final()  # Show the final win screen
        return  # Stop loading more levels

    # Load the new level
    maze = load_maze(levels[current_level])
    player = Player(maze)
    goal = Goal(maze)

    coins.clear()
    enemies.clear()
    for row_index, row in enumerate(maze):
        for col_index, tile in enumerate(row):
            if tile == 'C':
                coins.append((col_index, row_index))
            elif tile == 'E':
                enemies.append(Enemy(col_index, row_index))

def win_screen():
    """Display the win screen and wait for the player to continue."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)

    text = font.render("🎉 You Win! 🎉", True, WHITE)
    next_text = font.render("Press ENTER for Next Level", True, WHITE)

    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    screen.blit(next_text, next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    pygame.display.flip()

    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def win_screen_final():
    """Display the final win screen showing the total score and coins collected."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)

    # Final messages
    text1 = font.render("🎉 YOU BEAT THE GAME! 🎉", True, WHITE)
    text2 = font.render(f"Total Score: {score}", True, WHITE)
    text3 = font.render(f"Total Coins Collected: {score // 10}", True, WHITE)  # Since each coin = 10 points
    text4 = font.render("Press ESC to quit", True, WHITE)

    # Position text
    screen.blit(text1, text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)))
    screen.blit(text2, text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    screen.blit(text3, text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    screen.blit(text4, text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)))
    
    pygame.display.flip()  # Update the screen

    # Wait for ESC key to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Quit on ESC
                pygame.quit()
                exit()

class Player:
    """Player character that moves through the maze."""
    
    def __init__(self, maze):
        self.x, self.y = self.find_start_position(maze)

    def find_start_position(self, maze):
        """Find the player's starting position in the maze ('P')."""
        for row_index, row in enumerate(maze):
            for col_index, tile in enumerate(row):
                if tile == 'P':  # Found the player start position
                    return col_index * TILE_SIZE, row_index * TILE_SIZE
        return 0, 0  # Default if 'P' is missing

    def move(self, dx, dy):
        """Move the player by dx, dy while checking for walls, coins, enemies, and the goal."""
        
        new_x = self.x + dx * TILE_SIZE  # Move by tile size
        new_y = self.y + dy * TILE_SIZE  
        
        grid_x = new_x // TILE_SIZE
        grid_y = new_y // TILE_SIZE

        # ✅ Prevent moving through walls
        if maze[grid_y][grid_x] != 'W':  
            self.x = new_x
            self.y = new_y

            # ✅ Collect coins & update score
            global coins, score
            new_coins = []
            for cx, cy in coins:
                if self.x // TILE_SIZE == cx and self.y // TILE_SIZE == cy:
                    score += 10  # Increase score when collecting a coin
                    print(f"💰 Coin Collected! Score: {score}")  # Debugging message
                else:
                    new_coins.append((cx, cy))
            coins = new_coins  # Update the coin list

            # ✅ Check if the player touches an enemy (Game Over)
            for enemy in enemies:
                if self.x // TILE_SIZE == enemy.x and self.y // TILE_SIZE == enemy.y:
                    print("💀 You got caught! Game Over!")
                    pygame.time.delay(2000)
                    pygame.quit()
                    exit()

            # ✅ Check if the player reaches ANY goal
            for gx, gy in goal.positions:
                if self.x // TILE_SIZE == gx and self.y // TILE_SIZE == gy:
                    print("🎉 You Win! 🎉")
                    win_screen()
                    load_next_level()
                    return  # Stop checking after winning



    def draw(self):
        """Draw the player as a red square."""
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, TILE_SIZE, TILE_SIZE))

# Define the Enemy class (Moving Enemies)
class Enemy:
    """A moving enemy in the maze."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1  # 1 = moving right, -1 = moving left
        self.move_counter = 0  # Controls movement speed

    def move(self):
        """Move back and forth horizontally, bouncing off walls, but move every few frames."""
        self.move_counter += 1
        if self.move_counter % 15 == 0:  # Slow down movement (move every 15 frames)
            new_x = self.x + self.direction
            if maze[self.y][new_x] == 'W':  # Reverse if hitting a wall
                self.direction *= -1
            else:
                self.x = new_x

    def draw(self):
        """Draw the enemy as a red square."""
        pygame.draw.rect(screen, ENEMY_COLOR, 
                         (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Define the Goal class

class Goal:
    """Represents multiple goals that the player must reach."""

    def __init__(self, maze):
        self.positions = self.find_goal_positions(maze)  # Store all goal positions

    def find_goal_positions(self, maze):
        """Find all goal positions ('G') in the maze."""
        positions = []
        for row_index, row in enumerate(maze):
            for col_index, tile in enumerate(row):
                if tile == 'G':  # Found a goal
                    positions.append((col_index, row_index))
        return positions  # Store all goal positions

    def draw(self):
        """Draw all goal tiles as green squares."""
        for gx, gy in self.positions:
            pygame.draw.rect(screen, GOAL_COLOR, (gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Create Player, Goal, and Load Coins & Enemies
player = Player(maze)
goal = Goal(maze)
coins = []
enemies = []

# Scan the maze for coins and enemies
for row_index, row in enumerate(maze):
    for col_index, tile in enumerate(row):
        if tile == 'C':
            coins.append((col_index, row_index))
        elif tile == 'E':
            enemies.append(Enemy(col_index, row_index))  # Moving enemies

# Main game loop
running = True
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_left = max(LEVEL_TIME - elapsed_time, 0)

    if time_left == 0:
        print("⏳ Time's up! Game Over!")
        pygame.time.delay(2000)
        pygame.quit()
        exit()

    for enemy in enemies:
        enemy.move()

    screen.fill(BLACK)

    # Draw walls
    for row_index, row in enumerate(maze):
        for col_index, tile in enumerate(row):
            if tile == 'W':
                pygame.draw.rect(screen, BLUE, (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw game objects
    goal.draw()
    for cx, cy in coins:
        pygame.draw.circle(screen, COIN_COLOR, (cx * TILE_SIZE + TILE_SIZE // 2, cy * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
    for enemy in enemies:
        enemy.draw()
    player.draw()  # This must be here, not inside a loop

    pygame.display.flip()  # Refresh the screen
    clock.tick(FPS)  # Control the frame rate

pygame.quit()
