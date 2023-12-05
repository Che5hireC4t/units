from itertools import product
from re import compile, match
from math import prod, pow as power, floor, ceil, log10
from numpy.core import number

from __syntax import Prefix, UnitContext, Unit
from DimensionalArray import DimensionalArray
from ._MetaQuantity import _MetaQuantity
from exceptions import MissingUnitException, BadUnitException
from .exceptions import IncompatibleUnitError



class AbstractQuantity(float, metaclass=_MetaQuantity):
    """
    This class is the abstract class serving as model for all dimensions.
    All the classes representing a dimension must inherit from AbstractQuantity.
    It defines the addition, subtraction, multiplication and division through the
    corresponding magic methods.



    ███████╗ ██╗      ██████╗ ████████╗ ███████╗
    ██╔════╝ ██║     ██╔═══██╗╚══██╔══╝ ██╔════╝
    ███████╗ ██║     ██║   ██║   ██║    ███████╗
    ╚════██║ ██║     ██║   ██║   ██║    ╚════██║
    ███████║ ███████╗╚██████╔╝   ██║    ███████║
    ╚══════╝ ╚══════╝ ╚═════╝    ╚═╝    ╚══════╝

    _unit_map           list        List of UnitContext objects, containing descriptions of assigned units.
    _factor_from_si     float       If @self is multiplied by this factor,
                                    it allows to convert @self to international unit
    _precision          int         Precision of the measurement. Can be None in case of coefficients.



    ██████╗ ██████╗   ██████╗  ██████╗ ███████╗██████╗ ████████╗██╗ ███████╗███████╗
    ██╔══██╗██╔══██╗ ██╔═══██╗ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║ ██╔════╝██╔════╝
    ██████╔╝██████╔╝ ██║   ██║ ██████╔╝█████╗  ██████╔╝   ██║   ██║ █████╗  ███████╗
    ██╔═══╝ ██╔══██╗ ██║   ██║ ██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║ ██╔══╝  ╚════██║
    ██║     ██║  ██║ ╚██████╔╝ ██║     ███████╗██║  ██║   ██║   ██║ ███████╗███████║
    ╚═╝     ╚═╝  ╚═╝  ╚═════╝  ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══════╝╚══════╝

    symbol              -->     _symbol             str         Read Only
    unit_full_name      -->     _                   str         Read Only
    factor_from_si      -->     _factor_from_si     float       Read Only
    is_si               -->     _                   bool        Read Only
    """

    __slots__ = \
        (
            '_unit_map',
            '_factor_from_si',
            '_precision',
            '_significant_digits',
            '_format_cache',
            '__log10',
            '__ceil_log10'
        )

    _UNIT_DETECTION_REGEXP = compile(r'^(?P<prefix>da|[YZEPTGMkKhHdcmµnpfazy])?(?P<symbol>[a-zA-Z]+)(?P<exponent>-?[0-9]+)?$')
    _NUMBER_DETECTION_REGEXP = compile(r'^[0123456789.-]+')
    _DIMENSIONAL_ARRAY = DimensionalArray(127, 127, 127, 127, 127, 127, 127)
    _UNITS = dict()

    __MAPPED_FLOAT_COMPARATORS = \
        {
            0: float.__lt__,
            1: float.__le__,
            2: float.__gt__,
            3: float.__ge__
        }

    __context_cache = dict()



