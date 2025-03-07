from settings import *
from random import choice, uniform

from typing import Callable
from dataclasses import dataclass

@dataclass
class ParticleStages:
    count: int
    color: tuple
    burn_size: tuple
    lifetime: float

class Particles(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y, radius, color, lifetime=1.0):
        super().__init__(groups)

        # attributes
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.lifetime = lifetime

        # timer
        self.elapsed_time = 0
        self.creation_time = pygame.time.get_ticks()

        # image & rect
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_frect(center = (x, y))

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time > self.lifetime:
            self.kill()
        else:
            alpha = int(255 * (1 - self.elapsed_time / self.lifetime))
            self.image.fill((*self.color[:3], alpha), special_flags=pygame.BLEND_RGBA_MULT)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)

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

    def reset(self, position):
        self.rect.center = position

class Opponent(Paddle):
    def __init__(self, *groups, ball_sprites):
        super().__init__(groups)

        # rect & movement
        self.speed = SPEED['opponent']
        self.rect.center = POS['opponent']

        # reference
        self.ball = ball_sprites

    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
    
    def reset(self):
        super().reset(POS['opponent'])

class Agent(Paddle):
    def __init__(self, *groups, ball_sprites):
        super().__init__(groups)

        # reference
        self.ball = ball_sprites

        # rect & movement
        self.speed = SPEED['ai']
        self.rect.center = POS['ai']

    def get_direction(self, action=None):
        if action is not None:
            self.rect.centery += action * self.speed

    def reset(self):
        super().reset(POS['ai'])

class Player(Paddle):
    def __init__(self, *groups, ball_sprites):
        super().__init__(groups)

        # reference
        self.ball = ball_sprites

    def get_direction(self):
        # Player direction
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        # -------------------------------------------------------------- #

        # Agent direction
        # self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
    
    def reset(self):
        super().reset(POS['player'])

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups, 
                paddle_sprites: pygame.sprite.Group, 
                ball_sprites: pygame.sprite.Group,
                particules_sprites: pygame.sprite.Group,
                update_score: Callable[[str], dict[int, str]]):
        super().__init__(groups)

        # references
        self.paddle_sprites = paddle_sprites
        self.ball_sprite = ball_sprites
        self.particules_sprites = particules_sprites
        self.update_score = update_score

        # image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, 
                            COLORS['ball'], 
                            (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), 
                            SIZE['ball'][0] / 2)

        # shadow surf
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, 
                            COLORS['ball shadow'], 
                            (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), 
                            SIZE['ball'][0] / 2)

        # rect & movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()
        self.direction = pygame.Vector2(x=choice((-1, 1)), y=uniform(0.4, 0.8) * choice((1, -1))).normalize()

        # timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1200 # ms
        self.speed_modifier = 0

        # particle stages
        self.particle_stages = [
            (1.3, ParticleStages(0, (0, 0, 0), (0, 0), 0.0)),
            (1.8, ParticleStages(3, (170, 170, 170), (-3, 3), 0.2)),
            (2.4, ParticleStages(6, (210, 210, 0), (-4, 4), 0.3)),
            (float("inf"), ParticleStages(15, (255, 100, 0), (-5, 5), 0.4))
        ]

    def _get_particle_stage(self, speed):
        for threshold, stage in self.particle_stages:
            if speed <= threshold:
                return stage
        return self.particle_stages[-1][1] # if not stages, return final idx

    def _create_particles(self):
        speed = self.direction.length()
        stage = self._get_particle_stage(speed)

        for _ in range(stage.count):
            offset_x = np.random.randint(*stage.burn_size)
            offset_y = np.random.randint(*stage.burn_size)
            Particles(
                self.particules_sprites,
                x=self.rect.centerx + offset_x,
                y=self.rect.centery + offset_y,
                radius=self.get_radius(),
                color=stage.color,
                lifetime=stage.lifetime
            )

    def get_distance(self, paddle):
        dx = self.rect.centerx - paddle.rect.centerx
        dy = self.rect.centery - paddle.rect.centery
        return (dx**2 + dy**2) ** 0.5  # Distância Euclidiana
    
    def get_radius(self):
        return int(self.rect.width / 2)

    def move(self, dt):
        self.rect.x += self.direction.x * SPEED['ball'] * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.y += self.direction.y * SPEED['ball'] * dt * self.speed_modifier
        self.collision('vertical')

    def gradual_speed(self, scalar=0.1):
        return 1 + scalar * self.speed_modifier

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1 * self.gradual_speed()
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1 * self.gradual_speed()
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1 * self.gradual_speed()
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1 * self.gradual_speed()

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
        #     self.rect.left = 0
        #     self.reset()
            # self.direction.x *= -1 # quick left

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2) # A pos estava usadndo o tamanho da bola, o que fazia a bola sair um pouco do centro
        self.direction = pygame.Vector2(x=choice((-1, 1)), y=uniform(0.4, 0.8) * choice((1, -1))).normalize()
        self.start_time = pygame.time.get_ticks()

    def timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self._create_particles()
        self.move(dt)
        self.wall_collision()
