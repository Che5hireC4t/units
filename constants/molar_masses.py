from ..dimensions import MolarMass

PROTON = MolarMass(1.0072765, 'g mol-1')
NEUTRON = MolarMass(1.0086649, 'g mol-1')
ELECTRON = MolarMass(0.0005486, 'g mol-1')

# Atoms, sorted by weight
HYDROGEN = MolarMass(1.0080, 'g mol-1')
CARBON = MolarMass(12.011, 'g mol-1')
NITROGEN = MolarMass(14.007, 'g mol-1')
OXYGEN = MolarMass(15.999, 'g mol-1')
SULFUR = MolarMass(32.066, 'g mol-1')

# Molecules, sorted in alphabetical order
CARBON_DIOXIDE = CARBON + OXYGEN * 2
HYDROGEN_SULFIDE = SULFUR + HYDROGEN * 2
SULFUR_DIOXIDE = SULFUR + OXYGEN * 2
WATER = OXYGEN + HYDROGEN * 2
