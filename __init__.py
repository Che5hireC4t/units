from sys import path

__here_path = '/'.join(__file__.split('/')[:-1])
path.append(__here_path) if __here_path not in path else None

from units.dimensions import *
from units.constants import *
