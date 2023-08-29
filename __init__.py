from sys import path
from os.path import dirname

# This is just a memo for myself in order to handle versioning properly:
# https://betterprogramming.pub/why-versioning-is-important-and-how-to-do-it-686ce13b854f?gi=81d210140bbf
__version__ = '1.0.3'

__here_path = dirname(__file__)
path.append(__here_path) if __here_path not in path else None

from .dimensions import *
from .constants import *
