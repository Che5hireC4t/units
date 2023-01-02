from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Mass(AbstractQuantity):
    """
    Supported units (From smallest to biggest):

    Gram        g       Mass(1.0, "g")      https://en.wikipedia.org/wiki/Gram
    Ounce       oz      Mass(1.0, "oz")     https://en.wikipedia.org/wiki/Ounce
    Pound       lb      Mass(1.0, "lb")     https://en.wikipedia.org/wiki/Pound_(mass)
    Ton         t       Mass(1.0, "t")      https://en.wikipedia.org/wiki/Ton

    https://en.wikipedia.org/wiki/Mass
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1)
    _UNITS = \
        {
            Unit('g', 'gram', 0.001): 0.001,  # https://en.wikipedia.org/wiki/Gram
            Unit('oz', 'ounce', 0.028349523125): 0.028349523125,  # https://en.wikipedia.org/wiki/Ounce
            Unit('lb', 'pound', 0.45359237): 0.45359237,  # https://en.wikipedia.org/wiki/Pound_(mass)
            Unit('t', 'ton', 1000.0): 1000.0  # https://en.wikipedia.org/wiki/Ton
        }
