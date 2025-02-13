import sys
import pygame
from pygame.locals import *
import time
import numpy as np

SCREEN_SIZE = (600, 700)
TICK = 30


class Cal():
    def __init__(self, score):
        self.board = np.zeros((4, 4))
        self.location = [(10+145*x, 110+145*y)
                         for y in range(4) for x in range(4)]
        self.color_palette = [(240, 247, 212), (178, 215, 50),
                              (254, 39, 18), (52, 123, 152), (9, 40, 52),
                              (253, 187, 45), (62, 172, 174),
                              (143, 40, 127), (245, 114, 63), (79, 137, 29)]
        self.padding = 8
        self.border_radius = 8
        self.score = score

        self.points = [(x, y) for x in range(4) for y in range(4)]
        selected_points = np.random.choice(len(self.points), 2, replace=False)
        init_loc = [self.points[i] for i in selected_points]
        for loc in init_loc:
            self.board[loc] = np.random.choice([2, 4])
        self.score.update_count(self.board.sum())

    def spawn(self):
        nonoccupied_loc = np.argwhere(self.board.flatten() == 0)
        new_points = []
        for loc in nonoccupied_loc:
            new_points.append(self.points[loc[0]])

        if new_points == []:
            self.reset()
            return

        selected_points = np.random.choice(len(new_points), 1, replace=False)
        self.board[new_points[selected_points[0]]] = np.random.choice([2, 4])

    def update(self, direction):
        """
        direction::
        right=0
        up=1
        left=2
        down=3
        """
        self.board = np.rot90(self.board, -direction)
        for i, row in enumerate(self.board):
            row_updated = []
            row = row[::-1]
            row_ = np.append(row[row.nonzero()], 0)
            flag = True

            for idx, ele in enumerate(row_[:-1]):
                if ele == row_[idx+1] and flag:
                    row_updated.append(2*ele)
                    flag = False
                else:
                    if flag:
                        row_updated.append(ele)
                    flag = True

            while len(row_updated) < 4:
                row_updated = np.append(row_updated, 0)
            self.board[i, :] = row_updated[::-1]

        self.board = np.rot90(self.board, direction)
        self.spawn()
        self.score.update_count(self.board.sum())

    def draw(self, screen):
        for idx, ele in enumerate(self.board.flatten()):
            if ele != 0:
                rect = pygame.Rect(
                    self.location[idx][0]+self.padding, self.location[idx][1]+self.padding, 145-self.padding*2, 145-self.padding*2)
                color_idx = len(format(int(ele), 'b')[1:])
                pygame.draw.rect(screen, self.color_palette[color_idx], rect,
                                 border_radius=self.border_radius)

                number = pygame.font.Font(None, 70)
                number_dis = number.render(
                    f"{int(ele)}", True, (255, 255, 255))
                number_rect = number_dis.get_rect(center=rect.center)
                screen.blit(number_dis, number_rect)

    def reset(self):
        self.board = np.zeros((4, 4))
        self.points = [(x, y) for x in range(4) for y in range(4)]
        selected_points = np.random.choice(len(self.points), 2, replace=False)
        init_loc = [self.points[i] for i in selected_points]
        for loc in init_loc:
            self.board[loc] = np.random.choice([2, 4])
        reset_sound = pygame.mixer.Sound('Game2048/sound/reset.mp3')
        reset_sound.play()


class Score():
    def __init__(self, posx, posy):
        self.font = pygame.font.Font(None, 45)
        self.score = 0
        self.posx = posx
        self.posy = posy
        self.life = 5

    def draw(self, screen):
        count_dis = self.font.render(
            "Score: "+str(int(self.score)), False, (120, 53, 1))
        screen.blit(count_dis, (self.posx, self.posy))

    def update_count(self, score):
        self.score = score


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("2048")

    # sound
    pygame.mixer.init()
    sound_move = pygame.mixer.Sound("Game2048/sound/move.mp3")

    game_screen = pygame.surface.Surface((580, 580))
    game_screen.fill((255, 255, 255))

    # interactive button
    button = pygame.Rect(370, 60, 150, 40)
    button_color = (128, 118, 97)
    button_font = pygame.font.SysFont("Comic Sans", 20)

    font = pygame.font.Font(None, 55)
    score = Score(370, 20)
    cal = Cal(score)

    while True:
        screen.fill((255, 233, 179))
        screen.blit(game_screen, (10, 110))
        clock.tick(TICK)
        mouse_pos = pygame.mouse.get_pos()

        # text on screen
        text = font.render("2048", True, (77, 61, 24))
        screen.blit(text, [20, 20])

        # score on screen
        score.draw(screen)

        # board on screen
        cal.draw(screen)

        # button on screen
        if button.collidepoint(mouse_pos):
            button_color = (87, 80, 77)
        else:
            button_color = (128, 118, 97)
        pygame.draw.rect(screen, button_color, button, border_radius=10)
        button_text = button_font.render("Reset", True, (242, 236, 223))
        button_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_rect)

        pygame.display.update()
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    cal.update(2)
                elif event.key == K_RIGHT:
                    cal.update(0)
                elif event.key == K_UP:
                    cal.update(1)
                elif event.key == K_DOWN:
                    cal.update(3)
                sound_move.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    cal.reset()


if __name__ == "__main__":
    main()
