from settings import *
from sprite import Player, Ball

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.icon = pygame.image.load(file=join('assets', 'icon.png'))
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Pong_Tutorial')
        self.clock = pygame.time.Clock()
        self.runing = True

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        #self.ball_sprite = pygame.sprite.Group()

        # classes
        self.player = Player(self.all_sprites, self.paddle_sprites)
        self.ball = Ball(self.all_sprites, paddle_sprites=self.paddle_sprites)

    def run(self):
        while self.runing:
            dt = self.clock.tick(60) / 1000 # Divide por 1000 para converter milissegundos em segundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['bg'])
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()

    def collisions(self):
        pass

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
