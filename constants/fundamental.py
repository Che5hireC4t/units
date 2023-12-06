from ..dimensions import Frequency, Speed, ElectricCharge, Entropy, SubstanceAmount, Planck, Newton

CESIUM_133_HYPERFINE_TRANSITION_FREQUENCY = Frequency(9192631770, 'Hz', precision=0)
CELERITY = Speed(299792458, 'm sec-1', precision=0)
PLANCK_CONSTANT = Planck(6.62607015e-34, 'kg m2 sec-1', significant_digits=9)
ELEMENTARY_CHARGE = ElectricCharge(1.602176634e-19, 'A sec', significant_digits=10)
BOLTZMANN_CONSTANT = Entropy(1.380649e-23, 'J K-1', significant_digits=7)
AVOGADRO_CONSTANT = ~SubstanceAmount(6.02214076e23, 'mol-1', significant_digits=9)  # https://en.wikipedia.org/wiki/Avogadro_constant
GRAVITATIONAL_CONSTANT = Newton(6.6743e-11, 'm3 kg−1 sec−2', significant_digits=5)
