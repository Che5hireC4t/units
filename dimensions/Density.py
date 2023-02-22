from .AbstractQuantity import AbstractQuantity, DimensionalArray


class Density(AbstractQuantity):
    """
    VolumetricMass is an alias for Density

    Supported units: all supported Length units ^-3 over all supported Mass units:
    >>> Density(1.0, "g m-3")
    >>> Density(1.0, "oz in-3")
    etc...

    https://en.wikipedia.org/wiki/Density
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=-3)


VolumetricMass = Density
