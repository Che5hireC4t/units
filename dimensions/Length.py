from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Length(AbstractQuantity):
    """
    Supported units (From smallest to biggest):

    Meter                   m           Length(1.0, "m")
    Inch                    in          Length(1.0, "in")
    Foot                    ft          Length(1.0, "ft")
    Yard                    yd          Length(1.0, "yd")
    Flight Level            FL          Length(1.0, "FL")       # https://en.wikipedia.org/wiki/Flight_level
    Mile                    mil         Length(1.0, "mil")
    Nautical Mile           nmi         Length(1.0, "nmi")
    Astronomical Unit       au          Length(1.0, "au")
    Light Year              ly          Length(1.0, "ly")
    Parsec                  ps          Length(1.0, "ps")
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1)
    _UNITS = \
        {
            Unit('m', 'meter'): 1.0,
            Unit('in', 'inch'): 0.0254,
            Unit('ft', 'foot'): 0.3048,
            Unit('yd', 'yard'): 0.9144,
            Unit('FL', 'flight level'): 30.48,  # 1 FL = 100 ft = 30.48 m
            Unit('mil', 'mile'): 1609.344,
            Unit('nmi', 'nautical mile'): 1852.0,
            Unit('au', 'astronomical unit'): 149597870700.0,
            Unit('ly', 'light year'): 9460660000000000.0,
            Unit('ps', 'parsec'): 3.0856775814913673e16
        }
