from numpy import ndarray, array, int8, sum
from __syntax import Unit
from exceptions import BadUnitException



class DimensionalArray(ndarray):

    __slots__ = ('__as_array',)

    LENGTH_INDEX = 0
    TIME_INDEX = 1
    MASS_INDEX = 2
    TEMPERATURE_INDEX = 3
    SUBSTANCE_AMOUNT_INDEX = 4
    ELECTRIC_CURRENT_INDEX = 5
    LIGHT_INTENSITY_INDEX = 6



    def __new__\
            (
                cls,
                length_exponent: int = 0,
                time_exponent: int = 0,
                mass_exponent: int = 0,
                temperature_exponent: int = 0,
                substance_amount_exponent: int = 0,
                electric_current_exponent: int = 0,
                light_intensity_exponent: int = 0
            ):
        data_as_tuple = \
            (
                length_exponent,
                time_exponent,
                mass_exponent,
                temperature_exponent,
                substance_amount_exponent,
                electric_current_exponent,
                light_intensity_exponent
            )
        dimensional_array = array(data_as_tuple, dtype=int8)
        return dimensional_array.view(cls)



    def __init__ \
            (
                self,
                length_exponent: int = 0,
                time_exponent: int = 0,
                mass_exponent: int = 0,
                temperature_exponent: int = 0,
                substance_amount_exponent: int = 0,
                electric_current_exponent: int = 0,
                light_intensity_exponent: int = 0
            ) -> None:
        self.__as_array = self.view(ndarray)
        self.setflags(write=False)
        return



    @classmethod
    def register_base_dimensions(cls, dimension_class: type) -> None:
        dimension_class_name = dimension_class.__name__
        dimensions = list(cls.__UNITS_MAP.keys())
        if dimension_class_name not in dimensions:
            return
        units = cls.__UNITS_MAP.values()
        dimensions[dimensions.index(dimension_class_name)] = dimension_class
        cls.__UNITS_MAP = dict(zip(dimensions, units))
        return



    def get_dimension_from_unit(self, unit: Unit) -> type:
        for dimension_class, units in self.__UNITS_MAP.items():
            if unit in units:
                return dimension_class
        raise BadUnitException(f"{unit} can not be associated with a dimension.")



    def __array_finalize__(self, obj):
        if type(obj) is DimensionalArray:
            DimensionalArray.__init__(obj)
        return



    if __debug__:

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({', '.join(self)})"

    def __get_array_view(self) -> ndarray:
        try:
            return self.__as_array
        except AttributeError:
            as_array = self.view(ndarray)
            self.__as_array = as_array
            return as_array


    as_array = property(fget=__get_array_view, doc=f"{__get_array_view.__doc__}")

    def __is_elementary(self) -> bool:
        this_as_array = self.view(ndarray)
        return sum(this_as_array) == 1 and sum(this_as_array == 1) == 1

    is_elementary = property(fget=__is_elementary, doc=f"{__is_elementary.__doc__}")
