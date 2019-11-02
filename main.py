import pygame
import random

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((640, 672))

# Create the clock
clock = pygame.time.Clock()

# Title and icon
pygame.display.set_caption("Mark's Minesweeper")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

# Button images
untouched = pygame.image.load("assets/normal.png")
clear = pygame.image.load("assets/clear.png")
bomb = pygame.image.load("assets/bomb.png")
flag = pygame.image.load("assets/flag.png")
one = pygame.image.load("assets/1.png")
two = pygame.image.load("assets/2.png")
three = pygame.image.load("assets/3.png")
four = pygame.image.load("assets/4.png")
five = pygame.image.load("assets/5.png")
six = pygame.image.load("assets/6.png")
seven = pygame.image.load("assets/7.png")
eight = pygame.image.load("assets/8.png")
face = pygame.image.load("assets/face.png")

lost = False


# Tiles
class Tile:
    def __init__(self, x, y):
        self.has_bomb = False
        self.image = untouched
        self.count = 0
        self.flagged = False


# Generate tiles
tiles = {}
for i in range(0, 640, 32):
    for j in range(0, 640, 32):
        tiles[(i, j)] = Tile(i, j)


def draw_button(x, y):
    screen.blit(tiles[(x, y)].image, (x, y))


# Runs through each Tile in tiles. 1/3 chance of changing has_bomb to True
def generate_bombs():
    for tuple in tiles:
        tiles[tuple].has_bomb = False
        if random.randint(1, 10) == 1:
            tiles[tuple].has_bomb = True
    #     tiles[tuple].image = bomb


# Checks to see if neighbors have bombs, builds number
def check_neighbors(x, y):
    if not tiles[(x, y)].has_bomb:
        # Check up left
        if x - 32 >= 0 and y - 32 >= 0:
            if tiles[(x - 32, y - 32)].has_bomb:
                tiles[(x, y)].count += 1
        # Check up
        if y - 32 >= 0:
            if tiles[(x, y - 32)].has_bomb:
                tiles[(x, y)].count += 1
        # Check up right
        if x + 32 < 640 and y - 32 >= 0:
            if tiles[(x + 32, y - 32)].has_bomb:
                tiles[(x, y)].count += 1
        # Check left
        if x - 32 >= 0:
            if tiles[(x - 32, y)].has_bomb:
                tiles[(x, y)].count += 1
        # Check right
        if x + 32 < 640:
            if tiles[(x + 32, y)].has_bomb:
                tiles[(x, y)].count += 1
        # Check down left
        if x - 32 >= 0 and y + 32 < 640:
            if tiles[(x - 32, y + 32)].has_bomb:
                tiles[(x, y)].count += 1
        # Check down
        if y + 32 < 640:
            if tiles[(x, y + 32)].has_bomb:
                tiles[(x, y)].count += 1
        # Check down right
        if x + 32 < 640 and y + 32 < 640:
            if tiles[(x + 32, y + 32)].has_bomb:
                tiles[(x, y)].count += 1


def assign_icons(x, y):
    if not tiles[(x, y)].has_bomb:
        if tiles[(x, y)].count == 0:
            tiles[(x, y)].image = clear
        elif tiles[(x, y)].count == 1:
            tiles[(x, y)].image = one
        elif tiles[(x, y)].count == 2:
            tiles[(x, y)].image = two
        elif tiles[(x, y)].count == 3:
            tiles[(x, y)].image = three
        elif tiles[(x, y)].count == 4:
            tiles[(x, y)].image = four
        elif tiles[(x, y)].count == 5:
            tiles[(x, y)].image = five
        elif tiles[(x, y)].count == 6:
            tiles[(x, y)].image = six
        elif tiles[(x, y)].count == 7:
            tiles[(x, y)].image = seven
        elif tiles[(x, y)].count == 8:
            tiles[(x, y)].image = eight


def check_tile(x, y):
    if mouse_y < 640:
        if tiles[(x, y)].has_bomb:
            game_over()
        elif tiles[(x, y)].count != 0:
            assign_icons(x, y)
        elif tiles[(x, y)].count == 0:
            assign_icons(x, y)
            if y - 32 >= 0:
                if not tiles[(x, y - 32)].has_bomb and tiles[(x, y - 32)].count == 0 and tiles[
                    (x, y - 32)].image == untouched:
                    check_tile(x, y - 32)
            if x - 32 >= 0:
                if not tiles[(x - 32, y)].has_bomb and tiles[(x - 32, y)].count == 0 and tiles[
                    (x - 32, y)].image == untouched:
                    check_tile(x - 32, y)
            if y + 32 < 640:
                if not tiles[(x, y + 32)].has_bomb and tiles[(x, y + 32)].count == 0 and tiles[
                    (x, y + 32)].image == untouched:
                    check_tile(x, y + 32)
            if x + 32 < 640:
                if not tiles[(x + 32, y)].has_bomb and tiles[(x + 32, y)].count == 0 and tiles[
                    (x + 32, y)].image == untouched:
                    check_tile(x + 32, y)


# Bomb was clicked. Show all bombs, refuse more clicks
def game_over():
    global lost
    lost = True
    for i in range(0, 640, 32):
        for j in range(0, 640, 32):
            if tiles[(i, j)].has_bomb:
                tiles[(i, j)].image = bomb

# When face is clicked, clear everything and reassign bombs
def reset():
    global lost
    lost = False
    generate_bombs()
    for i in range(0, 640, 32):
        for j in range(0, 640, 32):
            tiles[(i, j)].count = 0
            tiles[(i, j)].flagged = False
            check_neighbors(i, j)
            tiles[(i, j)].image = untouched


# Generate bombs
generate_bombs()

# Check neighbors
for i in range(0, 640, 32):
    for j in range(0, 640, 32):
        check_neighbors(i, j)

# Main game loop
running = True
while running:

    # Grey background for the bottom
    screen.fill((128, 128, 128))
    # Set frame rate
    clock.tick(60)

    # Cycle through events
    for event in pygame.event.get():
        # Lets us quit
        if event.type == pygame.QUIT:
            running = False
        # Left mouse click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Get mouse click location
            pos = list(pygame.mouse.get_pos())
            # Check if face is clicked
            if pos[0] >= 304 and pos[0] <= 336 and pos[1] > 640:
                reset()
            if pos[1] < 640:
                # Convert coords to a multiple of 32, rounded down
                mouse_x = int(pos[0] / 32) * 32
                mouse_y = int(pos[1] / 32) * 32
                if not lost and not tiles[(mouse_x, mouse_y)].flagged:
                    check_tile(mouse_x, mouse_y)
        # Right mouse click
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            # Get mouse click location
            pos = list(pygame.mouse.get_pos())
            if pos[1] < 640:
                # Convert coords to a multiple of 32, rounded down
                mouse_x = int(pos[0] / 32) * 32
                mouse_y = int(pos[1] / 32) * 32
                if not lost:
                    # If no flag, make flag
                    if tiles[(mouse_x, mouse_y)].image == untouched:
                        tiles[(mouse_x, mouse_y)].flagged = True
                        tiles[(mouse_x, mouse_y)].image = flag
                    # If flag, make no flag
                    elif tiles[(mouse_x, mouse_y)].image == flag:
                        tiles[(mouse_x, mouse_y)].flagged = False
                        tiles[(mouse_x, mouse_y)].image = untouched

    # Draw buttons
    for i in range(0, 640, 32):
        for j in range(0, 640, 32):
            draw_button(i, j)
    # Draw face
    screen.blit(face, (304, 640))
    # Refresh screen
    pygame.display.update()
