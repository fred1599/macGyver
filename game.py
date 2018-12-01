import os, sys
import glob
import pygame
from pygame.locals import *
from random import randint

WIDTH, HEIGHT = 300, 300

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

if not pygame.mixer: print('Warning, sound disabled')

# Constants
PATH_CURRENT_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_LEVEL = "level/level_{}.txt"
PATH_IMAGE = os.path.join(PATH_CURRENT_FILE, "images")

# list of surfaces in game
OBJECTS = {}
for f in glob.iglob(PATH_CURRENT_FILE + '/**/*.png', recursive=True):
    filename, ext = os.path.splitext(os.path.basename(f))
    OBJECTS[filename] = pygame.image.load(f).convert()

def load_level(n):
    """
    :param n: integer that is the number of level
    :return: list of lists that represents line and column of level
    """
    path = os.path.join(PATH_CURRENT_FILE, PATH_LEVEL.format(n))
    grounds = []
    with open(path, 'r') as f:
        for line in f:
            objects = list(map(int, list(line.rstrip('\n'))))
            grounds.append(objects)
    return grounds


def add_warn_object(surface, grounds, obj, speed):
    """
    :param surface: surface pygame where we draw
    :param grounds: list of lists who represents the level
    :param obj: surface pygame of object that we placed
    :param speed: integer who represents the number of pixel of image
    :return: None
    """
    while True:
        line_rand = randint(0, len(grounds)-1)
        column_rand = randint(0, len(grounds[0]) - 1)
        n = grounds[line_rand][column_rand]
        if n == 1:
            grounds[line_rand][column_rand] = -1
            surface.blit(obj, (column_rand*speed, line_rand*speed))
            break


def draw(grounds, pixels):
    """
    :param grounds: list of lists who represents the level
    :param pixels: integer who represents the number of pixel of image
    :return: None
    """
    obj = ("floor23", "floor15", "MacGyver", "guardian")
    for j, ground in enumerate(grounds):
        for i, n in enumerate(ground):
            if n >= 0:
                screen.blit(OBJECTS[obj[n]], (i*20, j*20))


def move(player, grounds, direction):
    """
    :param player: Integer represent the value placed in level
    :param grounds: list of lists who represents the level
    :param direction: index given by the user information by pressing the arrow keys
    :return: None
    """
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    x, y = directions[direction]
    column_max = len(grounds[0])
    for i, line in enumerate(grounds):
        if player in line:
            index = line.index(player)
            new_index = index + x # new column of player
            new_line = i + y # new line of player
            if 0 <= new_index < column_max:
                if grounds[new_line][new_index] == -1: # collision dangerous objects
                    return False # Quit Game with message "you lose"
                elif grounds[new_line][new_index] == 3: # collision guardian
                    return True # Quit Game with message "you win"
                elif grounds[new_line][new_index] != 0: # collision floor
                    grounds[new_line][new_index] = player
                    grounds[i][index] = 1 # floor
                break


def draw_result(win=True):
    """
    :param win: True or False for Winner or Loser
    :return: None
    """
    text = "You won" if win else "You lose"
    pygame.draw.rect(screen, (0, 0, 0), (25, 25, 100, 50))
    surf = pygame.font.SysFont('helvetica', 18).\
            render(text, True, (255, 255, 255))
    screen.blit(surf, (50, 50))


class Game:
    RIGHT, LEFT = 0, 1
    UP, DOWN = 2, 3
    SPEED = 20
    PLAYER = 2

    def __init__(self, start=1):
        self.grounds = load_level(start)
        draw(self.grounds, Game.SPEED)
        for name in ("aiguille", "ether", "seringue"):
            add_warn_object(screen, self.grounds, OBJECTS[name], Game.SPEED)

    def quit(self):
        """exit game"""
        self.continu = False
        pygame.quit()
        sys.exit()

    def start(self):
        """start game"""
        self.clock = pygame.time.Clock()

        self.continu = True
        while self.continu:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    for attr in ('RIGHT', 'LEFT', 'UP', 'DOWN'):
                        if event.key == getattr(pygame, f'K_{attr}'):
                            res = move(Game.PLAYER, self.grounds, getattr(Game, attr))
                            draw(self.grounds, Game.SPEED)
                            if res != None:
                                draw_result(res)
                                pygame.display.flip()
                                pygame.time.delay(2000)
                                self.quit()
            pygame.display.flip()

game = Game()
game.start()
