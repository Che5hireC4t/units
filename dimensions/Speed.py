from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Speed(AbstractQuantity):
    """
    Supported units:

    Any unit of Length class optionally prefixed, followed by any unit of Time class
    optionally prefixed and obligatory suffixed by -1.

    Examples:
    >>> from units.dimensions import Speed
    >>> s1 = Speed(1, 'm sec-1')
    >>> s2 = Speed(1, 'km h-1')
    >>> s3 = Speed(1, 'mil h-1')
    >>> s4 = Speed(1, 'm My-1')  # Meters per million (Mega) of years.

    Additionally, the following shortcuts are also supported

    Mile per hour               mph         Speed(1.0, "mph")
    Nautical mile per hour      knot        Speed(1.0, "knot")      https://en.wikipedia.org/wiki/Knot_(unit)

    https://en.wikipedia.org/wiki/Speed
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1, time_exponent=-1)
    _UNITS = \
        {
            # n. mile (m) / sec in hour = 1852/60²
            Unit('knot', 'nautical mile per hour'): 0.5144444444444445,
            Unit('mph', 'mile per hour'): 0.44704
        }
