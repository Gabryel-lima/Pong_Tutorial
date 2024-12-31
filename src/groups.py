from settings import *

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

    def draw(self):
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)

class Particules_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.space_pressed = False

    def draw(self):
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.space_pressed = True  # Inicia a criação de partículas

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.space_pressed = False  # Para a criação de partículas

        if self.space_pressed:
            self.empty()

