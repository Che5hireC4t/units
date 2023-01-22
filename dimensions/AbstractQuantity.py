from itertools import product
from re import compile, match
from math import prod, pow as power

from __syntax import Prefix, UnitContext, Unit
from DimensionalArray import DimensionalArray
from dimensions._MetaQuantity import _MetaQuantity
from exceptions import MissingUnitException, BadUnitException
from dimensions.exceptions import IncompatibleUnitError



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

    __slots__ = ('_unit_map', '_factor_from_si')

    _UNIT_DETECTION_REGEXP = compile(r'^(?P<prefix>da|[YZEPTGMkKhHdcmµnpfazy])?(?P<symbol>[a-zA-Z]+)(?P<exponent>-?[0-9]+)?$')
    _NUMBER_DETECTION_REGEXP = compile(r'^[0123456789.-]+')
    _DIMENSIONAL_ARRAY = DimensionalArray(127, 127, 127, 127, 127, 127, 127)
    _UNITS = dict()



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
        if type(self) is not type(value):
            return False
        if not strict:
            return True



    def align_to(self, other):
        if type(self) != type(other):
            raise IncompatibleUnitError(f"{str(self)} and {str(other)} have incompatible unit. Impossible to convert.")
        conversion_factor = self._factor_from_si / other.factor_from_si
        new_unit = other.symbol
        return self.__class__(float(self) * conversion_factor, new_unit)



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
    def prod(cls, sequence_of_quantities: list | tuple, initial=None):
        """
        @param sequence_of_quantities       Iterable                    A sequence of AbstractQuantity object
        @param initial                      AbstractQuantity = None     The first element to init the product

        @return                             AbstractQuantity            The result of the product of all elements
                                                                        contained in @sequence_of_quantities

        Note: the code of this method is a quasi copy-paste of the function collection.Reduce
        """
        if type(sequence_of_quantities[0]) in (float, int):
            sequence_of_quantities = reversed(sequence_of_quantities)
        it = iter(sequence_of_quantities)
        if initial is None:
            try:
                value = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty iterable with no initial value") from None
        else:
            value = initial
        for element in it:
            value = cls.__mul__(value, element)
        return value




#   ███╗   ███╗  █████╗   ██████╗ ██╗  ██████╗     ███╗   ███╗ ███████╗████████╗██╗  ██╗  ██████╗  ██████╗  ███████╗
#   ████╗ ████║ ██╔══██╗ ██╔════╝ ██║ ██╔════╝     ████╗ ████║ ██╔════╝╚══██╔══╝██║  ██║ ██╔═══██╗ ██╔══██╗ ██╔════╝
#   ██╔████╔██║ ███████║ ██║  ███╗██║ ██║          ██╔████╔██║ █████╗     ██║   ███████║ ██║   ██║ ██║  ██║ ███████╗
#   ██║╚██╔╝██║ ██╔══██║ ██║   ██║██║ ██║          ██║╚██╔╝██║ ██╔══╝     ██║   ██╔══██║ ██║   ██║ ██║  ██║ ╚════██║
#   ██║ ╚═╝ ██║ ██║  ██║ ╚██████╔╝██║ ╚██████╗     ██║ ╚═╝ ██║ ███████╗   ██║   ██║  ██║ ╚██████╔╝ ██████╔╝ ███████║
#   ╚═╝     ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═════╝     ╚═╝     ╚═╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝

    #-----------------------#
    #    Object handling    #
    #-----------------------#

    def __new__(cls, value: int | float | str, unit: str = ''):
        try:
            return super(AbstractQuantity, cls).__new__(cls, value)
        except ValueError:  # If value is a string with a unit :
            value_without_unit = cls._strip_unit_chars(value)
            return super(AbstractQuantity, cls).__new__(cls, value_without_unit)



    def __init__(self, value: int | float | str, unit: str = None) -> None:
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
        if type(other) in (float, int):
            return self.__class__(float(self) * other, self.symbol)
        other_class = other.__class__
        result_class = self.__class__ * other_class
        decomposed_self = self.decompose()
        decomposed_other = other.decompose()
        converted_decomposed_other = [float(other)]
        final_contexts = list()
        for self_base_quantity in decomposed_self[1:]:
            for other_base_quantity in decomposed_other[1:]:
                s = self_base_quantity._unit_map[0]
                o = other_base_quantity._unit_map[0]
                self_elementary_unit = s.elementary_unit
                other_elementary_unit = o.elementary_unit
                if _MetaQuantity.which_dimension_has(self_elementary_unit) is _MetaQuantity.which_dimension_has(other_elementary_unit):
                    new_elementary_context = UnitContext(o.exponent, self_elementary_unit, s.prefix)
                    converted_base_quantity = other_base_quantity.convert(new_elementary_context.symbol)
                    converted_decomposed_other.append(converted_base_quantity)
                    exponents_sum = o.exponent + s.exponent
                    if exponents_sum == 0:
                        continue
                    final_contexts.append(UnitContext(exponents_sum, self_elementary_unit, s.prefix))
                else:
                    converted_decomposed_other.append(other_base_quantity)
                    if (other_base_quantity.__class__.DIMENSIONAL_ARRAY.as_array * result_class.DIMENSIONAL_ARRAY).sum() != 0:
                        final_contexts.append(UnitContext(o.exponent, other_elementary_unit, o.prefix))
                    if (self_base_quantity.__class__.DIMENSIONAL_ARRAY.as_array * result_class.DIMENSIONAL_ARRAY).sum() != 0:
                        final_contexts.append(UnitContext(s.exponent, self_elementary_unit, s.prefix))
        converted_other = self.__class__.prod(converted_decomposed_other)
        final_symbol = self.__get_unit_label(sorted(final_contexts, reverse=True, key=lambda x: x.exponent))
        result = result_class(float(self) * float(converted_other), final_symbol)
        return result



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) == float(converted_other)



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) != float(converted_other)



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) < float(converted_other)



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) <= float(converted_other)



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) > float(converted_other)



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
        """
        converted_other = self.__try_conversion(other)
        return float(self) >= float(converted_other)




    # -----------------------#
    #        Strings         #
    # -----------------------#

    def __str__(self) -> str:
        return f"{float(self)} {self.__get_unit_label(self._unit_map, False)}"



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
            return self.__str__()




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



    def __run_diagnostic(self, value: int | float | str, unit: str, error_object: Exception) -> None:
        if isinstance(value, (int, float)) and not unit:
            raise MissingUnitException(f"No unit was provided for value {value}") from None
        if isinstance(error_object, LookupError):
            raise BadUnitException(f"{unit} is an invalid unit for a {self.__class__.__name__}") from None
        raise BadUnitException from None



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
        return other.convert(self.symbol)




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
