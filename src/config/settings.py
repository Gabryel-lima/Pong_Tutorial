WINDOW_WIDTH, WINDOW_HEIGHT = (700, 540) 

SIZE = {'paddle': (18, 70), 
        'ball': (16, 16)} # Um circulo não precisa de um tamanho em x e y em seu desenho na tela, apenas um valor de raio. Mas para manter a consistência com o paddle, foi mantido.

POS = {'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 
        'opponent': (50, WINDOW_HEIGHT / 2), 
        'ai': (50, WINDOW_HEIGHT / 2)}

SPEED = {'player': 115, 
        'opponent': 115, 
        'ai': 20, 
        'ball': 190}

FPS = 60

COLORS = {
    'paddle': '#ee322c',
    'paddle shadow': '#b12521',
    'ball': '#ee622c',
    'ball shadow': '#000000',
    'bg': '#002633',
    'bg detail': '#004a63',
    'particle': '#ee322c',
}

__all__ = [
    'WINDOW_WIDTH',
    'WINDOW_HEIGHT',
    'SIZE',
    'POS',
    'SPEED',
    'FPS',
    'COLORS'
]
