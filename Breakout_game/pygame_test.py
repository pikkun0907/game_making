import sys
import pygame
from pygame.locals import *
import time

# 画面サイズ 600×500
SCREEN_SIZE = (600, 500)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game")
    px = 120
    py = 100
    x_direction = "RIGHT"
    y_direction = "UP"
    while True:
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (10, 10, 10), (px, py), 10)    # ●
        pygame.draw.rect(screen, (255, 0, 0), Rect(10, 275, 50, 50), 1)    # ■
        # pygame.draw.line(screen, (0, 255, 0), (0, 200), (100, 300), 2)

        if x_direction == "RIGHT":
            px += 1
            if px > 600:
                x_direction = "LEFT"
        elif x_direction == "LEFT":
            px -= 1
            if px < 0:
                x_direction = "RIGHT"

        if y_direction == "UP":
            py -= 1
            if py < 0:
                y_direction = "DOWN"
        elif y_direction == "DOWN":
            py += 1
            if py > 500:
                y_direction = "UP"

        pygame.display.update()
        time.sleep(0.001)
        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit()  # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
    main()
