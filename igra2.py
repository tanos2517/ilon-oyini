import pygame
import random

pygame.init()

# -------------------- Sozlamalar --------------------
WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Ranglar
BLACK = (0,0,0)
WHITE = (255,255,255)
COLORS = [(0,255,255),(0,0,255),(255,165,0),(255,255,0),(0,255,0),(128,0,128),(255,0,0)]

# SHAPES (rotation variantlari bilan)
SHAPES = [
    # I
    [
        [[1,1,1,1]],
        [[1],[1],[1],[1]]
    ],
    # O
    [
        [[1,1],
         [1,1]]
    ],
    # T
    [
        [[0,1,0],
         [1,1,1]],
        [[1,0],
         [1,1],
         [1,0]],
        [[1,1,1],
         [0,1,0]],
        [[0,1],
         [1,1],
         [0,1]]
    ],
    # L
    [
        [[1,0,0],
         [1,1,1]],
        [[1,1],
         [1,0],
         [1,0]],
        [[1,1,1],
         [0,0,1]],
        [[0,1],
         [0,1],
         [1,1]]
    ],
    # J
    [
        [[0,0,1],
         [1,1,1]],
        [[1,0],
         [1,0],
         [1,1]],
        [[1,1,1],
         [1,0,0]],
        [[1,1],
         [0,1],
         [0,1]]
    ],
    # S
    [
        [[0,1,1],
         [1,1,0]],
        [[1,0],
         [1,1],
         [0,1]]
    ],
    # Z
    [
        [[1,1,0],
         [0,1,1]],
        [[0,1],
         [1,1],
         [1,0]]
    ]
]

# -------------------- Klasslar va funksiyalar --------------------
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

def create_grid(locked={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (x, y), color in locked.items():
        if y >= 0:
            grid[y][x] = color
    return grid

def convert_shape(piece):
    positions = []
    shape = piece.shape[piece.rotation % len(piece.shape)]
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                positions.append((piece.x + j, piece.y + i))
    return positions

def valid_space(piece, grid):
    for x, y in convert_shape(piece):
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and grid[y][x] != BLACK:
            return False
    return True

def check_lost(locked):
    for (x, y) in locked:
        if y < 1:
            return True
    return False

def clear_rows(grid, locked):
    cleared = 0
    for i in range(ROWS-1, -1, -1):
        if all(grid[i][j] != BLACK for j in range(COLS)):
            cleared += 1
            for j in range(COLS):
                del locked[(j, i)]
            # yuqoridagi bloklarni pastga tushirish
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                x, y = key
                if y < i:
                    locked[(x, y+1)] = locked.pop((x, y))
    return cleared

def draw_grid(screen, grid):
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(screen, grid[i][j],
                             (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # chiziqlar
    for i in range(ROWS):
        pygame.draw.line(screen, WHITE, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE))
    for j in range(COLS):
        pygame.draw.line(screen, WHITE, (j*CELL_SIZE, 0), (j*CELL_SIZE, HEIGHT))

def draw_text_center(text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, y))
    screen.blit(render, rect)

# -------------------- Tetris o‘yini --------------------
def tetris_game():
    locked = {}
    grid = create_grid(locked)
    current_piece = Piece(COLS//2-1, 0, random.choice(SHAPES))
    fall_time = 0
    fall_speed = 0.5
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("comicsansms", 40)
    score = 0

    run = True
    while run:
        grid = create_grid(locked)
        fall_time += clock.get_rawtime()
        clock.tick()

        # figura tushishi
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape(current_piece):
                    locked[pos] = current_piece.color
                current_piece = Piece(COLS//2-1, 0, random.choice(SHAPES))
                score += clear_rows(grid, locked)

        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        # current piece chizish
        for x, y in convert_shape(current_piece):
            if y >= 0:
                grid[y][x] = current_piece.color

        draw_grid(screen, grid)
        draw_text_center(f"Score: {score}", pygame.font.SysFont("comicsansms", 30), WHITE, 20)
        pygame.display.update()

        if check_lost(locked):
            draw_text_center("Game Over!", pygame.font.SysFont("comicsansms", 40), (255,0,0), HEIGHT//2)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

    pygame.quit()

# -------------------- Start --------------------
tetris_game()