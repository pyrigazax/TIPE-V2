import sys
from pathlib import Path
sys.path.append(r'c:\users\maxou\appdata\local\packages\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\localcache\local-packages\python39\site-packages')
sys.path.append(Path(__file__).parent)
sys.path.append("\\".join(str(Path(__file__).parent).split("\\")[:-1]))
import pygame
import os
os.chdir(Path(__file__).parent)


from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
