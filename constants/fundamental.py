from ..dimensions import Frequency, Speed, ElectricCharge, Entropy, SubstanceAmount, Planck, Newton

# https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf/2d2b50bf-f2b4-9661-f402-5f9d66e4b507
# https://web.archive.org/web/20181119214326/https://www.bipm.org/utils/common/pdf/CGPM-2018/26th-CGPM-Resolutions.pdf
# https://web.archive.org/web/20210204120336/https://www.bipm.org/en/CGPM/db/26/1/
# https://www.nist.gov/si-redefinition/meet-constants
# https://web.archive.org/web/20201204121811/https://www.bipm.org/utils/common/pdf/CIPM-PV-OCR/CIPM1997.pdf

# https://en.wikipedia.org/wiki/Cesium_clock
CESIUM_133_HYPERFINE_TRANSITION_FREQUENCY = Frequency(9192631770, 'Hz', precision=0)

# https://en.wikipedia.org/wiki/Speed_of_light
CELERITY = Speed(299792458, 'm sec-1', precision=0)

# https://en.wikipedia.org/wiki/Planck_constant
# https://physics.nist.gov/cgi-bin/cuu/Value?h
PLANCK_CONSTANT = Planck(6.62607015e-34, 'kg m2 sec-1', significant_digits=9)

# https://en.wikipedia.org/wiki/Elementary_charge
ELEMENTARY_CHARGE = ElectricCharge(1.602176634e-19, 'A sec', significant_digits=10)

# https://en.wikipedia.org/wiki/Boltzmann_constant
BOLTZMANN_CONSTANT = Entropy(1.380649e-23, 'J K-1', significant_digits=7)

# https://en.wikipedia.org/wiki/Avogadro_constant
AVOGADRO_CONSTANT = ~SubstanceAmount(6.02214076e23, 'mol-1', significant_digits=9)

# https://en.wikipedia.org/wiki/Gravitational_constant
# https://physics.nist.gov/cgi-bin/cuu/Value?bg
GRAVITATIONAL_CONSTANT = Newton(6.6743e-11, 'm3 kg−1 sec−2', significant_digits=5)
