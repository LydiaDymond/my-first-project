import pygame
import random
import sys
from pygame.locals import *

# 初始化颜色
COLORS = [
    (0, 0, 0),        # 黑色（背景）
    (120, 37, 179),   # 紫色
    (100, 179, 179),  # 青色
    (80, 34, 22),     # 棕色
    (80, 134, 22),    # 绿色
    (180, 34, 22),    # 红色
    (180, 34, 122),   # 粉色
]

# 方块形状
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 2, 5, 6]],  # O
    [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[4, 5, 9, 10], [2, 6, 5, 9]]  # Z
]

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.figure = None
        self.next_figure = None
        self.level = 1
        self.lines = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure_x = 0
        self.figure_y = 0
        
        # 初始化游戏区域
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        if not self.next_figure:
            self.next_figure = Figure(3, 0)
        self.figure = self.next_figure
        self.next_figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                       j + self.figure.x > self.width - 1 or \
                       j + self.figure.x < 0 or \
                       self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1-1][j]
        self.score += lines ** 2
        self.lines += lines
        self.level = self.lines // 10 + 1

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self):
        return SHAPES[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

def main():
    pygame.init()
    size = (400, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("俄罗斯方块")

    # 初始化游戏
    game = Tetris(20, 10)
    counter = 0
    pressing_down = False
    paused = False

    # 设置字体
    font = pygame.font.SysFont('SimHei', 25, True, False)
    font1 = pygame.font.SysFont('SimHei', 65, True, False)

    # 游戏主循环
    while True:
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (50 // game.level) == 0 or pressing_down:
            if game.state == "start" and not paused:
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    paused = not paused
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(COLORS[0])

        # 绘制游戏区域
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, COLORS[game.field[i][j]],
                               [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 0)

        # 绘制当前方块
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, COLORS[game.figure.color],
                                       [game.x + game.zoom * (j + game.figure.x),
                                        game.y + game.zoom * (i + game.figure.y),
                                        game.zoom, game.zoom], 0)

        # 绘制下一个方块预览
        if game.next_figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, COLORS[game.next_figure.color],
                                       [game.x + game.zoom * (j + 3),
                                        game.y + game.zoom * (i + 1),
                                        game.zoom, game.zoom], 0)

        # 绘制分数和等级
        text = font.render("分数: " + str(game.score), True, (255, 255, 255))
        screen.blit(text, [0, 0])
        text = font.render("等级: " + str(game.level), True, (255, 255, 255))
        screen.blit(text, [0, 30])
        text = font.render("行数: " + str(game.lines), True, (255, 255, 255))
        screen.blit(text, [0, 60])

        # 游戏结束显示
        if game.state == "gameover":
            game_over_text = font1.render("游戏结束!", True, (255, 255, 255))
            screen.blit(game_over_text, [20, 200])

        # 暂停显示
        if paused:
            pause_text = font1.render("已暂停", True, (255, 255, 255))
            screen.blit(pause_text, [20, 200])

        pygame.display.flip()

if __name__ == '__main__':
    main() 