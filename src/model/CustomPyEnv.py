import keras
import tensorflow as tf
from tf_agents.specs import BoundedArraySpec
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.trajectories import time_step as ts

import numpy as np
import random
import pygame


class CustomPyEnvironment(PyEnvironment):
    """
    Custom CustomPyEnvironment para ser utilizado com agentes de aprendizado por reforço, onde um jogador deve interagir com uma bola e blocos.
    Esta classe implementa a lógica do jogo, observações, espaço de ações e recompensas.

    Attributes:
        render_mode (str): Modo de renderização do ambiente ('human' ou 'rgb_array').
        game (Game): Instância do jogo que contém a lógica principal.
    """
    __metadata__ = {"render_modes": ["human", "rgb_array"], "render_fps": 60} #TODO: Ainda não utilizado

    def __init__(self, game, render_mode: str = "human", seed: int = None):
        super().__init__()
        """
        Inicializa o ambiente personalizado.

        Args:
            game (Game): Instância do jogo que contém a lógica principal.
            render_mode (str, opcional): Define como o jogo deve ser renderizado ('human' ou 'rgb_array').
            seed (int, opcional): Define a semente para gerar resultados reprodutíveis.
        """

        # initialize game
        self.game = game

        # render mode
        self.render_mode = render_mode

        # define action space
        self._action_spec = BoundedArraySpec(shape=(), dtype=np.int32, minimum=-1, maximum=1, name="action")

        # define obs space
        self._observation_spec = BoundedArraySpec(
            shape=(2, ),
            dtype=np.float32, minimum=0.0, maximum=1.0, name="observation"
        )

        # total reward
        self.total_reward = 0.0

        # seed
        self.seed(seed) or np.random.randint(1, 1e+6)
            
    def seed(self, seed: int) -> None:
        """
        Define a semente para todos os geradores de números aleatórios utilizados (random, numpy, tensorflow).

        Args:
            seed (int): Valor da semente.
        """
        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)

    def action_spec(self) -> BoundedArraySpec:
        """ Retorna as especificações do espaço de ações. """
        return self._action_spec

    def observation_spec(self) -> BoundedArraySpec:
        """ Retorna as especificações do espaço de observação. """
        return self._observation_spec

    def _reset(self) -> ts.TimeStep:
        """
        Reinicia o ambiente para o estado inicial.

        Returns:
            ts.TimeStep: O estado inicial do ambiente após o reset.
        """
        obs = self.get_obs()
        return self._create_timestep(obs, ts.StepType.FIRST, 0.0, 1.0)

    def _step(self, action: int) -> ts.TimeStep:
        """
        Executa uma ação no ambiente.
    
        Args:
            action (int): Ação a ser tomada (0, 1).
    
        Returns:
            ts.TimeStep: O próximo estado do ambiente após a execução da ação.
        """
        self._apply_action(action)
        reward, done = self.calculate_reward(action)
        obs = self.get_obs()
    
        step_type = ts.StepType.MID if not done else ts.StepType.LAST
        discount = 1.0 if not done else 0.0

        return self._create_timestep(obs, step_type, reward, discount)

    def _create_timestep(self, obs, step_type, reward, discount) -> ts.TimeStep:
        """
        Cria um objeto TimeStep com os parâmetros fornecidos.

        Args:
            obs (np.ndarray): Observação do ambiente.
            step_type (ts.StepType): Tipo do passo (inicial, intermediário ou final).
            reward (float): Recompensa obtida.
            discount (float): Fator de desconto.

        Returns:
            ts.TimeStep: Estado representado como um TimeStep.
        """
        return ts.TimeStep(
            step_type=np.array(step_type, dtype=np.int32),
            reward=np.array(reward, dtype=np.float32),
            discount=np.array(discount, dtype=np.float32),
            observation=obs
        )

    def _apply_action(self, action: int) -> None:
        """
        Aplica a ação especificada ao jogador.

        Args:
            action (int): Ação a ser aplicada (-1 - mover para cima, 1 - mover para baixo).
        """
        self.game.agent.get_direction(action)
        #self.game.agent.move(pygame.time.get_ticks() / 1000)

    def calculate_reward(self, action: int) -> tuple[float, bool]:
        """
        Calcula a recompensa para o jogador com base na posição da bola e do jogador.

        Args:
            action (int): Ação tomada pelo jogador.

        Returns:
            tuple[float, bool]: Recompensa obtida e se o episódio terminou.
        """
        reward = 0.0
        done = False
        
        # Normalize distância
        max_distance = self.game.screen.width
        distance = self.game.ball.get_distance(self.game.agent) / max_distance

        # Penalidade se a bola passa pelo agente
        # if self.game.ball.rect.left < self.game.agent.rect.right:
        #     reward -= 4.0  # Penalidade maior
        #     done = True
        
        # TODO: O problema é a frequencia que o ep deve terminar. Deve terminar com mais frequência, exemplo; 
        # Vai sincronizar com o tempo de resposta do agente, em compensação. Isso é gambiarra. kkk
        if self.game.ball.rect.left > self.game.agent.rect.right:
            done = True

        # Recompensa significativa por colisão com a bola
        if self.game.agent.rect.colliderect(self.game.ball.rect):
            reward += 5.0  # Incentivo principal

        # Pequena penalidade incremental baseada na distância
        reward -= 0.1 * distance

        # Pequena recompensa por se aproximar da bola
        reward += 0.1 / (distance + 1)

        if done:
            #self.game.agent.reset()
            pass

        reward = max(-5.0, min(reward, 5.0))
        return reward, done

    def get_obs(self) -> np.ndarray:
        """
        Obtém a observação atual do ambiente.

        Returns:
            np.ndarray: A observação baseada na posição da bola y, posição do paddle do agente e velocidade da bola.
        """
        obs = self.game.run() / 255.0
        return obs

    def render(self, mode="human") -> np.ndarray:
        """
        Renderiza o estado atual do ambiente.

        Args:
            mode (str): Modo de renderização ('human' ou 'rgb_array').
        """
        if mode == "human":
            self.game.run()
            pygame.display.update()

        elif mode == "rgb_array":
            return np.array([self.game.agent.rect.y, self.game.ball.rect.y], dtype=np.float32)
        
        else:
            raise ValueError(f"Modo de renderização '{mode}' não suportado.")


    def close(self) -> None:
        """
        Fecha o ambiente e limpa todos os recursos.
        """
        pygame.quit()
