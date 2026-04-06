
# game.py
import pygame 
import random

pygame.init()

# -------------------- Настройки --------------------
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake & Tetris Game")
FONT = pygame.font.SysFont("comicsansms", 40)
SMALL_FONT = pygame.font.SysFont("comicsansms", 30)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)

# -------------------- Общие функции --------------------
def draw_text_center(text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, y))
    screen.blit(render, rect)

# -------------------- Змейка --------------------
CELL_SIZE = 20
SNAKE_WIDTH, SNAKE_HEIGHT = 600, 400

def snake_game():
    snake = [(SNAKE_WIDTH//2, SNAKE_HEIGHT//2)]
    snake_dir = (0, -CELL_SIZE)
    food = (random.randrange(0, SNAKE_WIDTH, CELL_SIZE), random.randrange(0, SNAKE_HEIGHT, CELL_SIZE))
    score = 0
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                    snake_dir = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                    snake_dir = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                    snake_dir = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                    snake_dir = (CELL_SIZE, 0)
        # Движение змейки
        head_x, head_y = snake[0]
        dx, dy = snake_dir
        new_head = (head_x + dx, head_y + dy)
        if new_head in snake or not (0 <= new_head[0] < SNAKE_WIDTH and 0 <= new_head[1] < SNAKE_HEIGHT):
            draw_text_center(f"Game Over! Счет: {score}", FONT, RED, HEIGHT//2)
            pygame.display.update()
            pygame.time.delay(2000)
            return
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = (random.randrange(0, SNAKE_WIDTH, CELL_SIZE), random.randrange(0, SNAKE_HEIGHT, CELL_SIZE))
        else:
            snake.pop()
        # Рисуем змейку и еду
        for x, y in snake:
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
        draw_text_center(f"Счет: {score}", SMALL_FONT, WHITE, HEIGHT - 20)
        pygame.display.update()
        clock.tick(10)

# -------------------- Меню --------------------
def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_center("Выберите игру", FONT, WHITE, 150)
        draw_text_center("1. Змейка", SMALL_FONT, GREEN, 250)
        draw_text_center("ESC - Выход", SMALL_FONT, GRAY, 550)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_game()
                elif event.key == pygame.K_2:
                    tetris_game()
                elif event.key == pygame.K_ESCAPE:
                    run = False

main_menu()
pygame.quit()
