import pygame
import numpy as np
from model.utils import lerp, get_rgba, draw_dashed_line

class Visualizer:
    def __init__(self):
        self.dash_offset = 0

    def update(self):
        self.dash_offset = (self.dash_offset + 0.05) % 1  # Speed of the dash movement

    def draw_network(self, screen, model):
        margin = 50
        left, top = margin, margin
        width, height = screen.get_width() - margin * 2, screen.get_height() - margin * 2
        level_height = height / len(model.layers)
        
        for i in range(len(model.layers) - 1, -1, -1):
            level_top = top + lerp(height - level_height, 0, 0.5 if len(model.layers) == 1 else i / (len(model.layers) - 1))
            output_labels = ['↑', '•', '↓'] if i == len(model.layers) - 1 else []
            self.draw_level(screen, model.layers[i], left, level_top, width, level_height, output_labels)

    def draw_level(self, screen, layer, left, top, width, height, output_labels):
        right, bottom = width + left, height + top

        try:
            weights, biases = layer.get_weights()
        except ValueError:
            return  # Ignore layers without weights (e.g., Dropout)

        inputs, outputs = weights.shape[0], weights.shape[1]
        self.draw_connections(screen, weights, inputs, outputs, left, right, top, bottom)
        self.draw_nodes(screen, inputs, outputs, weights, biases, left, right, top, bottom, output_labels)

        pygame.display.flip()

    def draw_connections(self, screen, weights, inputs, outputs, left, right, top, bottom):
        for i in range(inputs):
            for j in range(outputs):
                start_pos = self.get_node_x(inputs, i, left, right), bottom
                end_pos = self.get_node_x(outputs, j, left, right), top
                color = get_rgba(weights[i][j])
                draw_dashed_line(screen, color, start_pos, end_pos, 2, 10, self.dash_offset)

    def draw_nodes(self, screen, inputs, outputs, weights, biases, left, right, top, bottom, output_labels):
        node_radius, shadow_offset = 32, 4

        for i in range(inputs):
            x = self.get_node_x(inputs, i, left, right)
            self.draw_node(screen, x, bottom, node_radius, shadow_offset, get_rgba(weights[i][0])[:3])

        for i in range(outputs):
            x = self.get_node_x(outputs, i, left, right)
            self.draw_node(screen, x, top, node_radius, shadow_offset, get_rgba(weights[0][i])[:3], get_rgba(biases[i])[:3])
            if output_labels and output_labels[i]:
                self.draw_label(screen, output_labels[i], x, top, node_radius)

    def draw_node(self, screen, x, y, radius, shadow_offset, color, border_color=None):
        pygame.draw.circle(screen, (0, 33, 48), (x + shadow_offset, y + shadow_offset), radius) # shadow
        pygame.draw.circle(screen, (0, 0, 0), (x, y), radius) # node
        pygame.draw.circle(screen, color, (x, y), int(radius * 0.6)) # activation
        if border_color:
            pygame.draw.circle(screen, border_color, (x, y), int(radius * 0.8), 2) # border

    def draw_label(self, screen, label, x, y, radius):
        font = pygame.font.SysFont('Calibri', int(radius))
        text_surface = font.render(label, True, (206, 17, 38))
        text_rect = text_surface.get_rect(center = (x, y))
        screen.blit(text_surface, text_rect)

    @staticmethod
    def get_node_x(nodes, index, left, right):
        return lerp(left, right, 0.5 if nodes == 1 else index / (nodes - 1))
