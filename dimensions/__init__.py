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
from dimensions.Time import Time
from dimensions.Mass import Mass
from dimensions.Length import Length
from dimensions.Temperature import Temperature
from dimensions.SubstanceAmount import SubstanceAmount
from dimensions.ElectricCurrent import ElectricCurrent
from dimensions.LightIntensity import LightIntensity

# Composed dimensions
from dimensions.Surface import Surface
from dimensions.Volume import Volume
from dimensions.Frequency import Frequency
from dimensions.Speed import Speed
from dimensions.Acceleration import Acceleration
from dimensions.MolarMass import MolarMass
from dimensions.Density import Density, VolumetricMass
from dimensions.VolumetricFlow import VolumetricFlow
from dimensions.MassFlow import MassFlow
from dimensions.SubstanceFlow import SubstanceFlow
from dimensions.Energy import Energy
from dimensions.Entropy import Entropy
from dimensions.Pressure import Pressure
from dimensions.Dobson import Dobson
from dimensions.ElectricCharge import ElectricCharge
from dimensions.Power import Power
from dimensions.Voltage import Voltage
from dimensions.Resistivity import Resistivity
from dimensions.Conductivity import Conductivity
from dimensions.Planck import Planck
from dimensions.Newton import Newton
from dimensions.Force import Force

from dimensions._NullDimension import _NullDimension
