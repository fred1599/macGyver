import os, sys
import glob
import pygame
from pygame.locals import *
from random import randint

if not pygame.mixer: print('Warning, sound disabled')

# Les constantes (taille fenêtre, chemin, ...)
WIDTH, HEIGHT = 300, 300
PATH_CURRENT_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_LEVEL = "level/level_{}.txt"
PATH_IMAGE = os.path.join(PATH_CURRENT_FILE, "images")

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# list of surface in game
OBJECTS = {}
for f in glob.iglob(PATH_CURRENT_FILE + '/**/*.png', recursive=True):
    filename, ext = os.path.splitext(os.path.basename(f))
    OBJECTS[filename] = pygame.image.load(f).convert()

def load_level(n):
    """
    n is the number of level
    load_level(1) -> list of list represents grounds for level 1
    """
    path = os.path.join(PATH_CURRENT_FILE, PATH_LEVEL.format(n))
    grounds = []
    with open(path, 'r') as f:
        for line in f:
            objects = list(map(int, list(line.rstrip('\n'))))
            grounds.append(objects)
    return grounds

def add_warn_object(surface, grounds, obj, speed):
    while True:
        line_rand = randint(0, len(grounds)-1)
        column_rand = randint(0, len(grounds[0]) - 1)
        n = grounds[line_rand][column_rand]
        if n == 1:
            grounds[line_rand][column_rand] = -1
            surface.blit(obj, (column_rand*speed, line_rand*speed))
            break

def draw(grounds, pixels):
    obj = ("floor23", "floor15", "MacGyver", "guardian")
    for j, ground in enumerate(grounds):
        for i, n in enumerate(ground):
            if n >= 0:
                screen.blit(OBJECTS[obj[n]], (i*20, j*20))

def move(player, grounds, direction):
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    x, y = directions[direction]
    column_max = len(grounds[0])
    for i, line in enumerate(grounds):
        if player in line:
            index = line.index(player)
            new_index = index + x
            new_line = i + y
            if 0 <= new_index < column_max:
                try:
                    if grounds[new_line][new_index] == -1:
                        return False
                    elif grounds[new_line][new_index] == 3:
                        return True
                    elif grounds[new_line][new_index] != 0:
                        grounds[new_line][new_index] = player
                        grounds[i][index] = 1 # floor
                except IndexError:
                    pass # do nothing
                break


def draw_result(win=True):
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
        add_warn_object(screen, self.grounds, OBJECTS["aiguille"], Game.SPEED)
        add_warn_object(screen, self.grounds, OBJECTS["ether"], Game.SPEED)
        add_warn_object(screen, self.grounds, OBJECTS["seringue"], Game.SPEED)

    def quit(self):
        """exit game"""
        self.continu = False
        pygame.quit()

    def start(self):
        """start game"""
        self.clock = pygame.time.Clock()

        self.continu = True
        while self.continu:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        res = move(Game.PLAYER, self.grounds, Game.RIGHT)
                    elif event.key == pygame.K_LEFT:
                        res = move(Game.PLAYER, self.grounds, Game.LEFT)
                    elif event.key == pygame.K_UP:
                        res = move(Game.PLAYER, self.grounds, Game.UP)
                    elif event.key == pygame.K_DOWN:
                        res = move(Game.PLAYER, self.grounds, Game.DOWN)

                    draw(self.grounds, Game.SPEED)
                    if res == False or res == True:
                        draw_result(res)
                        self.continu = False
                    pygame.display.flip()
            pygame.display.flip()

game = Game()
game.start()
