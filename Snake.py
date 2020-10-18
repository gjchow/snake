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
    def __init__(self):
        self.body = [(0, 0)]
        self.head = 0, 0

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
                colour = (0, 200, 0)
            else:
                colour = (0, 255, 0)
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
        direction = 1
        s = Snake()
        f = Food()
        check = False
        save = 0
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
                pygame.time.delay(200)
                clock.tick(30)


if __name__ == "__main__":
    game = Game()
    game.run()


