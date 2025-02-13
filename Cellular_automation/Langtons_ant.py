import sys
import pygame
from pygame.locals import *
import time
import numpy as np

SCREEN_SIZE = (600, 500)
CELL_SIZE = 2
TICK = 1000


class Ant():
    def __init__(self, count):
        self.matrix = np.zeros(
            (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE))
        self.x, self.y = self.matrix.shape[0]//2, self.matrix.shape[1]//2
        self.direction = np.pi/2
        self.count = count

        # 上辺 (100,100) -> (200,100)
        self.matrix[100, 100:151] = 1

        # 右辺 (200,100) -> (200,200)
        self.matrix[100:201, 150] = 1

        # 下辺 (200,200) -> (100,200)
        self.matrix[200, 100:151] = 1

        # 左辺 (100,200) -> (100,100)
        self.matrix[100:201, 100] = 1

    def move(self):
        if self.matrix[self.x, self.y] == 0:  # if it is in the black
            self.matrix[self.x, self.y] = 1
            self.direction += np.pi/2
            self.x += np.cos(self.direction)
            self.y -= np.sin(self.direction)
        else:  # if it is in the white
            self.matrix[self.x, self.y] = 0
            self.direction -= np.pi/2
            self.x += np.cos(self.direction)
            self.y -= np.sin(self.direction)
        self.x = int(round(self.x) % self.matrix.shape[0])
        self.y = int(round(self.y) % self.matrix.shape[1])
        self.direction %= 2*np.pi

    def update(self, screen):
        self.move()
        self.count.update_count()
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.matrix[i, j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), (self.x*CELL_SIZE,
                         self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Count():
    def __init__(self, posx, posy):
        self.sysfont = pygame.font.SysFont('Arial', 20)
        self.count = 0
        self.posx = posx
        self.posy = posy
        self.life = 5

    def draw(self, screen):
        count_dis = self.sysfont.render(
            "Count: "+str(self.count), False, (255, 255, 255))
        screen.blit(count_dis, (self.posx, self.posy))

    def update_count(self):
        self.count += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Langton's ant")
    count = Count(20, 20)
    ant = Ant(count)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        clock.tick(TICK)
        ant.update(screen)
        count.draw(screen)
        pygame.display.update()
        time.sleep(0.00001)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
