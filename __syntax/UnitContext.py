from units.__syntax.Prefix import Prefix


class UnitContext(object):

    __slots__ = ('__exponent', '__elementary_unit', '__prefix')


    def __init__(self, exponent: int, elementary_unit, prefix: Prefix = Prefix.init_from_single_value('')) -> None:
        self.__exponent = int(exponent)
        self.__elementary_unit = elementary_unit
        self.__prefix = prefix
        return



    if __debug__:
        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.__exponent}, \"{self.__elementary_unit}\", \"{self.__prefix}\")"


    def __get_exponent(self) -> int:
        return self.__exponent

    exponent = property(fget=__get_exponent, doc=f"{__get_exponent.__doc__}")

    def __get_prefix(self) -> Prefix:
        return self.__prefix

    prefix = property(fget=__get_prefix, doc=f"{__get_prefix.__doc__}")

    def __get_elementary_unit(self):
        return self.__elementary_unit

    elementary_unit = property(fget=__get_elementary_unit, doc=f"{__get_elementary_unit.__doc__}")

    def __get_symbol(self) -> str:
        string_items = \
            (
                self.__prefix.symbol if self.__prefix else '',
                self.__elementary_unit.symbol,
                str(self.__exponent) if self.__exponent not in (0, 1) else ''
            )
        return ''.join(string_items)

    symbol = property(fget=__get_symbol, doc=f"{__get_symbol.__doc__}")

    def __get_full_name(self) -> str:
        string_items = \
            (
                self.__prefix.full_name if self.__prefix else '',
                self.__elementary_unit.long_name,
                str(self.__exponent) if self.__exponent not in (0, 1) else ''
            )
        return ''.join(string_items)

    long_name = property(fget=__get_full_name, doc=f"{__get_full_name.__doc__}")
