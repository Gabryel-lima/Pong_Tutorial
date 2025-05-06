
# Pong Tutorial

Este projeto é um tutorial de como criar um jogo de Pong utilizando Python e Pygame. Além disso, ele inclui um agente de aprendizado por reforço que joga o jogo utilizando um algoritmo evolutivo.

## Estrutura do Projeto

- `data/`: Contém arquivos de dados, como pontuações.
- `src/`: Contém o código principal do projeto, incluindo o ambiente personalizado, agentes e utilitários.
- `requirements.txt`: Lista de dependências do projeto.

## (work_in_progress)
### $ Recomendo utilizar o python3.11.9 por conta do tensorflow
### $ Se você não tiver gpu Nvidea ou sem instrução AVX2, FMA. Para o tensorflow-cpu. 

### $ Vou deixar o modelo pré-treinado do tflitle, e mais para frente vou trazer a versão sem dependência da lib.

## Dependências
Para instalar as dependências, execute:

- Se você estiver pelo Linux este arquivo setup.sh vai facilitar a criação do .venv 
- A versão usada do interpretador para o game é Python3.10.16
```bash
chmod +x ./setup.sh && ./setup.sh
```

## Executando o Jogo

Para executar o jogo Pong, navegue até o diretório `src` e execute o arquivo `Pong.py`:

```bash
python src/Pong.py
```

## Treinando o Agente

Para treinar o agente de aprendizado por reforço, execute o arquivo `EvolutionaryAgent.py`:

```bash
python src/model/EvolutionaryAgent.py
```

## Estrutura do Código

### `src/Pong.py`

Contém a lógica principal do jogo Pong, incluindo a inicialização do jogo, atualização de sprites e renderização.

### `src/model/CustomPyEnv.py`

Define um ambiente personalizado para o agente de aprendizado por reforço interagir com o jogo Pong.

### `src/model/EvolutionaryAgent.py`

Implementa um agente de aprendizado por reforço utilizando um algoritmo evolutivo para treinar um modelo que joga Pong.

### `src/settings.py`

Contém configurações e constantes utilizadas em todo o projeto, como dimensões da janela, cores e velocidades.

### `src/sprite.py`

Define as classes de sprites utilizadas no jogo, como `Paddle`, `Ball` e `Particles`.

### `src/groups.py`

Define grupos de sprites personalizados para gerenciar e desenhar sprites na tela.

## Contribuição

Sinta-se à vontade para abrir issues e pull requests para contribuir com melhorias e correções.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
