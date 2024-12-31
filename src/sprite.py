from settings import *
from random import choice, uniform

from typing import Callable

class Paddle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        # image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)

        # shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)

        # rect & movement
        self.rect = self.image.get_frect(center = (POS['player']))
        self.old_rect = self.rect.copy()
        self.direction = 0
        self.speed = SPEED['player']

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

    def reset(self):
        self.rect.center = POS['player'] or POS['opponent'] or POS['ai']

class Opponent(Paddle):
    def __init__(self, *groups, ball):
        super().__init__(*groups)

        # rect & movement
        self.speed = SPEED['opponent']
        self.rect.center = POS['opponent']

        # reference
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
    
    def reset(self):
        self.rect.center = POS['opponent']

class AiAgent(Paddle):
    def __init__(self, *groups, ball):
        super().__init__(*groups)

        # reference
        self.ball = ball

        # rect & movement
        self.speed = SPEED['ai']
        self.rect.center = POS['ai']

    def get_direction(self, action=None):
        if action is not None:
            self.rect.centery += action * self.speed
        # else:
        #     self.rect.centery += 1 if self.ball.rect.centery > self.rect.centery else -1

    def reset(self):
        self.rect.center = POS['opponent']

class Player(Paddle):
    def __init__(self, *groups, ball):
        super().__init__(*groups)

        # # rect & movement
        # self.speed = SPEED['opponent']
        # self.rect.center = POS['opponent']

        # reference
        self.ball = ball

    def get_direction(self):
        # keys = pygame.key.get_pressed()
        # self.direction = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        # -------------------------------------------------------------- #

        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
    
    def reset(self):
        self.rect.center = POS['player']

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups, paddle_sprites, update_score: Callable[[str], None]):
        super().__init__(*groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        # image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0] / 2)

        # shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0] / 2)

        # rect & movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(x=choice((-1, 1)), y=uniform(0.4, 0.8) * choice((1, -1)))

        # timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1200
        self.speed_modifier = 0

    def get_distance(self, paddle):
        return self.rect.centerx - paddle.rect.centerx

    def move(self, dt):
        self.rect.x += self.direction.x * SPEED['ball'] * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.y += self.direction.y * SPEED['ball'] * dt * self.speed_modifier 
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def wall_collision(self):
        # top
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        # bottom
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        # out of bounds
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            scorer = 'player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent'
            self.update_score(scorer)
            self.reset()

        # if self.rect.right >= WINDOW_WIDTH:
        #    self.rect.right = WINDOW_WIDTH
        #    self.direction.x *= -1

        # if self.rect.left <= 0:
        #     self.reset()
        #    self.rect.left = 0
        #    self.direction.x *= -1

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2 + 1, WINDOW_HEIGHT / 2) # +1 ajustar a pos da bolinha na linha
        self.direction = pygame.Vector2(x=choice((-1, 1)), y=uniform(0.4, 0.8) * choice((1, -1)))
        self.start_time = pygame.time.get_ticks()

    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(dt)
        self.wall_collision()
