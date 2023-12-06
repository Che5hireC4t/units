from .AbstractQuantity import AbstractQuantity, DimensionalArray


class _NullDimension(AbstractQuantity):
    """
    Dummy dimension, for compatibility issues.
    Returns a simple float, regardless of the unit passed in entry.
    """

    _DIMENSIONAL_ARRAY = DimensionalArray()


    def __new__\
            (
                cls,
                value: int | float | str,
                unit: str = '',
                precision: int | None = None,
                significant_digits: int | None = None
            ):
        """
        @value          int, float, str         A numeric value
        @unit           Any                     Ignored. Just there for compatibility issues
        @precision      Any                     Ignored. Just there for compatibility issues
        @sig_dig        Any                     Ignored. Just there for compatibility issues

        This method just returns value cast as a float.
        """
        return float(value)
