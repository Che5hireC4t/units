from re import compile, match
from units.__syntax.Prefix import Prefix


class Unit(object):

    __slots__ = ('__symbol', '__long_name', '__factor_from_si_unit', '__detection_regexp')

    __PREFIX = 'prefix'
    __SYMBOL = 'symbol'
    __EXPONENT = 'exponent'

    __instances = dict()



    def __new__(cls, symbol: str, long_name: str, factor_from_si_unit: float = 1.0):
        long_name = str(long_name)
        try:
            instance = cls.__instances[long_name]
        except KeyError:
            instance = super(Unit, cls).__new__(cls)
            cls.__instances[long_name] = instance
        return instance



    def __init__(self, symbol: str, long_name: str, factor_from_si_unit: float = 1.0) -> None:
        self.__long_name = str(long_name)
        self.__symbol = str(symbol)
        self.__factor_from_si_unit = float(factor_from_si_unit)
        self.__detection_regexp = self.__craft_detection_regexp(self.__symbol)
        return



    @classmethod
    def get_unit_from_raw_symbol(cls, raw_symbol: str) -> tuple:
        returned_symbols = list()
        for unit in cls.__instances.values():
            prefix, symbol, exponent = unit.match_raw_symbol(raw_symbol)
            if (prefix, symbol, exponent) != (None, None, None):
                returned_symbols.append((prefix, symbol, exponent))
        if not returned_symbols:
            raise ValueError(f"{raw_symbol} is not associated with any unit.")
        return tuple(returned_symbols)



    def match_raw_symbol(self, raw_symbol: str) -> tuple:
        parsed = match(self.__detection_regexp, raw_symbol)
        if not parsed:
            return None, None, None
        group_prefix = parsed.group('prefix')
        prefix = group_prefix if group_prefix else ''
        # symbol = parsed.group('symbol')
        try:
            exponent = int(parsed.group('exponent'))
        except TypeError:  # If there is no exponent:
            exponent = 1
        return Prefix.init_from_single_value(prefix), self, exponent



    def __craft_detection_regexp(self, symbol: str):
        prefix = self.__PREFIX
        symbol_group = self.__SYMBOL
        exponent = self.__EXPONENT
        regexp = f'^(?P<{prefix}>da|[YZEPTGMkKhHdcmµnpfazy])?(?P<{symbol_group}>{symbol})(?P<{exponent}>-?[0-9]+)?$'
        return compile(regexp)



    if __debug__:
        def __repr__(self) -> str:
            return self.__long_name



    def __get_long_name(self) -> str:
        return self.__long_name

    long_name = property(fget=__get_long_name, doc=f"{__get_long_name.__doc__}")

    def __get_symbol(self) -> str:
        return self.__symbol

    symbol = property(fget=__get_symbol, doc=f"{__get_symbol.__doc__}")

    def __get_factor_from_si(self) -> float:
        return self.__factor_from_si_unit

    factor_from_si_unit = property(fget=__get_factor_from_si, doc=f"{__get_factor_from_si.__doc__}")

    def __get_is_si(self) -> bool:
        return self.__factor_from_si_unit == 1.0

    is_si = property(fget=__get_is_si, doc=f"{__get_is_si.__doc__}")
