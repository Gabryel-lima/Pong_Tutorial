from settings import *

from sprite import Player, Ball, Opponent
from groups import AllSprites

from typing import Callable

def scaled_surface_percent(surf, percentage):
    """Return a scaled surface based on the percentage."""
    width, height = surf.get_size()
    new_width = int(width * percentage / 100)
    new_height = int(height * percentage / 100)
    return pygame.transform.scale(surf, (new_width, new_height))

class Game:
    def __init__(self):
        pygame.init()

        # display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # scaled surface
        self.scaled = scaled_surface_percent(self.screen, percentage=10)
        
        self.icon = pygame.image.load(join('assets', 'icon.png'))
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Pong_Tutorial')

        # time
        self.clock = pygame.time.Clock()
        self.runing = True

        # score
        self.load_score(reset=False)
        self.score = {'player': 0, 'opponent': 0}

        # sprites
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()

        # classes
        self.ball = Ball((self.all_sprites), paddle_sprites=self.paddle_sprites, update_score=self.update_score)
        self.player = Player((self.all_sprites, self.paddle_sprites), ball=self.ball)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), ball=self.ball)

        # font
        self.font = pygame.Font(None, 60)

    def background(self):
        self.screen.fill(COLORS['bg'])
        #pygame.draw.rect(self.screen, (127, 127, 127), (self.screen.get_frect()), 2) # border

    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.screen.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.screen.blit(opponent_surf, opponent_rect)

        # line separator
        pygame.draw.line(self.screen, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 5)

    def update_score(self, side: Callable[[str], None]):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def save_score(self):
        try:
            with open('data/score.json', 'w') as file:
                json.dump(self.score, file)

        except FileNotFoundError:
            os.makedirs('data')
            with open('data/score.json', 'w') as file:
                json.dump(self.score, file)

    def load_score(self, reset=False):
        try:
            if not reset:
                with open('data/score.json', 'r') as file:
                    self.score = json.load(file)
        except FileNotFoundError:
            self.score = {'player': 0, 'opponent': 0}
            self.save_score()

    def reset_game(self):
        self.load_score(reset=True)

    def _render_game(self):
        while self.runing:
            dt = self.clock.tick(FPS) / 1000 # Divide por 1000 para converter milissegundos em segundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.background()
            self.display_score()
            self.all_sprites.draw()

            # update display
            pygame.display.update()

            # return frame
            return np.array(pygame.surfarray.array3d(self.scaled), dtype=np.float32)
        
        pygame.quit()

    def run(self):
        while self.runing:
            dt = self.clock.tick(FPS) / 1000 # seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False
                    self.save_score()

            # update
            self.all_sprites.update(dt)

            # draw
            self.background()
            self.display_score()
            self.all_sprites.draw()

            # update display
            pygame.display.update()
        pygame.quit()

def main():
    Game().run()

if __name__ == '__main__':
    main()
