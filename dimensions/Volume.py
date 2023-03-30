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
    __ONE_THIRD = 1 / 3



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



    def __pow__(self, power: int | float, modulo=None):
        """
        @param power            int | float             The exponent. ONLY INTEGERS OR 1/3 ARE SUPPORTED!
        @param modulo           int                     The modulo

        @return                 AbstractQuantity        The result of pow(@self, @exponent, @modulo)

        @raise                  TypeError               if @exponent is neither an integer nor 1/3

        If @power == 1/3, then return the result of self.cbrt().
        Otherwise, calls the __pow__ method of AbstractQuantity
        """
        if power == self.__ONE_THIRD:
            return self.cbrt()
        return super().__pow__(power, modulo)
