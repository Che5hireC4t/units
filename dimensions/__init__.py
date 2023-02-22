"""
This submodule contains all the dimension class.
To import specific dimensions, do:
>>> from dimensions import Time, ElectricCharge

To import all dimensions, do:
>>> from dimensions import *

Here are the supported dimensions:



███████╗ ██╗   ██╗ ███╗   ██╗ ██████╗   █████╗  ███╗   ███╗ ███████╗ ███╗   ██╗████████╗ █████╗  ██╗
██╔════╝ ██║   ██║ ████╗  ██║ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██╔════╝ ████╗  ██║╚══██╔══╝██╔══██╗ ██║
█████╗   ██║   ██║ ██╔██╗ ██║ ██║  ██║ ███████║ ██╔████╔██║ █████╗   ██╔██╗ ██║   ██║   ███████║ ██║
██╔══╝   ██║   ██║ ██║╚██╗██║ ██║  ██║ ██╔══██║ ██║╚██╔╝██║ ██╔══╝   ██║╚██╗██║   ██║   ██╔══██║ ██║
██║      ╚██████╔╝ ██║ ╚████║ ██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ███████╗ ██║ ╚████║   ██║   ██║  ██║ ███████╗
╚═╝       ╚═════╝  ╚═╝  ╚═══╝ ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚══════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚══════╝

Time
Mass
Length
Temperature
SubstanceAmount
ElectricCurrent
LightIntensity



 ██████╗ ██████╗  ███╗   ███╗ ██████╗  ██████╗  ███████╗ ███████╗██████╗
██╔════╝██╔═══██╗ ████╗ ████║ ██╔══██╗██╔═══██╗ ██╔════╝ ██╔════╝██╔══██╗
██║     ██║   ██║ ██╔████╔██║ ██████╔╝██║   ██║ ███████╗ █████╗  ██║  ██║
██║     ██║   ██║ ██║╚██╔╝██║ ██╔═══╝ ██║   ██║ ╚════██║ ██╔══╝  ██║  ██║
╚██████╗╚██████╔╝ ██║ ╚═╝ ██║ ██║     ╚██████╔╝ ███████║ ███████╗██████╔╝
 ╚═════╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝      ╚═════╝  ╚══════╝ ╚══════╝╚═════╝

Acceleration
Conductivity
Density / VolumetricMass
Dobson
ElectricCharge
Energy
Entropy
Force
Frequency
MassFlow
MolarMass
Newton
Planck
Power
Pressure
Resistivity
Speed
SubstanceFlow
Surface
Voltage
Volume
VolumetricFlow
"""

# Fondamental dimensions:
from .Time import Time
from .Mass import Mass
from .Length import Length
from .Temperature import Temperature
from .SubstanceAmount import SubstanceAmount
from .ElectricCurrent import ElectricCurrent
from .LightIntensity import LightIntensity

# Composed dimensions
from .Surface import Surface
from .Volume import Volume
from .Frequency import Frequency
from .Speed import Speed
from .Acceleration import Acceleration
from .MolarMass import MolarMass
from .Density import Density, VolumetricMass
from .VolumetricFlow import VolumetricFlow
from .MassFlow import MassFlow
from .SubstanceFlow import SubstanceFlow
from .Energy import Energy
from .Entropy import Entropy
from .Pressure import Pressure
from .Dobson import Dobson
from .ElectricCharge import ElectricCharge
from .Power import Power
from .Voltage import Voltage
from .Resistivity import Resistivity
from .Conductivity import Conductivity
from .Planck import Planck
from .Newton import Newton
from .Force import Force

from ._NullDimension import _NullDimension
from .AbstractQuantity import AbstractQuantity
