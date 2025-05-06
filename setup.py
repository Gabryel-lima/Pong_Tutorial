import sys
from cx_Freeze import setup, Executable

if sys.platform == 'win32':
    base = 'Win32GUI'  # Para Windows, use Win32GUI para não mostrar o console
else:
    base = None

build_options = {
    'packages': [],
    'include_files': ['sounds/', 'data/', 'src/', 
                      'src/sprite.py', 'src/groups.py', 'src/utils.py']
}

executables = [
        Executable(
            'src/Pong.py', base=base, 
            target_name='Pong', icon='./assets/icon.png'
    )
]

setup(
    name='Pong_Tutorial',
    version='1.0',
    description='Este projeto é um tutorial de como criar um jogo de Pong utilizando Python e Pygame. Além disso, ele inclui um agente de aprendizado por reforço que joga o jogo utilizando um algoritmo evolutivo.',
    options={'build_exe': build_options},
    executables=executables
)
