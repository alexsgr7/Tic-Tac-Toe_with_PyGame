import pygame
import pygame.gfxdraw

# Initialize Pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Tic-Tac-Toe")

# Define game constants
cell_size = 200
line_width = 5
marker_size = 50
marker_color_x = (255, 0, 0)  # Red for "X"
marker_color_o = (0, 0, 255)  # Blue for "O"

# Define game variables
running = True
cell_sprites = []  # List to store cell sprites
current_player = "X"
game_over = False  # Variable to track game state


class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col, size):
        super().__init__()
        self.row = row
        self.col = col
        self.size = size
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.state = None  # This attribute stores the player's mark ("X" or "O")


def create_cells():
    for row in range(3):
        for col in range(3):
            cell = Cell(row, col, cell_size)
            cell.rect.topleft = (col * cell_size + 100, row * cell_size + 100)
            cell_sprites.append(cell)


create_cells()


# Define functions
def draw_board():
    screen.fill((255, 255, 255))
    for cell in cell_sprites:
        pygame.gfxdraw.rectangle(screen, cell.rect, (0, 0, 0))
        pygame.gfxdraw.rectangle(screen, cell.rect.inflate(-line_width, -line_width), (0, 0, 0))


def draw_x(x, y):
    pygame.draw.line(screen, marker_color_x, (x - marker_size, y - marker_size),
                     (x + marker_size, y + marker_size), 5)
    pygame.draw.line(screen, marker_color_x, (x - marker_size, y + marker_size),
                     (x + marker_size, y - marker_size), 5)


def draw_o(x, y):
    pygame.gfxdraw.aacircle(screen, x, y, marker_size, marker_color_o)
    pygame.gfxdraw.filled_circle(screen, x, y, marker_size, marker_color_o)


def is_valid_move():
    if game_over:  # Don't accept moves if the game is over
        return None

    pos = pygame.mouse.get_pos()
    for cell in cell_sprites:
        if cell.rect.collidepoint(pos) and cell.state is None:
            return cell.row, cell.col
    return None


def make_move(row, col):
    global current_player, game_over
    if is_valid_move() is not None:
        cell = cell_sprites[row * 3 + col]
        cell.state = current_player
        if current_player == "X":
            current_player = "O"
        elif current_player == "O":
            current_player = "X"

        if check_game_status():
            game_over = True


def check_game_status():
    def victory_check(player):
        for row in range(3):
            if (cell_sprites[row * 3].state == cell_sprites[row * 3 + 1].state == cell_sprites[row * 3 + 2].state ==
                    player):
                return True

        for col in range(3):
            if cell_sprites[col].state == cell_sprites[col + 3].state == cell_sprites[col + 6].state == player:
                return True

        if (cell_sprites[0].state == cell_sprites[4].state == cell_sprites[8].state == player) or \
           (cell_sprites[2].state == cell_sprites[4].state == cell_sprites[6].state == player):
            return True

        return False

    def draw_check():
        for cell in cell_sprites:
            if cell.state is None:
                return False
        return True

    if victory_check(current_player):
        print(f"{current_player} wins!")
        return True

    if draw_check():
        print("It's a draw.")
        return True

    return False


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            move = is_valid_move()
            if move is not None:
                make_move(move[0], move[1])

    draw_board()

    # Draw X and O marks based on cell state
    for cell in cell_sprites:
        if cell.state == "X":
            draw_x(cell.rect.centerx, cell.rect.centery)
        elif cell.state == "O":
            draw_o(cell.rect.centerx, cell.rect.centery)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
