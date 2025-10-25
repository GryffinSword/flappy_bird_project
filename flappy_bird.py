# Imports
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Window/Screen Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100

# FPS
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)

# Bird Constants
GRAVITY = 0.5
FLAP_STRENGTH = -10
BIRD_SIZE = 15

# Pipe Constants
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_SPAWN_DISTANCE = 200

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = BIRD_SIZE

    def flap(self):
        """Make the bird jump upward"""
        self.velocity = FLAP_STRENGTH

    def update(self):
        """Update bird's position based on velocity and gravity"""
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent bird from going above screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self, screen):
        """Draw the bird as a yellow circle"""
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)

    def check_collision(self):
        """Check if bird hits the ground or ceiling"""
        # Hit the ground
        if self.y + self.size >= SCREEN_HEIGHT - GROUND_HEIGHT:
            return True
        # Hit the ceiling
        if self.y - self.size <= 0:
            return True
        return False
    
    def get_rect(self):
        """Get bird's rectangle for collision detection"""
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        # Random height for the gap between pipes
        self.gap_y = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - 150)
        self.passed = False

    def update(self):
        """Move pipe to the left"""
        self.x -= PIPE_SPEED

    def draw(self, screen):
        """Draw top and bottom pipes"""
        # Top pipe
        top_pipe_height = self.gap_y - PIPE_GAP // 2
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, self.width, top_pipe_height))

        # Bottom pipe
        bottom_pipe_y = self.gap_y + PIPE_GAP // 2
        bottom_pipe_height = SCREEN_HEIGHT - GROUND_HEIGHT - bottom_pipe_y
        pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_pipe_y, self.width, bottom_pipe_height))

    def is_off_screen(self):
        """Check if pipe has moved off the left side"""
        return self.x + self.width < 0
    
    def collides_with(self, bird):
        """Check if bird collides with this pipe"""
        bird_rect = bird.get_rect()

        # Top pipe rectangle
        top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)

        # Bottom pipe rectangle
        bottom_pipe_y = self.gap_y + PIPE_GAP // 2
        bottom_pipe = pygame.Rect(self.x, bottom_pipe_y, self.width, SCREEN_HEIGHT - GROUND_HEIGHT - bottom_pipe_y)

        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)


def draw_ground(screen):
    """Draw the ground at the bottom"""
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

def draw_game_over(screen):
    """Display game over message"""
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Restart Instruction
    small_font = pygame.font.Font(None, 36)
    restart_text = small_font.render("Press R to Restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(restart_text, restart_rect)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Create bird
bird = Bird()

# Create pipes list
pipes = [Pipe(SCREEN_WIDTH)]

# Game State
game_over = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Flap when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()

            # Restart game when R is pressed
            if event.key == pygame.K_r and game_over:
                bird = Bird()
                pipes = [Pipe(SCREEN_WIDTH)]
                game_over = False

    # Update game only if not game over
    if not game_over:
        # Update bird
        bird.update()

        # Update pipes
        for pipe in pipes:
            pipe.update()

            # Check collision with pipe
            if pipe.collides_with(bird):
                game_over = True

        # Remove pipes that are off screen
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        # Add new pipe when the last pipe is far enough
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - PIPE_SPAWN_DISTANCE:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Check for collision
        if bird.check_collision():
            game_over = True

    # Fill the screen with sky blue
    screen.fill(SKY_BLUE)

    # Draw pipes
    for pipe in pipes:
        pipe.draw(screen)

    # Draw ground
    draw_ground(screen)

    # Draw bird
    bird.draw(screen)

    # Draw game over screen if needed
    if game_over:
        draw_game_over(screen)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit
pygame.quit()
sys.exit()