#   ██████╗ ██╗   ██╗ ██████╗ ██╗     ██╗  ██████╗     ███╗   ███╗ ███████╗████████╗██╗  ██╗  ██████╗  ██████╗  ███████╗
#   ██╔══██╗██║   ██║ ██╔══██╗██║     ██║ ██╔════╝     ████╗ ████║ ██╔════╝╚══██╔══╝██║  ██║ ██╔═══██╗ ██╔══██╗ ██╔════╝
#   ██████╔╝██║   ██║ ██████╔╝██║     ██║ ██║          ██╔████╔██║ █████╗     ██║   ███████║ ██║   ██║ ██║  ██║ ███████╗
#   ██╔═══╝ ██║   ██║ ██╔══██╗██║     ██║ ██║          ██║╚██╔╝██║ ██╔══╝     ██║   ██╔══██║ ██║   ██║ ██║  ██║ ╚════██║
#   ██║     ╚██████╔╝ ██████╔╝███████╗██║ ╚██████╗     ██║ ╚═╝ ██║ ███████╗   ██║   ██║  ██║ ╚██████╔╝ ██████╔╝ ███████║
#   ╚═╝      ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═════╝     ╚═╝     ╚═╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝

    def has_same_dimensions_than(self, value, strict: bool = False) -> bool:
        """
        @param value    AbstractQuantity
        @param strict   bool = False

        @return         bool

        This method takes as input any quantity, and checks if this quantity has same
        dimension as @self. If strict is set to True, also checks if @value also has
        the same unit than self.

        Example:
        >>> from dimensions import Length, Mass
        >>> a = Length(1, 'km')
        >>> b = Length(1, 'mil')
        >>> c = Mass(1, 'g')
        >>> a.has_same_dimensions_than(b)
        True
        >>> a.has_same_dimensions_than(b, True)
        False
        >>> a.has_same_dimensions_than(c)
        False
        """
        same_type = type(value) is self.__class__
        if not same_type:
            return False
        return self.symbol == value.symbol or not strict



    @classmethod
    def all_have_same_unit(cls, quantities: tuple | list | set | frozenset) -> bool:
        """
        @param quantities       Iterable                A list / tuple / set / etc. containing quantities

        @return                 bool                    Have all those quantities the same unit?

        @raise                  IncompatibleUnitError   - If the input iterable contains quantities of different dims
                                                        - If the common dimension of all those quantities is not cls

        This method checks if a set of quantities belonging to a specific dimension
        are all expressed in the same unit.

        Examples:

        >>> from dimensions import Length, Mass

        >>> a = Length(4, 'km')
        >>> b = Length(18, 'km')
        >>> c = Length(9.52, 'km')

        >>> Length.all_have_same_unit([a, b, c])
        True

        >>> d = Length(2.8, 'mil')
        >>> Length.all_have_same_unit([a, b, c, d])
        False

        >>> e = Mass(3.7, 'mg')
        >>> Length.all_have_same_unit([a, b, c, d, e])
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 108, in convert
            except (LookupError, ValueError):
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: All the quantities passed in input must have
        the dimension of a Length.
        However, the following dimensions have been detected:
        4 km -> Length
        18 km -> Length
        9.52 km -> Length
        2.8 mil -> Length
        3.7 mg -> Mass
        """
        dimensions = {type(quantity) for quantity in quantities}
        if len(dimensions) != 1:
            problematic_quantities = "\n".join([f"{q} -> {type(q)}" for q in quantities])
            error_message = f"All the quantities passed in input must have the dimension of a {cls.__name__}.\n" \
                            f"However, the following dimensions have been detected:\n{problematic_quantities}"
            raise IncompatibleUnitError(error_message)
        dimension = dimensions.pop()
        if dimension is not cls:
            error_message = f"The quantities must have the dimension of a {cls.__name__}. " \
                            f"However, they have the dimension of a {dimension.__name__}."
            raise IncompatibleUnitError(error_message)
        symbols = {quantity.symbol for quantity in quantities}
        return len(symbols) == 1



    def align_to(self, other):
        if type(self) != type(other):
            raise IncompatibleUnitError(f"{str(self)} and {str(other)} have incompatible unit. Impossible to convert.")
        conversion_factor = self._factor_from_si / other.factor_from_si
        new_unit = other.symbol
        return self.__class__(float(self) * conversion_factor, new_unit)



    def align_units(self, other):
        """
        @param other        AbstractQuantity        Another quantity

        @return             AbstractQuantity        The same quantity as @self, but converted
                                                    to have the same unit for common dimensions as other.

        Example:

        >>> from dimensions import MassFlow, MolarMass
        >>> water_flow = MassFlow(15, 'kg sec-1')
        >>> water_mm = MolarMass(18.015, 'g mol-1')

        Let's suppose you want a substance amount flow (mol sec-1). Theoretically, you just have to
        divide water_flow by water_mm. The problem is the mass unit (common dimension) is not the same.
        You have to "align" the mass unit of one over the mass unit of the other. So you should either
        convert water_flow in g sec-1 or water_mm into kg mol-1.

        This method does that:

        >>> converted_water_flow = water_flow.align_units(water_mm)
        >>> converted_water_flow
        15000 g sec-1

        This method works regardless of the number of common dimensions. If there is no common dimension,
        this method just returns @self.

        Normally, you should not need that method as it is internally called by the magic methods
        __mul__ and __div__. So in that specific example, you can just do water_mm_flow = water_flow / water_mm
        and basta. But as a dev on other side projects, I met the need to use this feature from
        outside the object, so it is not big deal to make it public.
        """
        this_class = self.__class__
        other_class = other.__class__
        if this_class is other_class:
            return self.convert(other.symbol)
        self_unit_map = self._unit_map.copy()
        other_unit_map_dict = \
            {
                _MetaQuantity.which_dimension_has(context.elementary_unit): context
                for context in self.__get_corresponding_protected_attribute_of_other_quantity(self_unit_map, other)
            }
        conversion_factor = 1.0
        final_unit_map = list()
        while self_unit_map:
            context = self_unit_map.pop()
            unit_dimension_class = _MetaQuantity.which_dimension_has(context.elementary_unit)
            if unit_dimension_class not in other_unit_map_dict:
                final_unit_map.append(context)
                continue
            already_mapped_elementary_unit = other_unit_map_dict[unit_dimension_class].elementary_unit
            already_mapped_prefix = other_unit_map_dict[unit_dimension_class].prefix
            analyzed_unit = context.elementary_unit
            analyzed_prefix = context.prefix
            new_unit = analyzed_unit
            new_prefix = analyzed_prefix
            # if bar         is not mmHg  ## Then we want to convert mmHg to bar
            if analyzed_unit is not already_mapped_elementary_unit:
                unit_conversion_map = unit_dimension_class.UNITS
                conversion_factor *= unit_conversion_map[analyzed_unit] / unit_conversion_map[already_mapped_elementary_unit]
                new_unit = already_mapped_elementary_unit
            # if kilo          is not milli  ## Then we want to convert milli to kilo
            if analyzed_prefix is not already_mapped_prefix:
                conversion_factor *= pow(10, analyzed_prefix.ten_power - already_mapped_prefix.ten_power)
                new_prefix = already_mapped_prefix
            new_context = UnitContext(context.exponent, new_unit, new_prefix)
            final_unit_map.append(new_context)
        final_symbol = self.__get_unit_label(final_unit_map)
        return self.__class__(float(self) * conversion_factor, final_symbol)



    def convert(self, new_unit: str):
        """
        @param new_unit     str                     The symbol of a unit to perform the conversion

        @return             AbstractQuantity        The converted quantity

        @raise              IncompatibleUnitError   If trying to convert a dimension to a unit which does not
                                                    belong to that dimension.

        Example:

        >>> from dimensions import Length
        >>> a = Length(1, 'km')
        >>> b = a.convert('mil')
        >>> b
        0.621371192237334 mil
        >>> a.convert('sec')
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 108, in convert
            except (LookupError, ValueError):
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: sec is incompatible with km
        """
        try:
            new_quantity = self.__class__(float(self), new_unit)
        except (LookupError, ValueError):
            raise IncompatibleUnitError(f"{new_unit} is incompatible with {self.symbol}") from None
        conversion_factor = self._factor_from_si / new_quantity.factor_from_si
        if self._precision is None:
            new_quantity._precision = None
            new_quantity._significant_digits = None
        else:
            new_precision = new_quantity.__calculate_precision(self._significant_digits)
            new_quantity._significant_digits = self._significant_digits
            new_quantity._precision = new_precision
        return new_quantity * conversion_factor



    def decompose(self) -> tuple:
        decomposed = [float(self)]
        for context in self._unit_map:
            exponent = context.exponent
            elementary_unit = context.elementary_unit
            prefix = context.prefix
            corresponding_class = _MetaQuantity.which_dimension_has(elementary_unit)
            if exponent != 1:
                powered_dimension_class = pow(corresponding_class, exponent)
                exponent_str = exponent if exponent not in (0, 1) else ''
                decomposed.append(powered_dimension_class(1.0, f"{prefix.symbol}{elementary_unit.symbol}{exponent_str}"))
            else:
                exponent_str = exponent if exponent not in (0, 1) else ''
                decomposed.append(corresponding_class(1.0, f"{prefix.symbol}{elementary_unit.symbol}{exponent_str}"))
        return tuple(decomposed)



    @classmethod
    def sum(cls, sequence_of_quantities: list | tuple | set | frozenset):
        """
        @param sequence_of_quantities       Iterable                    A sequence of AbstractQuantity object

        @return                             AbstractQuantity            The result of the sum of all elements
                                                                        contained in @sequence_of_quantities
        """
        copy_of_sequence = cls.__prepare_sequence_for_operation(sequence_of_quantities)
        result = copy_of_sequence.pop()
        while copy_of_sequence:
            result += copy_of_sequence.pop()
        return result



    @classmethod
    def prod(cls, sequence_of_quantities: list | tuple | set | frozenset):
        """
        @param sequence_of_quantities       Iterable                    A sequence of AbstractQuantity object

        @return                             AbstractQuantity            The result of the product of all elements
                                                                        contained in @sequence_of_quantities
        """
        copy_of_sequence = cls.__prepare_sequence_for_operation(sequence_of_quantities)
        result = copy_of_sequence.pop()
        while copy_of_sequence:
            result *= copy_of_sequence.pop()
        return result



    def get_dimensional_part(self, base_dimension) -> int:
        try:
            if not base_dimension.IS_BASE_QUANTITY:
                raise TypeError(f"{base_dimension.__name__} is not a base quantity.")
            projection = base_dimension.DIMENSIONAL_ARRAY.as_array * self._DIMENSIONAL_ARRAY.as_array
            return projection.sum()
        except AttributeError:
            raise TypeError(f"Unrecognized type: {type(base_dimension)}. Only base quantity classes are accepted.")




