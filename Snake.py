import pygame
import random

pygame.init()
screen_width = 600
rows = 20
grid = screen_width // rows
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_width))
pygame.display.set_caption("Snake")
up = pygame.K_UP, pygame.K_w
down = pygame.K_DOWN, pygame.K_s
right = pygame.K_RIGHT, pygame.K_d
left = pygame.K_LEFT, pygame.K_a


class Food(object):
    def __init__(self):
        self.x = random.randint(0, rows-1)
        self.y = random.randint(0, rows-1)

    def draw(self):
        rect = pygame.Rect(self.x*grid, self.y*grid, grid, grid)
        pygame.draw.rect(screen, (255, 0, 0), rect)

    def remake(self):
        self.x = random.randint(0, rows-1)
        self.y = random.randint(0, rows-1)

    def pos(self) -> tuple:
        return self.x, self.y


class Snake(object):
    def __init__(self, x, y, colour):
        self.body = [(x, y)]
        self.head = x, y
        self.colour = colour

    def __len__(self):
        return len(self.body)

    def eat(self, food: Food) -> bool:
        if self.head == food.pos():
            return True
        return False

    def move(self, direction, food) -> bool:
        if direction == 1:
            self.head = self.body[0]
            self.head = (self.head[0] + 1, self.head[1])
            if self.head[0] > rows - 1:
                return False
        if direction == 2:
            self.head = self.body[0]
            self.head = (self.head[0], self.head[1] - 1)
            if self.head[1] < 0:
                return False
        if direction == 3:
            self.head = self.body[0]
            self.head = (self.head[0] - 1, self.head[1])
            if self.head[0] < 0:
                return False
        if direction == 4:
            self.head = self.body[0]
            self.head = (self.head[0], self.head[1] + 1)
            if self.head[1] > rows - 1:
                return False
        if direction != 0:
            if not self.eat(food):
                self.body.pop()
            self.body.insert(0, self.head)
        if self.body.count(self.head) == 2:
            return False
        return True

    def draw(self):
        for coord in self.body:
            if self.head == coord:
                colour = (int(self.colour[0]*0.8), int(self.colour[1]*0.8),
                          int(self.colour[2]*0.8))
            else:
                colour = self.colour
            rect = pygame.Rect(coord[0]*grid, coord[1]*grid, grid, grid)
            pygame.draw.rect(screen, colour, rect)


class Game:
    def __init__(self):
        self.done = False

    def game_over(self):
        self.done = True
        print("GAME OVER!")
        pygame.quit()

    def run(self):
        direction = 0
        s = Snake(0, 0, (0, 255, 0))
        f = Food()
        check = False
        save = 1
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if direction != 0:
                        save = direction
                        direction = 0
                    else:
                        direction = save
                if event.type == pygame.KEYDOWN and event.key in right:
                    if direction != 3 and direction != 0:
                        direction = 1
                if event.type == pygame.KEYDOWN and event.key in up:
                    if direction != 4 and direction != 0:
                        direction = 2
                if event.type == pygame.KEYDOWN and event.key in left:
                    if direction != 1 and direction != 0:
                        direction = 3
                if event.type == pygame.KEYDOWN and event.key in down:
                    if direction != 2 and direction != 0:
                        direction = 4
            while not check:
                if f.pos() in s.body:
                    f.remake()
                else:
                    check = True
            if s.eat(f):
                f.remake()
                check = False
            if not self.done:
                screen.fill((0, 0, 0))
            if not s.move(direction, f):
                self.game_over()
                self.done = True
            if not self.done:
                f.draw()
                s.draw()
                pygame.display.flip()
                pygame.time.delay(200-((len(s)-1)*10))
                clock.tick(60)


class GameTwo(Game):
    def run(self):
        d1 = 0
        s1 = Snake(0, 0, (0, 255, 0))
        d2 = 0
        s2 = Snake(rows - 1, rows - 1, (0, 0, 255))
        f = Food()
        check = False
        save1 = 1
        save2 = 3
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if d1 != 0:
                        save1 = d1
                        save2 = d2
                        d1 = 0
                        d2 = 0
                    else:
                        d1 = save1
                        d2 = save2
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if d1 != 3 and d1 != 0:
                        d1 = 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if d1 != 4 and d1 != 0:
                        d1 = 2
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if d1 != 1 and d1 != 0:
                        d1 = 3
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if d1 != 2 and d1 != 0:
                        d1 = 4
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    if d2 != 3 and d2 != 0:
                        d2 = 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    if d2 != 4 and d2 != 0:
                        d2 = 2
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    if d2 != 1 and d2 != 0:
                        d2 = 3
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    if d2 != 2 and d2 != 0:
                        d2 = 4
            while not check:
                if f.pos() in s1.body or f.pos() in s2.body:
                    f.remake()
                else:
                    check = True
            if s1.eat(f) or s2.eat(f):
                f.remake()
                check = False
            if s1.head in s2.body and s2.head in s1.body:
                print("Tie")
                self.game_over()
                self.done = True
            elif s1.head in s2.body:
                print("Player1 Loses")
                self.game_over()
                self.done = True
            elif s2.head in s1.body:
                print("Player2 Loses")
                self.game_over()
                self.done = True
            if not self.done:
                screen.fill((0, 0, 0))
            m1 = s1.move(d1, f)
            m2 = s2.move(d2, f)
            if not m1 and not m2:
                print("Tie")
                self.game_over()
                self.done = True
            elif not m1:
                print("Player1 Loses")
                self.game_over()
                self.done = True
            elif not m2:
                print("Player2 Loses")
                self.game_over()
                self.done = True
            if not self.done:
                f.draw()
                s1.draw()
                s2.draw()
                pygame.display.flip()
                pygame.time.delay(200)
                clock.tick(60)


if __name__ == "__main__":
    game = GameTwo()
    game.run()
