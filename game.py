import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# Les constantes (taille fenêtre, chemin, ...)
WIDTH, HEIGHT = 300, 300
PATH_CURRENT_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_LEVEL = "level/level_{}.txt"

class Level:

    def __init__(self, n):
        self.content = self.load(PATH_LEVEL.format(n))

    def load(self, path):
        obj = []
        with open(path, 'r') as f:
            for line in f:
                array_obj = map(int, list(line.rstrip('\n')))
                obj.append(list(array_obj))
        return obj

    def draw(self, surface, speed):
        i, j = speed, speed
        for line in self.content:
            for n in line:
                if n == 0:
                    obj = Obj("floor23")
                elif n == 1:
                    obj = Obj("floor15")
                elif n == 2:
                    obj = Player()
                elif n == 3:
                    obj = Obj("guardian")
                surface.blit(obj.image, (i, j))
                i += speed
            i = 0
            j += speed

class Obj(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.path = os.path.join(PATH_CURRENT_FILE, f"images/{name}.png")
        self.image = pygame.image.load(self.path).convert()
        self.pos = self.image.get_rect()

    def draw(self, surface, pos):
        surface.blit(self.image, pos)

class Player(Obj):

    def __init__(self):
        Obj.__init__(self, "MacGyver")
        self.pos_x, self.pos_y = self.pos.x, self.pos.y

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            new_pos = self.pos_x + Player.speed
            if new_pos < WIDTH:
                self.update()
                self.pos_x = new_pos
        elif key[pygame.K_LEFT]:
            new_pos = self.pos_x - Player.speed
            if new_pos >= 0:
                self.update()
                self.pos_x = new_pos
        elif key[pygame.K_UP]:
            new_pos = self.pos_y - Player.speed
            if new_pos >= 0:
                self.update()
                self.pos_y = new_pos
        elif key[pygame.K_DOWN]:
            new_pos = self.pos_y + Player.speed
            if new_pos < HEIGHT:
                self.update()
                self.pos_y = new_pos

    def draw(self, surface):
        surface.blit(self.image, (self.pos_x, self.pos_y))

    def update(self):
        self.pos.x = self.pos_x
        self.pos.y = self.pos_y

class Game:

    def __init__(self):
        pygame.display.set_mode((WIDTH, HEIGHT))

    def quit(self):
        """exit game"""
        self.continu = False
        pygame.quit()

    def start(self):
        """start game"""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.level = Level(1)
        self.clock = pygame.time.Clock()

        self.continu = True
        while self.continu:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.level.draw(self.screen, 20)  # 20 is speed pixels

                    pygame.display.flip()
            pygame.display.flip()



game = Game()
game.start()
