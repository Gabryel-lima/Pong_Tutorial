import keras
import tensorflow as tf

import numpy as np
import random

# import sys
# import os

from tf_agents.specs import BoundedArraySpec
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.trajectories import time_step as ts

import matplotlib.pyplot as plt

from model.Visualizer import Visualizer


class EvoAgent:
    def __init__(self, env, population_size: int = 50, num_generations: int = 100, 
                 mutation_rate: float = 0.1, elite_fraction: float = 0.2, set_seed: bool = True,
                 seed_np: int = None, seed_random: int = None, seed_tf: int = None):
        
        # population_size
        if population_size < 10:
            raise ValueError("O tamanho da população não pode ser menor que 10.")

        # environment
        self.env = env
        self.visualizer = Visualizer()

        # genetic algorithm
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.elite_fraction = elite_fraction

        # model
        self.input_shape = self.env.observation_spec().shape
        self.num_actions = self.env.action_spec().maximum - self.env.action_spec().minimum + 1
        
        # metrics
        self.population = []
        self.fitness_history = []
        
        # seeds
        self.seed_np, self.seed_random, self.seed_tf = self.set_seeds(set_seed, seed_np, seed_random, seed_tf)
        
        # initialize population
        self.init_population()
        self.model = None

    @staticmethod
    def set_seeds(set_seed=False, seed_np=None, seed_random=None, seed_tf=None) -> tuple:
        """set seeds for numpy, random and tensorflow."""
        if set_seed:
            seed_np = seed_np or 42
            seed_random = seed_random or 42
            seed_tf = seed_tf or 42
        else:
            seed_np = np.random.randint(1, 1e+6)
            seed_random = np.random.randint(1, 1e+6)
            seed_tf = np.random.randint(1, 1e+6)

        np.random.seed(seed_np)
        random.seed(seed_random)
        tf.random.set_seed(seed_tf)

        return seed_np, seed_random, seed_tf
    
    def visualize_individual(self, screen, model):
        if model is not None:
            self.visualizer.update()
            self.visualizer.draw_network(screen, model)

    def init_population(self) -> None:
        # y = ⨍(Wⅹ + b)

        for _ in range(self.population_size):
            model = self.create_model()
            self.population.append(model)

    def create_model(self):
        return keras.Sequential([
            keras.layers.Input(self.input_shape),
            keras.layers.Dense(self.num_actions, activation='relu'),
            keras.layers.Dense(self.num_actions, activation='tanh')])

    def get_individual(self, model) -> np.ndarray:
        # action_values = W₂ * relu(W₁ * state + b₁) + b₂

        total_reward = 0
        time_step = self.env.reset()

        while not time_step.is_last():
            state = time_step.observation
            self.visualize_individual(self.env.game.screen, model)
            action_values = model(np.expand_dims(state, axis=0), training=False)
            action_idx = int(np.argmax(action_values.numpy()[0]))
            action = action_idx - 1 # [0, 1, 2] -> [-1, 0, 1]
            time_step = self.env.step(action)
            total_reward += time_step.reward

        return total_reward

    def get_elite(self, fitnesses: np.ndarray) -> list:
        # elite_indices = np.argsort(fitnesses)[-num_elite:]

        num_elite = max(1, int(self.elite_fraction * self.population_size))
        elite_indices = np.argsort(fitnesses)[-num_elite:]
        elite = [self.population[i] for i in elite_indices]
        return elite

    def crossover(self, parent1: list, parent2: list) -> keras.Sequential:
        # chield = parent1 * mask + parent2 * (1 - mask)
        # w = np.where(mask, w1, w2)

        child = self.create_model()
        
        for i in range(len(child.layers)):
            weights_parent1 = parent1.layers[i].get_weights()
            weights_parent2 = parent2.layers[i].get_weights()

            new_weights = []

            for w1, w2 in zip(weights_parent1, weights_parent2):
                mask = np.random.rand(*w1.shape) > 0.5
                w = np.where(mask, w1, w2)
                new_weights.append(w)
            child.layers[i].set_weights(new_weights)

        return child

    def mutate(self, model) -> None:
        # W' = W + N(0, 0.1)
        # w += np.random.normal(0, 0.1, size=w.shape)

        for layer in model.layers:
            weights = layer.get_weights()

            new_weights = []
            for w in weights:
                if np.random.rand() < self.mutation_rate:
                    mutation = np.random.normal(0, 0.1, size=w.shape)
                    w += mutation
                new_weights.append(w)
            layer.set_weights(new_weights)

    def train(self) -> None:
        # fitness = sum(reward)

        best_fitness_overall: float = -np.inf 

        for generation in range(self.num_generations):
            fitnesses = []

            for individual in self.population:
                fitness = self.get_individual(individual)
                fitnesses.append(fitness)
                #self.visualize_individual(self.env.game.screen, individual)

            max_fitness = np.max(fitnesses)
            avg_fitness = np.mean(fitnesses)
            self.fitness_history.append(max_fitness)

            print(f"Geração {generation +1}/{self.num_generations} - Melhor Fitness: {max_fitness:.2f} - Fitness Médio: {avg_fitness:.2f}")
            
            best_index = np.argmax(fitnesses)
            if fitnesses[best_index] > best_fitness_overall:
                best_fitness_overall = fitnesses[best_index]
                self.model = self.population[best_index]

                print(f"Novo melhor modelo encontrado com fitness: {best_fitness_overall:.2f}")

            elite = self.get_elite(fitnesses)
            new_population = elite.copy()
            while len(new_population) < self.population_size:
                parents = random.sample(elite, 2)
                child = self.crossover(parents[0], parents[1])
                self.mutate(child)
                new_population.append(child)
            self.population = new_population

    def evaluate_best(self) -> None:
        if self.model is None:
            print("Nenhum modelo disponível para avaliação.")
            return
        
        best_individual = self.model
        fitness = self.get_individual(best_individual)
        print(f"Melhor Fitness: {fitness:.2f}")

    def save_best_model(self, filepath: str) -> None:
        if self.model is not None:
            self.model.save(filepath)
            print(f"Melhor modelo salvo em '{filepath}'")
        else:
            print("Nenhum modelo para salvar.")

    def save_best_model_tflite(self, filepath: str) -> None:
        if self.model is not None:
            converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
            tflite_model = converter.convert()

            with open(filepath, "wb") as f:
                f.write(tflite_model)

            print(f"Melhor modelo salvo em formato TFLite em '{filepath}'")
        else:
            print("Nenhum modelo para salvar.")

    def plot_fitness(self) -> None:
        plt.plot(self.fitness_history)
        plt.title('Histórico do Melhor Fitness')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.savefig('./train')
