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
