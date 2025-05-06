from src.config.settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            for i in range(3):  # draw shadow
                self.screen.blit(sprite.shadow_surf, sprite.rect.topleft + pygame.Vector2(i, i))

        for sprite in self:  # draw sprite
            self.screen.blit(sprite.image, sprite.rect)

class Ball_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)

class Paddle_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

class Particules_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)

