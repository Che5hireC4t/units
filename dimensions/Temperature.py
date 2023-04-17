from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Temperature(AbstractQuantity):
    """
    Supported units (From smallest to biggest):

    Kelvin     K       Temperature(1.0, "K")        https://en.wikipedia.org/wiki/Kelvin

    https://en.wikipedia.org/wiki/Temperature
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(temperature_exponent=1)
    _UNITS = \
        {
            Unit('K', '°Kelvin'): 1.0
        }
    __FAHRENHEIT_KELVIN_FACTOR = 5.0/9.0
    __ABSOLUTE_ZERO = -273.15



    def __new__(cls, value: int | float | str, unit: str = '') -> AbstractQuantity:
        unit = unit.lstrip('°')
        if unit == 'F':
            return super(Temperature, cls).__new__(cls, cls.__fahrenheit_to_kelvin(value), 'K')
        if unit == 'C':
            return super(Temperature, cls).__new__(cls, value - cls.__ABSOLUTE_ZERO, 'K')
        if unit == 'B':
            return super(Temperature, cls).__new__(cls, cls.__benamran_to_kelvin(value), 'K')
        return super(Temperature, cls).__new__(cls, value, unit)



    def __init__(self, value: int | float | str, unit: str) -> None:
        unit = unit.lstrip('°')
        if unit in ('F', 'C', 'B'):
            super().__init__(value, 'K')
            return
        super().__init__(value, unit)
        return



    def __kelvin_to_fahrenheit(self) -> float:
        return 1.8 * (float(self) + self.__ABSOLUTE_ZERO) + 32

    @classmethod
    def __fahrenheit_to_kelvin(cls, degree_fahrenheit: float) -> float:
        return (degree_fahrenheit - 32) * cls.__FAHRENHEIT_KELVIN_FACTOR - cls.__ABSOLUTE_ZERO

    def __get_celsius(self) -> float:
        return float(self) + self.__ABSOLUTE_ZERO

    def __kelvin_to_benamran(self) -> float:
        """
        https://www.youtube.com/watch?v=OqcqsUaEqUk

        T'es le meilleur, Bruce. Big up à toi, bro (;
        """
        return (187.0 / 352.5) * (self.as_celsius - 4.2)

    @classmethod
    def __benamran_to_kelvin(cls, degree_benamram: float) -> float:
        return ((352.5 / 187.0) * degree_benamram + 4.2) - cls.__ABSOLUTE_ZERO

    as_celsius = property(fget=__get_celsius, doc=f"{__get_celsius.__doc__}")
    as_fahrenheit = property(fget=__kelvin_to_fahrenheit, doc=f"{__kelvin_to_fahrenheit.__doc__}")
    as_benamran = property(fget=__kelvin_to_benamran, doc=f"{__kelvin_to_benamran.__doc__}")
