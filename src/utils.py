# import pygame
# import tensorflow as tf
# import numpy as np
# import random
# import sys
# import os


# def scaled_surface_percent(surf, percentage):
#     """Return a scaled surface based on the percentage."""
#     width, height = surf.get_size()
#     new_width = int(width * percentage / 100)
#     new_height = int(height * percentage / 100)
#     return pygame.transform.scale(surf, (new_width, new_height))

# def set_seeds(set_seed=True, seed_np=None, seed_random=None, seed_tf=None) -> tuple:
#     """set seeds for numpy, random and tensorflow."""
#     if set_seed:
#         seed_np = seed_np if seed_np is not None else 42
#         seed_random = seed_random if seed_random is not None else 42
#         seed_tf = seed_tf if seed_tf is not None else 42
#     else:
#         seed_np = np.random.randint(1, 1e+6)
#         seed_random = np.random.randint(1, 1e+6)
#         seed_tf = np.random.randint(1, 1e+6)

#     np.random.seed(seed_np)
#     random.seed(seed_random)
#     tf.random.set_seed(seed_tf)

#     return seed_np, seed_random, seed_tf
