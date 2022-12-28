from itertools import product
from re import compile, match
from math import prod, pow as power

from __syntax import Prefix, UnitContext, Unit
from DimensionalArray import DimensionalArray
from dimensions._MetaQuantity import _MetaQuantity
from exceptions import MissingUnitException, BadUnitException
from dimensions.exceptions import IncompatibleUnitError



class AbstractQuantity(float, metaclass=_MetaQuantity):

    __slots__ = ('_unit_map', '_factor_from_si')

    _UNIT_DETECTION_REGEXP = compile(r'^(?P<prefix>da|[YZEPTGMkKhHdcmµnpfazy])?(?P<symbol>[a-zA-Z]+)(?P<exponent>-?[0-9]+)?$')
    _NUMBER_DETECTION_REGEXP = compile(r'^[0123456789.-]+')
    _DIMENSIONAL_ARRAY = DimensionalArray(127, 127, 127, 127, 127, 127, 127)
    _UNITS = dict()



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



    def has_same_dimensions_than(self, value, strict: bool = False) -> bool:
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







    def __add__(self, other):
        converted_other = other.convert(self)
        return self.__class__(float(self) + float(converted_other), self.symbol)



    def __sub__(self, other):
        converted_other = other.convert(self)
        return self.__class__(float(self) - float(converted_other), self.symbol)



    def __mul__(self, other):
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
                if _MetaQuantity.which_dimension_has(s.elementary_unit) is _MetaQuantity.which_dimension_has(o.elementary_unit):
                    new_elementary_context = UnitContext(o.exponent, s.elementary_unit, s.prefix)
                    converted_base_quantity = other_base_quantity.convert(new_elementary_context.symbol)
                    converted_decomposed_other.append(converted_base_quantity)
                    final_contexts.append(UnitContext(o.exponent + s.exponent, s.elementary_unit, s.prefix))
                else:
                    converted_decomposed_other.append(other_base_quantity)
                    final_contexts.append(UnitContext(o.exponent, o.elementary_unit, o.prefix))
                    final_contexts.append(UnitContext(s.exponent, s.elementary_unit, s.prefix))
        converted_other = self.__class__.prod(converted_decomposed_other)
        final_symbol = self.__get_unit_label(sorted(final_contexts, reverse=True, key=lambda x: x.exponent))
        result = result_class(float(self) * float(converted_other), final_symbol)
        return result



    def __truediv__(self, other):
        return self.__mul__(~other)



    def __invert__(self):
        inverted_class = ~self.__class__
        new_unit_context = \
            [
                UnitContext(-1 * context.exponent, context.elementary_unit, context.prefix)
                for context in self._unit_map
            ]
        inverted_symbol = self.__get_unit_label(sorted(new_unit_context, reverse=True, key=lambda x: x.exponent))
        return inverted_class(1.0/float(self), inverted_symbol)



    @classmethod
    def prod(cls, sequence_of_quantities: list | tuple, initial=None):
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



    __imul__ = __mul__



    def __str__(self) -> str:
        return f"{float(self)} {self.__get_unit_label(self._unit_map, False)}"



    def __run_diagnostic(self, value: int | float | str, unit: str, error_object: Exception) -> None:
        if isinstance(value, (int, float)) and not unit:
            raise MissingUnitException(f"No unit was provided for value {value}") from None
        if isinstance(error_object, LookupError):
            raise BadUnitException(f"{unit} is an invalid unit for a {self.__class__.__name__}") from None
        raise BadUnitException from None



    @classmethod
    def _strip_unit_chars(cls, quantity_as_str_with_unit: str) -> str:
        found = match(cls._NUMBER_DETECTION_REGEXP, quantity_as_str_with_unit)
        return found[0]



    # def _parse_unit_string2(self, unit_as_string: str) -> list:
    #     split_units = unit_as_string.split()
    #     unit_map = list()
    #     for unit_str in split_units:
    #         parsed = match(self._UNIT_DETECTION_REGEXP, unit_str)
    #         symbol, prefix = self.__handle_particular_cases(unit_str)
    #         if symbol is None and prefix is None:
    #             group_prefix = parsed.group('prefix')
    #             prefix = group_prefix if group_prefix else ''
    #             symbol = parsed.group('symbol')
    #         try:
    #             exponent = int(parsed.group('exponent'))
    #         except TypeError:  # If there is no exponent:
    #             exponent = 1
    #         unit = self.__get_unit_from_hint(symbol, exponent)
    #         unit_map.append(UnitContext(exponent, unit, Prefix.init_from_single_value(prefix)))
    #     return unit_map


    # _TEST = tuple()

    def _parse_unit_string(self, unit_as_string: str) -> list:
        metaclass = self.__class__.__class__
        split_units = unit_as_string.split()
        unit_map = list()
        if len(split_units) == 1:
            for builtin_unit in self._UNITS:
                prefix, unit, exponent = builtin_unit.match_raw_symbol(unit_as_string)
                if (prefix, unit, exponent) != (None, None, None):
                    unit_map.append(UnitContext(exponent, unit, prefix))
                    return unit_map
        candidates = list()
        for unit_str in split_units:
            candidates_contexts = Unit.get_unit_from_raw_symbol(unit_str)
            candidates.append({metaclass.which_dimension_has(context[1]): context for context in candidates_contexts})
            # prefix, unit, exponent = Unit.get_unit_from_raw_symbol(unit_str)
            # dimension_class = metaclass.which_dimension_has(unit)
            # dimension_composition[dimension_class] = exponent
            # unit_map.append(UnitContext(exponent, unit, prefix))
        try:
            correct_candidates = self.__select_correct_candidates(candidates)
            [unit_map.append(UnitContext(exponent, unit, prefix)) for prefix, unit, exponent in correct_candidates]
            return unit_map
        except ValueError:
            msg = f"{unit_as_string} is an invalid unit for dimensions {self.__class__.__name__}."
            raise BadUnitException(msg) from None



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



    # def __determine_unit_set_to_use(self, elementary_unit_as_str: str, unit_exponent: int) -> dict:
    #     for unit_map in self._TEST:
    #         for unit, exponent in unit_map.items():
    #             if elementary_unit_as_str == unit.symbol and unit_exponent == exponent:
    #                 return unit_map
    #     raise BadUnitException



    # @staticmethod
    # def __get_unit_from_hint(hint: str, exponent: int, map_to_search_in: dict) -> (Unit, int):
    #     for unit, unit_exponent in map_to_search_in.items():
    #         if exponent == unit_exponent and (hint == unit.symbol or hint == unit.long_name):
    #             return unit
    #     raise BadUnitException  # (f"{hint}{exponent} is not a valid unit for dimension {self.__class__.__name__}.")



    # def __get_unit_from_hint2(self, hint: str, exponent: int) -> (Unit, int):
    #     for unit, unit_exponent in self._UNITS.items():
    #         if exponent == unit_exponent and (hint == unit.symbol or hint == unit.long_name):
    #             return unit
    #     raise BadUnitException(f"{hint}{exponent} is not a valid unit for dimension {self.__class__.__name__}.")



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


    if __debug__:

        def __repr__(self) -> str:
            return self.__str__()



    def __get_symbol(self) -> str:
        return self.__get_unit_label(self._unit_map, False)

    symbol = property(fget=__get_symbol, doc=f"{__get_symbol.__doc__}")

    def __get_full_name(self) -> str:
        return self.__get_unit_label(self._unit_map, True)

    unit_full_name = property(fget=__get_full_name, doc=f"{__get_full_name.__doc__}")

    def __get_factor_from_si_attribute(self) -> float:
        return self._factor_from_si

    factor_from_si = property(fget=__get_factor_from_si_attribute, doc=f"{__get_factor_from_si_attribute.__doc__}")

    def __get_is_si(self) -> bool:
        return self._factor_from_si == 1.0

    is_si = property(fget=__get_is_si, doc=f"{__get_is_si.__doc__}")