#   ███╗   ███╗  █████╗   ██████╗ ██╗  ██████╗     ███╗   ███╗ ███████╗████████╗██╗  ██╗  ██████╗  ██████╗  ███████╗
#   ████╗ ████║ ██╔══██╗ ██╔════╝ ██║ ██╔════╝     ████╗ ████║ ██╔════╝╚══██╔══╝██║  ██║ ██╔═══██╗ ██╔══██╗ ██╔════╝
#   ██╔████╔██║ ███████║ ██║  ███╗██║ ██║          ██╔████╔██║ █████╗     ██║   ███████║ ██║   ██║ ██║  ██║ ███████╗
#   ██║╚██╔╝██║ ██╔══██║ ██║   ██║██║ ██║          ██║╚██╔╝██║ ██╔══╝     ██║   ██╔══██║ ██║   ██║ ██║  ██║ ╚════██║
#   ██║ ╚═╝ ██║ ██║  ██║ ╚██████╔╝██║ ╚██████╗     ██║ ╚═╝ ██║ ███████╗   ██║   ██║  ██║ ╚██████╔╝ ██████╔╝ ███████║
#   ╚═╝     ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═════╝     ╚═╝     ╚═╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝

    #-----------------------#
    #    Object handling    #
    #-----------------------#

    def __new__\
            (
                cls,
                value: int | float | str,
                unit: str = '',
                precision: int | None = None,
                significant_digits: int | None = None
            ):
        try:
            return super(AbstractQuantity, cls).__new__(cls, value)
        except ValueError:  # If value is a string with a unit :
            value_without_unit = cls._strip_unit_chars(value)
            return super(AbstractQuantity, cls).__new__(cls, value_without_unit)



    def __init__\
            (
                self,
                value: int | float | str,
                unit: str = '',
                precision: int | None = None,
                significant_digits: int | None = None
            ) -> None:
        if significant_digits is None and precision is None:
            self._precision = None
            self._significant_digits = None
        elif significant_digits is None and precision is not None:
            self.__log10 = log10(abs(float(self)))
            self.__ceil_log10 = ceil(self.__log10)
            if not isinstance(precision, int):
                raise TypeError(f"precision must be an int or None. Here, it is of type {(str(type(precision)))}.")
            self._precision = precision
            self._significant_digits = self.__calculate_significant_digits(precision)
        elif significant_digits is not None and precision is None:
            self.__log10 = log10(abs(float(self)))
            self.__ceil_log10 = ceil(self.__log10)
            if not isinstance(significant_digits, int):
                raise TypeError(f"significant digits must be an int or None. Here, it is of type {(str(type(precision)))}.")
            self._significant_digits = significant_digits
            self._precision = self.__calculate_precision(significant_digits)
        else:
            msg = 'precision and significant digits cannot be set at same time, because one is computed from the other.'
            raise ArithmeticError(msg)
        self._format_cache = dict()
        try:
            self._unit_map, self._factor_from_si = self.__class__.__context_cache[(self.__class__, unit)]
        except KeyError:
            self.__init_from_scratch(value, unit)
        return



    def __hash__(self) -> int:
        """
        @return     int     An integer representation

        Magic method automatically called when calling the builtin function "hash".
        This method must be defined in order to make an object hashable.
        The "hashable" behavior (and thus this magic method) is mandatory
        to put such an object in a set or as keys in dictionaries.
        """
        return hash(float(self) * hash(self.__class__))



    # -----------------------#
    #         Maths          #
    # -----------------------#

    def __add__(self, other):
        """
        @param other        AbstractQuantity        Another quantity

        @return             AbstractQuantity        The result of the addition between @self and @other

        @raise              IncompatibleUnitError   If @self and @other don't have the same dimensions.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative. Read the end of this docstring.

        Magic method automatically called when using the "+" (plus) operator.
        This method is intended to implement the addition between two quantities.
        Both quantities must belong to the same dimension. Otherwise, an IncompatibleUnitError is raised.
        If both quantities belong to the same dimension, but have different units, this method automatically
        converts @other to the same unit as @self, and returns a result with the same unit as @self.

        Examples:

        >>> from dimensions import Mass, Speed
        >>> m1 = Mass(1.0, 'g')
        >>> m2 = Mass(2.0, 'g')
        >>> m1 + m2
        3.0 g
        >>> m3 = Mass(1.0, 'oz')
        >>> m1 + m3
        29.349523125 g
        >>> sp = Speed(1.0, 'm sec-1')
        >>> m1 + sp
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 252, in __add__
            >>> m3 = Mass(1.0, 'oz')
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 566, in __try_conversion
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: Impossible to compare 1.0 g (Mass)
        and 1.0 m sec-1 (Speed): dimensions are different.

        Explanation about the non-commutative warning:
        >>> m1 = Mass(1.0, 'g')
        >>> m1 + 1
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 282, in __add__
            converted_other = self.__try_conversion(other)
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 687, in __try_conversion
            raise IncompatibleUnitError(error_message)
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: Impossible to compare 1.0 g (Mass)
        and 1 (int): dimensions are different.

        BUT:
        >>> m1 = Mass(1.0, 'g')
        >>> 1 + m1  # 1 is an integer, but can also be a float
        2.0

        This artifact is due to the fact that the called __add__ magic method is the one of the FIRST
        member of the addition. In the first case, the first member is a Mass, thus the Mass
        __add__ method is called. But in the second case, the first member is a simple int and the
        int __add__ magic method is called, which casts the second member as a simple float.
        """
        converted_other = self.__try_conversion(other)
        return self.__class__(float(self) + float(converted_other), self.symbol)



    def __sub__(self, other):
        """
        @param other        AbstractQuantity        Another quantity

        @return             AbstractQuantity        The result of the subtraction from @other to @self

        @raise              IncompatibleUnitError   If @self and @other don't have the same dimensions.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __add__ magic method docstring for further words of explanation.

        Magic method automatically called when using the "-" (minus) operator.
        This method is intended to implement the subtraction between two quantities.
        Both quantities must belong to the same dimension. Otherwise, an IncompatibleUnitError is raised.
        If both quantities belong to the same dimension, but have different units, this method automatically
        converts @other to the same unit as @self, and returns a result with the same unit as @self.

        Examples:

        >>> from dimensions import Mass, Speed
        >>> m1 = Mass(1.0, 'g')
        >>> m2 = Mass(2.0, 'g')
        >>> m2 - m1
        1.0 g
        >>> m3 = Mass(1.0, 'oz')
        >>> m3 - m1
        0.9647260380504196 oz
        >>> sp = Speed(1.0, 'm sec-1')
        >>> m1 - sp
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 252, in __sub__
            converted_other = self.__try_conversion(other)
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 566, in __try_conversion
            raise IncompatibleUnitError(error_message)
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: Impossible to compare 1.0 g (Mass)
        and 1.0 m sec-1 (Speed): dimensions are different.
        """
        converted_other = self.__try_conversion(other)
        return self.__class__(float(self) - float(converted_other), self.symbol)



    def __mul__(self, other):
        """
        @param other        AbstractQuantity        Another quantity

        @return             AbstractQuantity        The result of the multiplication between @self and @other

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This method may not be commutative. Read the end of this docstring.

        Magic method automatically called when using the "*" (time) operator.
        This method is intended to implement the multiplication between two quantities.
        The multiplication between 2 quantities may give a result in a new dimension
        (For instance, a surface multiplied by a speed give a volumetric flow).
        This is automatically handled by this magic method:

        >>> from dimensions import Surface, Speed
        >>> area = Surface(2.0, 'm2')
        >>> sp = Speed(3.0, 'm sec-1')
        >>> flow = area * sp
        >>> flow
        6.0 m3 sec-1
        >>> type(flow)
        <class 'dimensions.VolumetricFlow.VolumetricFlow'>

        If quantities have one or more dimension in common (for instance, surface and speed
        have a length dimension in common), a conversion is internally applied to "align"
        the same units of @other to @self ones.

        Example:

        >>> area = Surface(2.0, 'm2')
        >>> sp = Speed(3.0, 'ft sec-1')
        >>> area * sp
        1.8288 m3 sec-1

        If @self is multiplied by a pure float (without dimension), then a regular multiplication is
        applied and the result will have the same dimension as @self:

        >>> sp = Speed(3.0, 'ft sec-1')
        >>> sp * 2.0
        6.0 ft sec-1

        Explanation about the non-commutative warning:

        If you do the following:
        >>> sp = Speed(3.0, 'ft sec-1')
        >>> sp * 2.0
        6.0 ft sec-1

        BUT:
        >>> sp = Speed(3.0, 'ft sec-1')
        >>> 2.0 * sp  # This will not give a Speed, but a simple float.
        6.0

        This artifact is due to the fact that the called __mul__ magic method is the one of the FIRST
        member of the multiplication. In the first case, the first member is a Speed, thus the Speed
        __mul__ method is called. But in the second case, the first member is a simple float and the
        float __mul__ method is called, which casts the second member as a simple float.
        """
        if type(other) in (float, int) or isinstance(other, number):  # number => numpy.core.number
            new_quantity = self.__class__(float(self) * other, self.symbol)
            if self._significant_digits is not None:
                new_quantity._precision = new_quantity.__calculate_precision(self._significant_digits)
                new_quantity._significant_digits = self._significant_digits
            return new_quantity
        other_class = other.__class__
        result_class = self.__class__ * other_class
        self_unit_map = self._unit_map.copy()
        self_aligned = self.align_units(other)
        final_unit_map = list()
        self_unit_map_dict = \
            {
                _MetaQuantity.which_dimension_has(ctx.elementary_unit): ctx
                for ctx in self.__get_corresponding_protected_attribute_of_other_quantity(self_unit_map, self_aligned)
            }
        other_unit_map_dict = \
            {
                _MetaQuantity.which_dimension_has(context.elementary_unit): context
                for context in self.__get_corresponding_protected_attribute_of_other_quantity(self_unit_map, other)
            }
        dimensions_of_self = set(self_unit_map_dict.keys())
        dimensions_of_other = set(other_unit_map_dict.keys())
        common_dimensions = dimensions_of_self & dimensions_of_other
        self_specific_dimensions = dimensions_of_self - dimensions_of_other
        other_specific_dimensions = dimensions_of_other - dimensions_of_self
        for dimension_class in common_dimensions:
            aligned_context = self_unit_map_dict[dimension_class]
            exponent = aligned_context.exponent + other_unit_map_dict[dimension_class].exponent
            if exponent == 0:
                continue
            unit = aligned_context.elementary_unit  # We ensured by unit alignment it is the same unit...
            prefix = aligned_context.prefix         # ... and prefix.
            final_unit_map.append(UnitContext(exponent, unit, prefix))
        for dimension_class in self_specific_dimensions:
            final_unit_map.append(self_unit_map_dict[dimension_class])
        for dimension_class in other_specific_dimensions:
            final_unit_map.append(other_unit_map_dict[dimension_class])
        final_symbol = self.__get_unit_label(final_unit_map)
        new_quantity = result_class(float(self_aligned) * float(other), final_symbol)
        if self._significant_digits is not None:
            new_quantity._precision = new_quantity.__calculate_precision(self._significant_digits)
            new_quantity._significant_digits = self._significant_digits
        return new_quantity



    def __truediv__(self, other):
        """
        @param other        AbstractQuantity        Another quantity

        @return             AbstractQuantity        The result of the division between @self and @other

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This method may not be commutative.
        Read __mul__ and __add__ magic methods docstrings for further words of explanation.

        Magic method automatically called when using the "/" (divided) operator.
        This method is intended to implement the division between two quantities.
        The division between 2 quantities may give a result in a new dimension
        (For instance, a length divided by a time give a speed).
        This is automatically handled by this magic method:

        >>> from dimensions import Length, Time
        >>> l = Length(6.0, 'm')
        >>> t = Time(3.0, 'sec')
        >>> sp = l / t
        >>> sp
        2.0 m sec-1
        >>> type(sp)
        <class 'dimensions.Speed.Speed'>

        The division of two quantities having the same dimension gives a simple float:
        >>> L = Length(6.0, 'm')
        >>> l = Length(3.0, 'm')
        >>> x = L / l
        >>> x
        2.0
        >>> type(x)
        <class 'float'>

        ...Even if both have not the same units. In that case, the second member is internally
        converted to have the same units as the first member before doing the division:
        >>> L = Length(19.685, 'ft')  # ~ 6m
        >>> l = Length(3.0, 'm')      # This will be converted internally to feet
        >>> L / l
        1.999996
        """
        if isinstance(other, AbstractQuantity):
            return self.__mul__(~other)
        return self.__mul__(1.0 / other)  # Case if @other is a pure float.



    def __invert__(self):
        """
        @return             AbstractQuantity        The result of 1 / @self

        This magic method is automatically called when using the "~" (reverse) operator.
        It computes the reverse of the quantity (1 / quantity). The result will be an
        instance of the reverse dimension.

        Example:

        >>> from dimensions import Time
        >>> t = Time(0.5, 'sec')
        >>> f = ~t
        >>> f
        2.0 sec-1
        >>> type(f)
        <class 'dimensions.Frequency.Frequency'>
        """
        inverted_class = ~self.__class__
        new_unit_context = \
            [
                UnitContext(-1 * context.exponent, context.elementary_unit, context.prefix)
                for context in self._unit_map
            ]
        inverted_symbol = self.__get_unit_label(sorted(new_unit_context, reverse=True, key=lambda x: x.exponent))
        return inverted_class(1.0/float(self), inverted_symbol)



    def __pow__(self, exponent: int, modulo=None):
        """
        @param exponent         int                     The exponent. ONLY INTEGERS ARE SUPPORTED!
        @param modulo           int                     The modulo

        @return                 AbstractQuantity        The result of pow(@self, @exponent, @modulo)

        @raise                  TypeError               if @exponent is not an integer.

        Example:

        >>> from dimensions import Length
        >>> l = Length(2, 'm')
        >>> s = pow(l, 2)
        >>> s
        4.0 m2
        >>> type(s)
        <class 'dimensions.Surface.Surface'>
        """
        if not isinstance(exponent, int):
            raise TypeError(f"Exponent must be a strict integer. However, exponent type is {type(exponent)}")
        new_class = pow(self.__class__, exponent)
        new_unit_context = \
            [
                UnitContext(exponent * context.exponent, context.elementary_unit, context.prefix)
                for context in self._unit_map
            ]
        new_symbol = self.__get_unit_label(sorted(new_unit_context, reverse=True, key=lambda x: x.exponent))
        return new_class(pow(float(self), exponent, modulo), new_symbol)



    __imul__ = __mul__



    # -----------------------#
    #       Comparison       #
    # -----------------------#

    def __eq__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self == @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using the "==" (equal) operator.
        This method is intended to implement the comparison between two quantities.
        Both quantities must belong to the same dimension. Otherwise, an IncompatibleUnitError is raised.
        If both quantities belong to the same dimension, but have different units, this method automatically
        converts @other to the same unit as @self before doing the comparison.

        Examples:

        >>> from dimensions import Mass, Speed
        >>> m1 = Mass(1.0, 'g')
        >>> m2 = m1.convert('oz')
        0.035273961949580414 oz
        >>> m1 == m2
        True
        >>> sp = Speed(1.0, 'm sec-1')
        >>> m1 == sp
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 252, in __eq__
            converted_other = self.__try_conversion(other)
          File "/home/dev/units/dimensions/AbstractQuantity.py", line 566, in __try_conversion
            raise IncompatibleUnitError(error_message)
        dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: Impossible to compare 1.0 g (Mass)
        and 1.0 m sec-1 (Speed): dimensions are different.


        This method takes into account the precision of compared quantities:
        - If one quantity has a precision set to None, then it just compare the values.
        - If both quantities has a precision set, this method return True
          only and if only both value and precision are equal

        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(1, 'g', None)
        >>> m1 == m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(1, 'g', None)
        >>> m1 == m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(1.0, 'g', 1) # Then, m2 = 1.0 g
        >>> m1 == m2
        False
        """
        try:
            converted_other = self.__try_conversion(other)
            if self._precision is None or converted_other.precision is None:
                return float(self) == float(converted_other)
            return float(self) == float(converted_other) and self._precision == converted_other.precision
        except IncompatibleUnitError:
            return False



    def __ne__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self != @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __eq__, __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using "!=" (different) operator. For instance q1 != q2.
        Read docstring of __eq__ magic method as this method is very similar.


        This method takes into account the precision of compared quantities:
        - If one quantity has a precision set to None, then it just compare the values.
        - If both quantities has a precision set, this method return True
          only and if only value or precision are different

        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(1, 'g', None)
        >>> m1 != m2
        False

        >>> m1 = Mass(1, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(1, 'g', None)
        >>> m1 != m2
        False

        >>> m1 = Mass(1, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(1, 'g', 1) # Then, m2 = 1.0 g
        >>> m1 != m2
        True
        """
        try:
            converted_other = self.__try_conversion(other)
            if self._precision is None or converted_other.precision is None:
                return float(self) != float(converted_other)
            return float(self) != float(converted_other) or self._precision != converted_other.precision
        except IncompatibleUnitError:
            return True



    def __lt__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self < @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __eq__, __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using "<" (lower than) operator. For instance q1 < q2.
        Read docstring of __eq__ magic method as this method is very similar.


        This method takes into account the precision of compared quantities:
        - If one quantity has a precision set to None, then it just compare the values.
        - If both quantities has a precision set, this method return True
          if and only if first value < second value and uncertainties does not overlap

        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(2, 'g', None)
        >>> m1 < m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2, 'g', None)
        >>> m1 < m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2.0, 'g', 1) # Then, m2 = 2.0 g
        >>> m1 < m2 # There, all values between [0.999: 1.001] are lower than all values between [1.9: 2.1]
        True

        >>> m1 = Mass(1.199, 'g', 3) # Then, m1 = 1.199 g
        >>> m2 = Mass(1.2, 'g', 1) # Then, m2 = 1.2 g
        >>> m1 < m2 # There, maybe m1 is in fact 1.200 g and m2 is in fact 1.1 g
        False
        """
        return self.__compare(other, 0, False)



    def __le__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self <= @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __eq__, __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using "<=" (lower or equal) operator. For instance q1 <= q2.
        Read docstring of __eq__ magic method as this method is very similar.


        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(2, 'g', None)
        >>> m1 <= m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2, 'g', None)
        >>> m1 <= m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2.0, 'g', 1) # Then, m2 = 2.0 g
        >>> m1 <= m2 # There, all values between [0.999: 1.001] are lower than all values between [1.9: 2.1]
        True

        >>> m1 = Mass(1.199, 'g', 3) # Then, m1 = 1.199 g
        >>> m2 = Mass(1.2, 'g', 1) # Then, m2 = 1.2 g
        >>> m1 <= m2 # There, maybe m1 is in fact 1.200 g and m2 is in fact 1.1 g
        False
        """
        return self.__compare(other, 0, True)



    def __gt__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self > @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __eq__, __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using ">" (greater than) operator. For instance q1 > q2.
        Read docstring of __eq__ magic method as this method is very similar.

        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(2, 'g', None)
        >>> m2 > m1
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2, 'g', None)
        >>> m2 > m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2.0, 'g', 1) # Then, m2 = 2.0 g
        >>> m2 > m1 # There, all values between [1.9: 2.1] are greater than all values between [0.999: 1.001]
        True

        >>> m1 = Mass(1.199, 'g', 3) # Then, m1 = 1.199 g
        >>> m2 = Mass(1.2, 'g', 1) # Then, m2 = 1.2 g
        >>> m2 > m1 # There, maybe m1 is in fact 1.200 g and m2 is in fact 1.1 g
        False
        """
        return self.__compare(other, 2, False)



    def __ge__(self, other) -> bool:
        """
        @param other    AbstractQuantity        Another quantity

        @return         Bool                    Is @self >= @other

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        !!! BIG SCARY FAT WARNING OF DOOM !!!
        This magic method may not be commutative.
        Read __eq__, __add__ and __mul__ magic methods docstrings for further words of explanation.

        Magic method called automatically when using ">=" (greater or equal) operator. For instance q1 >= q2.
        Read docstring of __eq__ magic method as this method is very similar.

        Examples:
        >>> m1 = Mass(1, 'g', None) # None is the default value in constructor
        >>> m2 = Mass(2, 'g', None)
        >>> m2 >= m1
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2, 'g', None)
        >>> m2 >= m2
        True

        >>> m1 = Mass(1.000, 'g', 3) # Then, m1 = 1.000 g
        >>> m2 = Mass(2.0, 'g', 1) # Then, m2 = 2.0 g
        >>> m2 >= m1 # There, all values between [1.9: 2.1] are greater than all values between [0.999: 1.001]
        True

        >>> m1 = Mass(1.199, 'g', 3) # Then, m1 = 1.199 g
        >>> m2 = Mass(1.2, 'g', 1) # Then, m2 = 1.2 g
        >>> m2 >= m1 # There, maybe m1 is in fact 1.200 g and m2 is in fact 1.1 g
        False
        """
        return self.__compare(other, 2, True)



    # -----------------------#
    #        Strings         #
    # -----------------------#

    def __str__(self) -> str:
        return f"{float(self)} {self.__get_unit_label(self._unit_map, False)}"



    def __format__(self, format_spec: str = '') -> str:
        if format_spec in self._format_cache:
            return self._format_cache[format_spec]
        value_as_float = float(self)
        if self._precision is None:
            decimal_places = 6  # This is the default value for float formatting when no precision is set.
            self_rounded = value_as_float
        else:
            decimal_places = self._precision
            self_rounded = round(value_as_float, decimal_places)
        try:
            flags = format_spec.split('+')
        except (AttributeError, TypeError):  # TypeError is raised if format_spec is Bytes.
            raise TypeError(f"Format spec must be a string. {str(type(format_spec))} instead.") from None
        assert len(flags) != 0, f"Flags length = 0. Input value = {str(format_spec)}"
        notation = flags[0]
        if len(flags) > 1:
            if flags[1] != 's':
                raise ValueError(f"Incorrect symbol flag: +{flags[1]}. Should be +s")
            symbol = f" {self.__get_unit_label(self._unit_map, False)}"
        else:
            symbol = ''
        if notation == '':
            if decimal_places <= 0:
                return_value = f"{int(self_rounded)}{symbol}"
            else:
                return_value = f"{self_rounded:.{decimal_places}f}{symbol}"
            self._format_cache[format_spec] = return_value
            return return_value
        if notation == 'e':
            e_decimals = 6 if self._precision is None else self._significant_digits - 1
            if self_rounded == 0.0:
                exponent_sign = '-' if decimal_places >= 0 else '+'
                return_value = f"0e{exponent_sign}{abs(decimal_places):02d}{symbol}"
            else:
                return_value = f"{self_rounded:.{e_decimals}e}{symbol}"
            self._format_cache[format_spec] = return_value
            return return_value
        if notation == 'eng':
            try:
                exponent = int(floor(log10(abs(self_rounded))))
            except ValueError:
                exponent = -1 * decimal_places
            exponent_modulo = exponent % 3
            exponent -= exponent_modulo
            displayed_number = self_rounded / pow(10, exponent)
            exponent_sign = '+' if exponent >= 0 else '-'
            if self._precision is None:
                decimal_places = 6
            else:
                decimal_places = self._significant_digits - exponent_modulo - 1
            if decimal_places <= 0:
                return_value = f"{int(displayed_number)}e{exponent_sign}{abs(exponent):02d}{symbol}"
            else:
                return_value = f"{displayed_number:.{decimal_places}f}e{exponent_sign}{abs(exponent):02d}{symbol}"
            self._format_cache[format_spec] = return_value
            return return_value
        raise ValueError(f"Format spec {notation} not supported.")



    if __debug__:

        def __repr__(self) -> str:
            """
            @return         str         A string representation of the object.

            !!! NOT AVAILABLE IF DEBUG FLAG IS SET TO TRUE !!!

            This magic method is automatically called by the builtin function "repr()",
            or by calling an instance in a python interpreter:

            >>> from dimensions import Length
            >>> x = Length(1, 'm')
            >>> x  # This line calls __repr__
            1.0 m
            """
            return self.__format__('+s')




#   ██████╗ ██████╗  ██████╗ ████████╗        ███╗   ███╗ ███████╗████████╗██╗  ██╗  ██████╗  ██████╗  ███████╗
#   ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝        ████╗ ████║ ██╔════╝╚══██╔══╝██║  ██║ ██╔═══██╗ ██╔══██╗ ██╔════╝
#   ██████╔╝██████╔╝██║   ██║   ██║           ██╔████╔██║ █████╗     ██║   ███████║ ██║   ██║ ██║  ██║ ███████╗
#   ██╔═══╝ ██╔══██╗██║   ██║   ██║           ██║╚██╔╝██║ ██╔══╝     ██║   ██╔══██║ ██║   ██║ ██║  ██║ ╚════██║
#   ██║     ██║  ██║╚██████╔╝   ██║   ██╗     ██║ ╚═╝ ██║ ███████╗   ██║   ██║  ██║ ╚██████╔╝ ██████╔╝ ███████║
#   ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝     ╚═╝     ╚═╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝

    @classmethod
    def _strip_unit_chars(cls, quantity_as_str_with_unit: str) -> str:
        found = match(cls._NUMBER_DETECTION_REGEXP, quantity_as_str_with_unit)
        return found[0]



    def _parse_unit_string(self, unit_as_string: str) -> list:
        metaclass = self.__class__.__class__
        split_units = unit_as_string.split()
        unit_map = list()
        candidates = list()
        for unit_str in split_units:
            candidates_contexts = Unit.get_unit_from_raw_symbol(unit_str)
            candidates.append({metaclass.which_dimension_has(context[1]): context for context in candidates_contexts})
        try:
            correct_candidates = self.__select_correct_candidates(candidates)
            [unit_map.append(UnitContext(exponent, unit, prefix)) for prefix, unit, exponent in correct_candidates]
            return unit_map
        except ValueError:
            msg = f"{unit_as_string} is an invalid unit for dimensions {self.__class__.__name__}."
            raise BadUnitException(msg) from None




#   ██████╗ ██████╗ ██╗██╗   ██╗      ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
#   ██╔══██╗██╔══██╗██║██║   ██║      ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
#   ██████╔╝██████╔╝██║██║   ██║      ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
#   ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝      ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
#   ██║     ██║  ██║██║ ╚████╔╝██╗    ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
#   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═╝    ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

    def __get_factor_from_si(self, contexts: list) -> float:
        metaclass = self.__class__.__class__
        factors = list()
        for context in contexts:
            exponent = context.exponent
            elementary_unit = context.elementary_unit
            prefix = context.prefix
            sub_dimension_class = metaclass.which_dimension_has(elementary_unit)
            base_factor = sub_dimension_class.UNITS[elementary_unit]
            # base_factor = elementary_unit.factor_from_si_unit
            factor = power(base_factor * power(10, prefix.ten_power), exponent)
            factors.append(factor)
        return prod(factors)



    def __compare(self, other, comparator_index: int, equality: bool) -> bool:
        """
        Compare the current instance with another object using specified float comparators.

        This method performs a comparison between the current instance and another object,
        using a specific comparator based on the provided index.
        The comparison takes into account the precision of both objects and can also check for equality.

        :param other:
        The object to compare with the current instance. It is attempted to be converted to a compatible type.

        :param comparator_index:
        An integer index to select the appropriate comparator from `__MAPPED_FLOAT_COMPARATORS`.
        Valid indices are
            - 0 for less than,
            - 1 for less than or equal,
            - 2 for greater than
            - 3 for greater than or equal

        :param equality: A boolean flag indicating whether to check for equality.
        If True, equality is checked based on both value and precision.

        :return: Returns True if the comparison based on the selected comparator is successful, otherwise False.

        The comparison logic includes checking for precision and adjusting the comparison values
        based on the precision of the objects. If the precision is not set (None),
        a different comparator is used for equality check.

        Note:
        - The method uses `__MAPPED_FLOAT_COMPARATORS` for selecting the comparator function.
        - The comparison takes into account the precision of both objects, if available.
        - The method is designed to be used internally within the class and is not part of the public interface.
        """
        converted_other = self.__try_conversion(other)
        comp = self.__MAPPED_FLOAT_COMPARATORS[comparator_index]
        self_as_float = float(self)
        other_as_float = float(converted_other)
        if equality:
            if self._precision is None or converted_other.precision is None:
                comp_equal = self.__MAPPED_FLOAT_COMPARATORS[comparator_index + 1]
                return comp_equal(self_as_float, other_as_float)
            if self_as_float == other_as_float and self._precision == converted_other.precision:
                return True
        comparisons = \
            (
                comp(self_as_float - pow(10, self._precision), other_as_float - pow(10, converted_other.precision)),
                comp(self_as_float - pow(10, self._precision), other_as_float + pow(10, converted_other.precision)),
                comp(self_as_float + pow(10, self._precision), other_as_float - pow(10, converted_other.precision)),
                comp(self_as_float + pow(10, self._precision), other_as_float + pow(10, converted_other.precision)),
            )
        return all(comparisons)



    def __calculate_significant_digits(self, precision: int) -> int:
        """
        Calculate the number of significant digits for the object based on a specified precision.

        This method computes the number of significant digits for the current object.
        The calculation is based on the logarithmic value of the absolute float representation of the object
        and a given precision.

        The calculation involves finding the logarithm base 10 of the absolute value
        of the float representation of `self`. The number of significant digits is then determined
        based on this logarithmic value and the provided precision.
        In most cases, this involves adding the ceiling of the logarithm to the precision.
        However, for numbers that are exact powers of ten, an additional digit is added to the result.

        Note:
        - This method is intended for internal use within the class and is not part of the public interface.
        - It is particularly useful for determining the display format or for calculations requiring
          a specific number of significant digits. See __format__ magic method.

        :param precision: An integer specifying the precision to be used in the calculation.
        :return: Returns an integer representing the number of significant digits.

        Example:
        >>> self = 123.45
        >>> self.__calculate_significant_digits(2)
        5
        """
        ceil_self_log10 = self.__ceil_log10
        if self.__log10 != ceil_self_log10:
            # This is the standard case in 99% of cases.
            return max(1, ceil_self_log10 + precision)
        # We get there for instance if self is a perfect power of ten (1, 1.0, 100.0, etc...)
        return max(1, ceil_self_log10 + precision + 1)



    def __calculate_precision(self: float, significant_digits: int) -> int:
        """
        Calculate the precision needed to reach a specified number of significant digits for the float object.

        This method computes the precision (number of digits after the decimal point) for the current object,
        to achieve a given number of significant digits.
        It is essentially the reverse operation of __calculate_significant_digits method.

        The method calculates the logarithm base 10 of the absolute value of `self`,
        and then determines the necessary precision based on this logarithmic value and the provided significant digits.
        Generally, the calculation involves subtracting the ceiling of the logarithm from the significant digits.
        However, for numbers that are exact powers of ten, an additional adjustment is made to the calculation.

        Note:
        - This method is designed for internal use within the class.
        - It is useful in contexts where a specific number of significant digits is required,
          and the corresponding precision needs to be determined.

        :param significant_digits: An integer representing the desired number of significant digits.
        :return: Returns an integer representing the calculated precision.

        Example:
        >>> obj = 123.45
        >>> obj.__calculate_precision(5)
        2
        """
        ceil_self_log10 = self.__ceil_log10
        if self.__log10 != ceil_self_log10:
            # This is the standard case in 99% of cases.
            return significant_digits - ceil_self_log10
        # We get there for instance if self is a perfect power of ten (1, 1.0, 100.0, etc...)
        return significant_digits - ceil_self_log10 - 1



    def __run_diagnostic(self, value: int | float | str, unit: str, error_object: Exception) -> None:
        if isinstance(value, (int, float)) and not unit:
            raise MissingUnitException(f"No unit was provided for value {value}") from None
        if isinstance(error_object, LookupError):
            raise BadUnitException(f"{unit} is an invalid unit for a {self.__class__.__name__}") from None
        raise BadUnitException from None



    @staticmethod
    def __prepare_sequence_for_operation(sequence_of_quantities: list | tuple | set | frozenset) -> list:
        copy_of_sequence = [item for item in sequence_of_quantities]
        try:
            first_quantity = copy_of_sequence[0]
        except IndexError:  # Happens if sequence_of_quantities is empty
            raise IndexError('Passing an empty sequence for method "sum".') from None
        if type(first_quantity) in (float, int) or isinstance(first_quantity, number):  # number => numpy.core.number
            copy_of_sequence = reversed(copy_of_sequence)
        return copy_of_sequence



    def __select_correct_candidates(self, candidates: list) -> tuple:
        candidates = [c.items() for c in candidates]
        combinaisons = product(*candidates)
        for comb in combinaisons:
            dimension_composition = {cls: umap[2] for cls, umap in comb}
            try:
                self.__check_dimension_composition(dimension_composition)
                return tuple([umap for _, umap in comb])
            except ValueError:
                continue
        raise ValueError()



    def __check_dimension_composition(self, dimension_composition: dict):
        updated_dimensional_array = DimensionalArray(0, 0, 0, 0, 0, 0, 0).as_array
        for dimension_class, exponent in dimension_composition.items():
            dimensional_array = dimension_class.DIMENSIONAL_ARRAY.as_array
            updated_dimensional_array = (dimensional_array * exponent) + updated_dimensional_array
        if bool((updated_dimensional_array == self._DIMENSIONAL_ARRAY.as_array).prod()) is True:
            return
        raise ValueError()



    def __init_from_scratch(self, value: int | float | str, unit: str = None) -> None:
        if isinstance(value, (int, float)) and not unit:
            raise MissingUnitException(f"No unit was provided for value {value}")
        raw_contexts = None
        try:
            raw_contexts = self._parse_unit_string(unit)
            self._unit_map = sorted(raw_contexts, reverse=True, key=lambda x: x.exponent)
        except AttributeError:  # if unit is None
            try:
                unit_without_value = value.lstrip('-., 0123456789')
                raw_contexts = self._parse_unit_string(unit_without_value)
                self._unit_map = sorted(raw_contexts, reverse=True, key=lambda x: x.exponent)
            except AttributeError as error:
                self.__run_diagnostic(value, unit, error)
        except BadUnitException:
            msg = f"{unit} is not a valid unit for dimension {self.__class__.__name__}"
            raise BadUnitException(msg) from None
        self._factor_from_si = self.__get_factor_from_si(raw_contexts)
        self.__class__.__context_cache[(self.__class__, unit)] = (self._unit_map, self._factor_from_si)
        return



    def __get_corresponding_protected_attribute_of_other_quantity(self, self_attribute_value, other_quantity):
        """
        @param self_attribute_value     Any                 An attribute of @self. For instance self._unit_map
        @param other_quantity           AbstractQuantity    Another quantity

        @return                         Any                 The value stored in the attribute with
                                                            the same name for @other_quantity

        @raise                          TypeError           if @other_quantity is not an AbstractQuantity

        This method strictly internal is intended to retrieve the protected or private attributes
        of another quantity in a compliant way. Indeed, it is normally considered as a bad practice
        to query directly a protected or private attribute. Some languages such as PhP or C++ even
        purposely crash if the developer tries to do that. In Python, everything is public.
        Hence, you can do it, but it does not mean you should.

        But in that particular case, I want to access to a protected / private attribute of an instance
        of this class, from another instance of this same class. Thus, we already know that attribute
        exists, and we also have an idea of its value.

        Moreover, we need those private attributes only for internal comparison purpose. They do not
        need to be exposed to the outside word, and they should not because they are of no utility
        outside this class.
        """
        error_message = f"other_quantity must be an AbstractQuantity object. " \
                        f"However, type(other_quantity) = {type(other_quantity)}"
        assert isinstance(other_quantity, AbstractQuantity), error_message
        for attribute_name in AbstractQuantity.__slots__:
            value = getattr(self, attribute_name)
            if value == self_attribute_value:
                # Warning. Potential bug if an attribute contains a float('NaN') because float('NaN') != float('NaN')
                # (Yes, this is silly, but true. Try by yourself in a Python shell if you don't trust me).
                return getattr(other_quantity, attribute_name)
        raise TypeError(error_message)



    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        dimensional_array = self._DIMENSIONAL_ARRAY
        if dimensional_array[dimensional_array.TIME_INDEX] != 0:
            if unit_as_string.startswith('min'):  # Minute. Conflict with "mili" (m) prefix
                return 'min', ''
        if dimensional_array[dimensional_array.LENGTH_INDEX] != 0:
            if unit_as_string.startswith('mil'):  # Mile. Conflict with "mili" (m) prefix
                return 'mil', ''
            if unit_as_string.startswith('nmil'):  # Nautical mile. Nonflict with "nano' (n) prefix.
                return 'nmil', ''
        return None, None



    @staticmethod
    def __get_unit_label(contexts, full_label: bool = False) -> str:
        name_items = list()
        for context in contexts:
            exponent = context.exponent
            elementary_unit = context.elementary_unit
            prefix = context.prefix
            exponent_str = exponent if exponent not in (0, 1) else ''
            if full_label:
                name_items.append(f"{prefix.full_name}{elementary_unit.long_name}{exponent_str}")
            else:
                name_items.append(f"{prefix.symbol}{elementary_unit.symbol}{exponent_str}")
        return ' '.join(name_items)



    def __try_conversion(self, other):
        """
        @param other    AbstractQuantity        Another quantity

        @return         AbstractQuantity        @other converted to the same unit as @self

        @raise          IncompatibleUnitError   if @other is not of the same dimensions as @self.

        This method tries to perform the conversion in order to compare @self and @other.
        It is called by mathematical and comparison magic method when the calling procedure
        tries to add two quantities, or check if a quantity is greater than another.
        """
        if not isinstance(other, self.__class__):
            error_message = f"Impossible to compare {self} ({self.__class__.__name__}) " \
                            f"and {other} ({other.__class__.__name__}): dimensions are different."
            raise IncompatibleUnitError(error_message)
        converted_other = other.convert(self.symbol)
        return converted_other




#   ██████╗ ██████╗   ██████╗  ██████╗ ███████╗██████╗ ████████╗██╗ ███████╗███████╗
#   ██╔══██╗██╔══██╗ ██╔═══██╗ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║ ██╔════╝██╔════╝
#   ██████╔╝██████╔╝ ██║   ██║ ██████╔╝█████╗  ██████╔╝   ██║   ██║ █████╗  ███████╗
#   ██╔═══╝ ██╔══██╗ ██║   ██║ ██╔═══╝ ██╔══╝  ██╔══██╗   ██║   ██║ ██╔══╝  ╚════██║
#   ██║     ██║  ██║ ╚██████╔╝ ██║     ███████╗██║  ██║   ██║   ██║ ███████╗███████║
#   ╚═╝     ╚═╝  ╚═╝  ╚═════╝  ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚══════╝╚══════╝

    def __get_symbol(self) -> str:
        """
        symbol      -->     _symbol     str     Read Only

        The unit symbol attached to the quantity. For instance, if self = Speed(1, 'm sec-1'),
        symbol = 'm sec-1'
        """
        return self.__get_unit_label(self._unit_map, False)

    symbol = property(fget=__get_symbol, doc=f"{__get_symbol.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_full_name(self) -> str:
        """
        unit_full_name      -->     _     str     Read Only

        The full name of the unit. For instance "Meter", "Pascal", "Electron-Volt", etc...
        """
        return self.__get_unit_label(self._unit_map, True)

    unit_full_name = property(fget=__get_full_name, doc=f"{__get_full_name.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_factor_from_si_attribute(self) -> float:
        """
        factor_from_si      -->     _factor_from_si     float     Read Only

        This is a view to @self._factor_from_si (factor from international system).
        This factor relates @self to the corresponding value in the international system.
        """
        return self._factor_from_si

    factor_from_si = property(fget=__get_factor_from_si_attribute, doc=f"{__get_factor_from_si_attribute.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_is_si(self) -> bool:
        """
        is_si      -->     _     bool     Read Only

        True if this quantity is expressed with unit of the international system.
        False otherwise.

        For instance, 1 Pa (Pressure) will have this property set to True because
        1 Pa = 1 Kg m-1 sec-2. All those units are SI.

        But 1 mmHg (Pressure) will have this property set to False, because mercury
        millimeter is not SI.
        """
        return self._factor_from_si == 1.0

    is_si = property(fget=__get_is_si, doc=f"{__get_is_si.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __is_base_quantity(self) -> bool:
        """
        TL;DR --> Return true if `self` belongs to one of the following:
        - Time
        - Mass
        - Length
        - Temperature
        - SubstanceAmount
        - ElectricCurrent
        - LightIntensity

        (and False in any other case)

        Complete answer: the above-mentioned dimensions are called base quantities and their dimensional array
        is a pure unit in one the 7 dimensions vectorial base axis.

        In practice, this function checks if the dimensional array of the underlying class has exactly one of its
        values equal to 1, and 0 elsewhere.
        """
        return self.__class__.IS_BASE_QUANTITY  # This is a property defined in _MetaQuantity metaclass.

    is_base_quantity = property(fget=__is_base_quantity, doc=f"{__is_base_quantity.__doc__}")
# ----------------------------------------------------------------------------------------------------------------------

    def __get_precision(self) -> int | None:
        """
        How precise self is known? This is related to how many digits after comma there is?

        https://en.wikipedia.org/wiki/Precision_(computer_science)
        """
        return self._precision

    precision = property(fget=__get_precision, doc=f"{__get_precision.__doc__}")

# ----------------------------------------------------------------------------------------------------------------------

    def __get_significant_digits(self) -> int | None:
        """
        https://en.wikipedia.org/wiki/Significant_figures
        """
        return self._significant_digits

    significant_digits = property(fget=__get_significant_digits, doc=f"{__get_significant_digits.__doc__}")
