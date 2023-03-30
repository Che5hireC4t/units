from math import sqrt
from .Length import Length, AbstractQuantity, DimensionalArray


class Surface(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=2)



    def sqrt(self) -> Length:
        """
        @return                 Length        The square root of @self, expressed as a Length object.

        Example:

        >>> s = Surface(4, 'm2')
        >>> l = s.sqrt()
        >>> l
        2.0 m
        >>> type(l)
        <class 'dimensions.Length.Length'>
        """
        new_symbol = self.symbol.replace('2', '')
        new_quantity = sqrt(float(self))
        return Length(new_quantity, new_symbol)



    def __pow__(self, power: int | float, modulo=None):
        """
        @param power            int | float             The exponent. ONLY INTEGERS OR 0.5 ARE SUPPORTED!
        @param modulo           int                     The modulo

        @return                 AbstractQuantity        The result of pow(@self, @exponent, @modulo)

        @raise                  TypeError               if @exponent is neither an integer nor 0.5

        If @power == 0.5, then return the result of self.sqrt().
        Otherwise, calls the __pow__ method of AbstractQuantity
        """
        if power == 0.5:
            return self.sqrt()
        return super().__pow__(power, modulo)
