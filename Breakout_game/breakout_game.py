import sys
import pygame
from pygame.locals import *
import time
import pygame.mixer
import numpy as np

screen_size = (600, 800)
block_size = [48, 28]
block_padding = 1
block_occupancy = 0.4


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((100, 15))
        self.rect = self.image.get_rect()
        self.rect.bottom = screen_size[1]-20

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(Rect(0, 0, screen_size[0], screen_size[1]))


class Ball(pygame.sprite.Sprite):
    def __init__(self, bar, blocks, score, * groups):
        super().__init__(self.containers)
        radius = 7

        # Create Surface for image and display circle on it.
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (16, 225, 231),
                           (radius, radius), radius)
        self.rect = self.image.get_rect()

        self.dy = 0
        self.dy = 0
        self.life = 5
        self.bar = bar
        self.blocks = blocks
        self.update = self.start
        self.score = score

    def start(self):
        self.rect.centerx = self.bar.rect.centerx
        self.rect.bottom = self.bar.rect.top

        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = np.random.randint(-5, 5)
            self.dy = -10
            self.update = self.move

    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = -self.dx

        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
            self.dx = -self.dx

        if self.rect.top < 0:
            self.rect.top = 0
            self.dy = -self.dy

        if self.rect.colliderect(self.bar.rect) and self.dy > 0:
            self.rect.bottom = self.bar.rect.top
            self.dy = -self.dy
            raletive_pos = self.rect.centerx-self.bar.rect.centerx
            self.dx = 5*raletive_pos / \
                (self.bar.rect.right-self.bar.rect.centerx)
            self.hitbar_sound.play()

        if self.rect.bottom > screen_size[1]:
            # Reduce residue
            self.score.update_life(-1)
            self.update = self.start
            self.loselife_sound.play()

        block_collision = pygame.sprite.spritecollide(self, self.blocks, True)
        if block_collision:
            ball = self.rect
            for block in block_collision:
                # if the ball attacks from right side
                if ball.left > block.rect.left and ball.right > block.rect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx
                # if the ball attacks from left side
                if ball.right < block.rect.right and ball.left < block.rect.left:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                # if the ball attacks from top
                if ball.bottom < block.rect.bottom and ball.top < block.rect.top:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy
                # if the ball attacks from bottom
                if ball.bottom > block.rect.bottom and ball.top > block.rect.top:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy
                self.score.update_score(1)
                self.hitblock_sound.play()


class Block(pygame.sprite.Sprite):
    def __init__(self, i, j,):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface(block_size)
        # color randomize
        color = pygame.Color(0)
        height = int(screen_size[1]*block_occupancy /
                     (block_size[1]+2*block_padding))
        color.hsva = (350/height*j, 100, 78, 0.5)
        rgba = (color.r, color.g, color.b, color.a)
        self.image.fill(rgba)
        x = i*(block_size[0]+2 *
               block_padding)+block_padding
        y = j*(block_size[1]+2 *
               block_padding)+block_padding
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


class Score():
    def __init__(self, posx, posy):
        self.sysfont = pygame.font.SysFont('Comic Sans MS', 25)
        self.score = 0
        self.posx = posx
        self.posy = posy
        self.life = 5

    def draw(self, screen):
        score_dis = self.sysfont.render(
            "Score: "+str(self.score), False, (0, 0, 0))
        screen.blit(score_dis, (self.posx, self.posy))
        life_dis = self.sysfont.render(
            "LIFE: "+str(self.life), False, (239, 79, 9))
        screen.blit(life_dis, (self.posx, self.posy+30))

    def update_score(self, value):
        self.score += value

    def update_life(self, value):
        self.life += value


def main():
    SCREEN_SIZE = (600, 800)
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # sound
    Ball.hitbar_sound = pygame.mixer.Sound("breakout game/sound/hit_bar.mp3")
    Ball.hitblock_sound = pygame.mixer.Sound(
        "breakout game/sound/hit_block.mp3")
    Ball.loselife_sound = pygame.mixer.Sound(
        "breakout game/sound/lose_life.mp3")

    # RenderUpdates is the subset of Group()
    gp = pygame.sprite.RenderUpdates()
    blocks = pygame.sprite.Group()

    Bar.containers = gp
    Ball.containers = gp
    Block.containers = gp, blocks

    for i in range(int(screen_size[0]/(block_size[0]+2*block_padding))):
        for j in range(int(screen_size[1]*block_occupancy/(block_size[1]+2*block_padding))):
            Block(i, j)

    bar = Bar()
    score = Score(450, 700)

    Ball(bar, blocks, score)

    clock = pygame.time.Clock()

    while (True):
        screen.fill((255, 255, 255))
        clock.tick(60)
        gp.update()
        gp.draw(screen)
        score.draw(screen)
        pygame.display.update()
        time.sleep(0.001)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if score.life <= 0:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
