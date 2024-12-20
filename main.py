import pygame

# inicialização do pygame
pygame.init()

# Configurando a janela
WINDOW_WIDTH, WINDOW_HEIGHT = (700, 540) # Entre (VGA) e (SVGA)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#clock = pygame.time.Clock()

runing = True
while runing:
    # loop de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    # desenhando o jogo 
    

pygame.quit()
