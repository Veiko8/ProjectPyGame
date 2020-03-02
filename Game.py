import pygame
import random
import os

pygame.init()

size = (1200, 400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

dim = 10
mines = 10


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 5
        self.top = 5
        self.cell_size = 40

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0), (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 \
                or cell_x >= self.width \
                or cell_y < 0 \
                or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        pass


class Sweaper(Board):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        self.proigrich = False
        self.board = [[-1] * width for _ in range(height)]
        i = 0
        self.ochki1 = 0
        self.ochki2 = 0
        self.colichestvo_hodov = 1
        self.vivod = ""
        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                i += 1

    def open_cell(self, cell):
        x, y = cell
        if self.board[y][x] == 10:
            self.proigrich = True
            return
        if self.board[y][x] != -1:
            return
        s = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if self.board[y + dy][x + dx] == 10:
                    s += 1
                    if self.colichestvo_hodov != 0:
                        if self.colichestvo_hodov % 2 == 0:
#                           очки2 то есть ходы первого игрока
                            self.ochki2 += 1
                            break
                        else:
#                       очки1 то есть ходы второго игрока
                            self.ochki1 += 1
        self.board[y][x] = s

    def on_click(self, cell):
        self.open_cell(cell)
        if self.proigrich == False:
            self.colichestvo_hodov += 1
        else:
            self.colichestvo_hodov = 0

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 10 and self.proigrich:
                    pygame.draw.rect(screen, pygame.Color("red"), (
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size, self.cell_size))

                    if self.ochki1 < self.ochki2:
                        self.vivod = "Победил второй игрок!"
                    elif self.ochki1 > self.ochki2:
                        self.vivod = "Победил первый игрок!"
                    elif self.ochki1 == self.ochki2:
                        self.vivod = "Победила дружба!"
                    else:
                        self.vivod = "Ошибка. Попробуйте ещё!"

                    font = pygame.font.Font(None, 70)
                    text = font.render(self.vivod, 1, (253, 244, 227))
                    screen.blit(text, (530, 330))

                if self.board[y][x] >= 0 and self.board[y][x] != 10:
                    if self.colichestvo_hodov % 2 == 0:
                        font = pygame.font.Font(None, self.cell_size - 6)
                        text = font.render(str(self.board[y][x]),
                                           1, (255, 0, 0))
                        screen.blit(text, (x * self.cell_size + self.left + 3,
                                           y * self.cell_size + self.top + 3))
                    else:
                        font = pygame.font.Font(None, self.cell_size - 6)
                        text = font.render(str(self.board[y][x]),
                                           1, (0, 255, 0))
                        screen.blit(text, (x * self.cell_size + self.left + 3,
                                           y * self.cell_size + self.top + 3))

                    font = pygame.font.Font(None, 150)
                    text = font.render(str(self.ochki1), 1, (253, 244, 227))
                    screen.blit(text, (650, 210))

                    font = pygame.font.Font(None, 150)
                    text = font.render(str(self.ochki2), 1, (253, 244, 227))
                    screen.blit(text, (880, 210))

                pygame.draw.rect(screen, (190, 245, 1),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

                font = pygame.font.Font(None, 50)
                text = font.render(str("Правила игры"), 1, (0, 255, 0))
                screen.blit(text, (670, 10))
                font = pygame.font.Font(None, 30)
                text = font.render(str("На поле заложено 10 мин. Игроки поочерёдно делают ходы. Чем больше"),
                                   1, (0, 0, 0))
                screen.blit(text, (410, 60))
                text = font.render(str("рядом с открытой клеткой мин, тем больше очков начисляется игроку. Если"),
                                   1, (0, 0, 0))
                screen.blit(text, (410, 90))
                text = font.render(str("выводится 0, значит в соседних клетках мин нет. Победит тот, кто наберёт"),
                                   1, (0, 0, 0))
                screen.blit(text, (410, 120))
                text = font.render(str("больше очков, прежде чем наткнётся на мину. Не нажимайте в клетку дважды."),
                                   1, (0, 0, 0))
                screen.blit(text, (410, 150))
                font = pygame.font.Font(None, 25)
                text = font.render(str("Удачи и приятной игры!!!"), 1, (0, 0, 255))
                screen.blit(text, (670, 180))
                font = pygame.font.Font(None, 30)
                text = font.render(str("Количесвто очков"), 1, (0, 0, 0))
                screen.blit(text, (410, 230))
                text = font.render(str("первого игрока"), 1, (0, 0, 0))
                screen.blit(text, (410, 270))
                text = font.render(str("Количесвто очков"), 1, (0, 0, 0))
                screen.blit(text, (1000, 230))
                text = font.render(str("второго игрока"), 1, (0, 0, 0))
                screen.blit(text, (1000, 270))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((255, 255, 255))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
cursor = pygame.sprite.Sprite(all_sprites)
cursor.image = pygame.transform.scale(load_image("arrow.png"), (50, 50))
cursor.rect = cursor.image.get_rect()


pygame.mouse.set_visible(False)
board = Sweaper(dim, dim, mines)
board.set_view(0, 0, min(size) // dim)
time_on = False
ticks = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not board.proigrich:
            board.get_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos
    screen.fill((42, 92, 3))
    if pygame.mouse.get_focused():
        all_sprites.draw(screen)
    board.render()
    pygame.display.flip()
    clock.tick(10)
    ticks += 1

pygame.quit()
