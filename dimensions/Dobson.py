from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Dobson(AbstractQuantity):
    """
    Supported units: all supported SubstanceAmount units over all supported Length units ^-2:
    >>> Dobson(1.0, "mol m-2")
    >>> Dobson(1.0, "part mil-2")
    etc...

    Furthermore, dobson units (DU) and prefixes (milli, micro, etc...) are supported:
    >>> Dobson(1.0, "DU")
    >>> Dobson(1.0, "mDU")
    >>> Dobson(1.0, "µDU")

    https://en.wikipedia.org/wiki/Dobson_unit
    https://ozonewatch.gsfc.nasa.gov/facts/dobson.html
    https://sacs.aeronomie.be/info/dobson.php
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(substance_amount_exponent=1, length_exponent=-2)
    _UNITS = {Unit('DU', 'dobson', 0.00044615): 0.00044615}
