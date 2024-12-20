from settings import *
from random import choice, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # image
        self.image = pygame.Surface(SIZE['paddle'])
        self.image.fill(COLORS['paddle'])

        # rect & movement
        self.rect = self.image.get_frect(center = (POS['player']))
        self.direction = 0
        self.speed = SPEED['player']

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN] - keys[pygame.K_UP]) 

    def update(self, dt):
        self.get_direction()
        self.move(dt)

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # image
        self.image = pygame.Surface(SIZE['ball'])
        self.image.fill(COLORS['ball'])

        # rect & movement
        self.rect = self.image.get_frect(center = (POS_BALL['ball']))
        self.direction = pygame.Vector2(x=choice((-1, 1)), y=uniform(0.4, 0.8) * choice((1, -1)))
        self.speed = SPEED['ball']

    def move(self, dt):
        self.rect.center += self.direction * SPEED['ball'] * dt
        # self.direction.x += self.direction * self.speed * dt
        # self.direction.y += self.direction * self.speed * dt

    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        if self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.direction.x *= -1

        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1

    def update(self, dt):
        self.move(dt)
        self.wall_collision()