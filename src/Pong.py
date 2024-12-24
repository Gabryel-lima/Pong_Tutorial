from settings import *
from sprite import Player, Ball, Opponent
from groups import AllSprites
import json

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
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball((self.all_sprites), paddle_sprites=self.paddle_sprites, update_score=self.update_score)
        Opponent((self.all_sprites, self.paddle_sprites), ball=self.ball)

        # score
        #self.score = {'player': 0, 'opponent': 0}
        self.load_score()
        self.font = pygame.Font(None, 60)

    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        # line separator
        pygame.draw.line(self.display_surface, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 5)

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def save_score(self):
        with open('data/score.json', 'w') as file:
            json.dump(self.score, file)

    def load_score(self):
        try:
            with open('data/score.json', 'r') as file:
                self.score = json.load(file)
        except:
            self.score = {'player': 0, 'opponent': 0}

    def run(self):
        while self.runing:
            dt = self.clock.tick(60) / 1000 # Divide por 1000 para converter milissegundos em segundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False
                    self.save_score()

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.draw()
            pygame.display.update()
        pygame.quit()

def main():
    Game().run()

if __name__ == '__main__':
    main()
