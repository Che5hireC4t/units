from math import cbrt
from .Length import Length, AbstractQuantity, Unit, DimensionalArray



class Volume(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Volume
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3)
    _UNITS = \
        {
            Unit('l', 'liter', 0.001): 0.001,
            Unit('gal', 'gallon(US)', 0.003785411784): 0.003785411784  # https://en.wikipedia.org/wiki/Gallon
        }



    def cbrt(self) -> Length:
        """
        @return                 Length        The cubic root of @self, expressed as a Length object.

        Example:

        >>> v = Volume(27, 'm2')
        >>> l = v.cbrt()
        >>> l
        3.0 m
        >>> type(l)
        <class 'dimensions.Length.Length'>

        If @self is expressed in liters, the resulting unit will be dm (decimeters), because one liter = 1 dm3
        >>> v = Volume(27, 'l')
        >>> l = v.cbrt()
        >>> l
        3.0 dm

        If @self is expressed in US gallons, the resulting unit will be in (inches), because 1 Gal = 231 in3
        >>> v = Volume(1, 'gal')
        >>> l = v.cbrt()
        >>> l
        6.14 in
        """
        if self.unit_full_name == 'liter':
            new_symbol = 'dm'
        elif self.unit_full_name == 'gallon(US)':
            as_cubic_inches = self.convert('in3')
            return as_cubic_inches.cbrt()
        else:
            new_symbol = self.symbol.replace('3', '')
        new_quantity = cbrt(float(self))
        return Length(new_quantity, new_symbol)
