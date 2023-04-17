from datetime import timedelta
from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Time(AbstractQuantity):
    """
    Supported units (from smallest to biggest):

    Second          sec         Time(1.0, "sec")
    Minute          min         Time(1.0, "min")
    Hour            h           Time(1.0, "h")
    Day             d           Time(1.0, "d")
    Week            w           Time(1.0, "w")
    Year            y           Time(1.0, "y")

    This class has also an interface with the datetime module.
    In particular, a timedelta object can be passed an argument
    to __init__ / __new__ methods:

    >>> from datetime import timedelta
    >>> from dimensions import Time
    >>> td = timedelta(days=1, hours=1, minutes=1, seconds=1, microseconds=1)
    >>> t = Time(t)

    It is also possible to retrieve the time as a timedelta object:
    >>> t = Time(18, 'sec')
    >>> td = t.as_timedelta
    >>> type(td)
    <class 'datetime.timedelta'>
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(time_exponent=1)
    _UNITS = \
        {
            Unit('sec', 'second'): 1.0,
            Unit('min', 'minute'): 60.0,
            Unit('h', 'hour'): 3600.0,
            Unit('d', 'day'): 86400.0,
            Unit('w', 'week'): 604800.0,
            Unit('y', 'year'): 31536000.0
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
        """
        @param delta_t      timedelta                   A time interval

        @return             tuple(int | float, str)     A number and its unit,
                                                        to build a Time object

        Private class method called by __new__ in order to convert a timedelta object
        to arguments which can be processed by the constructor of the super class
        to instantiate a quantity object.
        """
        return delta_t.total_seconds(), 'sec'



    def __get_timedelta(self) -> timedelta:
        """
        @return         timedelta       Time object converted to a timedelta one.

        Property to access the Time object as a datetime.timedelta object.
        >>> t = Time(18, 'sec')
        >>> td = t.as_timedelta
        >>> type(td)
        <class 'datetime.timedelta'>
        """
        return timedelta(seconds=float(self.convert('sec')))

    as_timedelta = property(fget=__get_timedelta, doc=f"{__get_timedelta.__doc__}")
