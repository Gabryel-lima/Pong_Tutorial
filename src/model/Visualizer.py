import pygame
import numpy as np

class Visualizer:
    def __init__(self, node_radius=20, node_color=(0, 0, 255), 
                 pos_color=(0, 255, 0), neg_color=(255, 0, 0), 
                 margin=50):
        """
        Inicializa o visualizador com parâmetros configuráveis. TODO: Ainda falta configurar melhor a classe.
        """
        self.dash_offset = 0
        self.node_radius = node_radius
        self.node_color = node_color
        self.pos_color = pos_color
        self.neg_color = neg_color
        self.margin = margin

    def update(self, dt):
        """
        Atualiza o estado do visualizador, como o deslocamento do traço.
        """
        self.dash_offset += 0.05 * dt
        if self.dash_offset >= 1:
            self.dash_offset = 0

    def draw_network(self, screen, weights):
        """
        Desenha a rede neural na tela.
        """
        screen_width, screen_height = screen.get_size()
        num_layers = len(weights)
        layer_height = screen_height / (num_layers + 1)

        for i, layer_weights in enumerate(weights):
            num_nodes_in = layer_weights[0].shape[0]
            num_nodes_out = layer_weights[0].shape[1]
            node_spacing_in = screen_width / (num_nodes_in + 1)
            node_spacing_out = screen_width / (num_nodes_out + 1)

            for j in range(num_nodes_in):
                x_in = (j + 1) * node_spacing_in
                y_in = (i + 1) * layer_height
                pygame.draw.circle(screen, self.node_color, (int(x_in), int(y_in)), self.node_radius)

                for k in range(num_nodes_out):
                    x_out = (k + 1) * node_spacing_out
                    y_out = (i + 2) * layer_height
                    weight = layer_weights[0][j][k]
                    color = self.pos_color if weight > 0 else self.neg_color
                    pygame.draw.line(screen, color, (int(x_in), int(y_in)), (int(x_out), int(y_out)), 1)

            for k in range(num_nodes_out):
                x_out = (k + 1) * node_spacing_out
                y_out = (i + 2) * layer_height
                pygame.draw.circle(screen, self.node_color, (int(x_out), int(y_out)), self.node_radius)

    def draw_level(self, screen, level, left, top, width, height):
        """
        Desenha um nível da rede neural.
        """
        right = left + width
        bottom = top + height
        node_spacing = width / (len(level.outputs) + 1)
        
        # Desenhar conexões
        for i, input_value in enumerate(level.inputs):
            for j, output_value in enumerate(level.outputs):
                start_pos = (left + (i + 1) * node_spacing, top + height / 2)
                end_pos = (left + (j + 1) * node_spacing, bottom - height / 2)
                color = self.pos_color if level.weights[i][j] > 0 else self.neg_color
                pygame.draw.line(screen, color, start_pos, end_pos, 2)
        
        # Desenhar nós
        for i, input_value in enumerate(level.inputs):
            pos = (left + (i + 1) * node_spacing, top + height / 2)
            pygame.draw.circle(screen, self.node_color, pos, self.node_radius)
        
        for j, output_value in enumerate(level.outputs):
            pos = (left + (j + 1) * node_spacing, bottom - height / 2)
            pygame.draw.circle(screen, self.node_color, pos, self.node_radius)
