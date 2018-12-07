import os
import sys
from random import randint

import pygame


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game Resolution
WIDTH = 300
HEIGHT = 300

class Game:
    PATH_CURRENT_FILE = os.path.abspath(os.path.dirname(__file__))
    PATH_LEVEL = "level/level_{}.txt"
    PATH_IMAGES = "images"
    PATH_BONUS = "images/bonus"
    DIRECTIONS = {
        "RIGHT": (1, 0), "LEFT": (-1, 0),
        "UP": (0, -1), "DOWN": (0, 1)
    }

    PLAYER = 2
    GUARDIAN = 3

    WALL = 0
    FLOOR = 1
    BONUS = -1

    FLOORS = ('images/floor15.png', 'images/floor23.png')
    GUARDIAN_IMAGE = 'images/guardian.png'
    MACGYVER_IMAGE = 'images/MacGyver.png'
    WINNER = 'images/player/winner.png'

    IMAGES = {WALL: FLOORS[1], FLOOR: FLOORS[0],
              GUARDIAN: GUARDIAN_IMAGE, PLAYER: MACGYVER_IMAGE}

    PIXELS = 20

    def __init__(self, n):
        self.win = False
        self.n = n
        self.level = []
        self.tiles = []
        self.bonus = []
        self.points = 0
        self.total = 0

    def load_level(self):
        with open(Game.PATH_LEVEL.format(self.n)) as f:
            for line in f:
                new_line = line.rstrip('\n')
                self.level.append(list(map(int, list(new_line))))

    def load_bonus(self):
        for f in os.listdir(Game.PATH_BONUS):
            path = os.path.join(Game.PATH_BONUS, f)
            surface = pygame.image.load(path).convert()
            self.bonus.append(surface)
            self.total += 1

    def load_tile(self, path):
        surface = pygame.image.load(path).convert()
        self.tiles.append(surface)
        return surface

    def move(self, key):
        if self.win:
            return

        elif hasattr(self, "all_bonus"):
            if not self.all_bonus:
                return

        x, y = Game.DIRECTIONS[key]
        for line, columns in enumerate(self.level):
            if Game.PLAYER in columns:
                column = columns.index(Game.PLAYER)
                break

        try:
            if self.level[line + y][column + x] != Game.WALL:
                if self.level[line + y][column + x] == Game.BONUS:
                    self.points += 1

                elif self.level[line + y][column + x] == Game.GUARDIAN:
                    if self.points == self.total:
                        self.win = True
                    else:
                        self.all_bonus = False

                self.level[line + y][column + x] = Game.PLAYER
                self.level[line][column] = Game.FLOOR
        except IndexError:
            pass

    def place_bonus(self):
        for tile in self.bonus:
            while True:
                line = randint(0, len(self.level) - 1)
                column = randint(0, len(self.level[0]) - 1)
                value = self.level[line][column]
                if value == Game.FLOOR:
                    self.level[line][column] = Game.BONUS
                    break

    def draw(self, pixels):
        for i, line in enumerate(self.level):
            for j, value in enumerate(line):
                pos = (j * pixels, i * pixels)
                if value in (Game.WALL, Game.FLOOR,
                             Game.GUARDIAN, Game.PLAYER):
                    SCREEN.blit(self.load_tile(Game.IMAGES[value]), pos)
                else:
                    if self.bonus:
                        SCREEN.blit(self.bonus.pop(), pos)
        if self.win:
            self.draw_result("YOU WON!")
        elif hasattr(self, "all_bonus"):
            if not self.all_bonus:
                self.draw_result("YOU LOSE!")

    def draw_result(self, text):
        pygame.draw.rect(SCREEN, WHITE, [50, 50, 225, 100])
        text = text_format(text, font, 45, BLACK)
        SCREEN.blit(text, (60, 60, 200, 100))

    def start(self):
        self.load_level()
        self.load_bonus()
        self.place_bonus()
        self.draw(Game.PIXELS)
        clock.tick(FPS)

        # loop of game
        continu = True
        while continu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continu = False
                    for direction in Game.DIRECTIONS:
                        if event.key == getattr(pygame, f'K_{direction}'):
                            self.move(direction)
                            self.draw(Game.PIXELS)
                            pygame.display.flip()
            pygame.display.flip()
        pygame.quit()
        sys.exit()


def text_format(message, text_font, textSize, textColor):
    new_font = pygame.font.Font(text_font, textSize)
    new_text = new_font.render(message, 0, textColor)

    return new_text


def main_menu():
    menu = True
    selected = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = True
                elif event.key == pygame.K_DOWN:
                    selected = False
                if event.key == pygame.K_RETURN:
                    if selected:
                        Game(1).start()
                    else:
                        pygame.quit()
                        quit()

        # Main Menu UI
        SCREEN.fill(BLUE)
        title = text_format("Mc Gyver", font, 45, YELLOW)
        if selected:
            text_start = text_format("START", font, 30, WHITE)
            start_rect = text_start.get_rect()
            SCREEN.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 150))
        elif not selected:
            text_quit = text_format("QUIT", font, 30, BLACK)
            quit_rect = text_quit.get_rect()
            SCREEN.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 180))

        title_rect = title.get_rect()

        # Main Menu Text
        SCREEN.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Mc Gyver - Main Menu")


# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Fonts
font = "Airstream.ttf"

# Game Framerate
clock = pygame.time.Clock()
FPS = 30

main_menu()
