from datetime import timedelta
from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Time(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(time_exponent=1)
    _UNITS = \
        {
            Unit('sec', 'second', 1.0): 1.0,
            Unit('min', 'minute', 60.0): 60.0,
            Unit('h', 'hour', 3600.0): 3600.0,
            Unit('d', 'day', 86400.0): 86400.0,
            Unit('w', 'week', 604800.0): 604800.0,
            Unit('y', 'year', 31536000.0): 31536000.0
        }



    def __new__(cls, value: int | float | str | timedelta, unit: str = ''):
        if isinstance(value, timedelta):
            return super(AbstractQuantity, cls).__new__(cls, *cls.__extract_from_timedelta(value))
        try:
            return super(Time, cls).__new__(cls, value)
        except ValueError:  # If value is a string with a unit :
            value_without_unit = cls._strip_unit_chars(value)
            return super(Time, cls).__new__(cls, value_without_unit)



    @staticmethod
    def __extract_from_timedelta(delta_t: timedelta) -> (int | float, str):
        return delta_t.total_seconds(), 'sec'



    def __get_timedelta(self) -> timedelta:
        return timedelta(seconds=float(self.convert('sec')))

    as_timedelta = property(fget=__get_timedelta, doc=f"{__get_timedelta.__doc__}")
