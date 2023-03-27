class Prefix(object):

    __slots__ = ('__full_name', '__symbol', '__10_power')

    # https://physics.nist.gov/cuu/Units/prefixes.html
    __PREFIXES = \
        (
            ('yotta', 'Y', 24),
            ('zetta', 'Z', 21),
            ('exa', 'E', 18),
            ('peta', 'P', 15),
            ('tera', 'T', 12),
            ('giga', 'G', 9),
            ('mega', 'M', 6),
            ('kilo', 'k', 3),
            ('hecto', 'h', 2),
            ('deca', 'da', 1),
            ('', '', 0),
            ('deci', 'd', -1),
            ('centi', 'c', -2),
            ('mili', 'm', -3),
            ('micro', 'µ', -6),
            ('nano', 'n', -9),
            ('pico', 'p', -12),
            ('femto', 'f', -15),
            ('atto', 'a', -18),
            ('zepto', 'z', -21),
            ('yocto', 'y', -24)
        )

    __instances = dict()



    def __new__(cls, full_name: str, symbol: str, ten_power: int):
        symbol = cls.__aliases_for_kilo_hecto(symbol)
        if (full_name, symbol) == (None, None):
            full_name, symbol = '', ''
        cls.__raise_for_invalid_values(full_name, symbol, ten_power)
        symbol = str(symbol)
        try:
            instance = cls.__instances[symbol]
        except KeyError:
            instance = super(Prefix, cls).__new__(cls)
            cls.__instances[symbol] = instance
        return instance



    @classmethod
    def __aliases_for_kilo_hecto(cls, symbol: str) -> str:
        if symbol in ('K', 'H'):
            return symbol.lower()
        return symbol



    def __init__(self, full_name: str, symbol: str, ten_power: int) -> None:
        self.__full_name = full_name
        self.__symbol = symbol
        self.__10_power = ten_power
        return



    def __getnewargs__(self) -> tuple:
        """
        I have never heard from this magic method until now. According to the docs,
        __getnewargs__ method is suitable if you want to pickle / unpickle an object
        from a class overloading the __new__ method.

        Indeed, the magic method __setstate__ is intended to restore the state of an
        object at unpickling stage. However, it requires this object to already exists
        (and obviously being empty). Thus, the __new__ method must have already been
        called to create the object. The default behavior when unpickling an object
        is passing an empty tuple to the __new__ method. But if __new__ is overloaded
        to get multiple arguments, python raises the following error during unpickling:

        "TypeError: MyClass.__new__() missing n required positional arguments: ..."

        Thus, __getnewargs__ is there to fix that issue:
        - It never takes any parameters
        - It is automatically called on the object at pickling stage
        - It must return a tuple of variables.
        - Those variables are saved for unpickling stage
        - At unpickling stage, those variable are used as parameters for __new__

        More doc there:

        https://peps.python.org/pep-0307/#the-getnewargs-method
        https://docs.python.org/3/library/pickle.html#object.__getnewargs__
        """
        return self.__full_name, self.__symbol, self.__10_power



    if __debug__:
        def __repr__(self) -> str:
            return self.__full_name if self.__full_name else ''



    @classmethod
    def init_from_single_value(cls, value: str | int):
        return cls(*cls.__guess_prefix(value))



    @classmethod
    def __raise_for_invalid_values(cls, full_name: str, symbol: str, ten_power: int) -> None:
        if (full_name, symbol, ten_power) in cls.__PREFIXES:
            return
        raise ValueError(f"Invalid values for profile initialization: {full_name}, {symbol}, {ten_power}")



    @classmethod
    def __guess_prefix(cls, value: str | int) -> (str, str, int):
        if value is None:
            value = ''
        for full_name, symbol, ten_exponent in cls.__PREFIXES:
            if value == full_name or cls.__aliases_for_kilo_hecto(str(value)) == symbol or value == ten_exponent:
                return full_name, symbol, ten_exponent
        raise ValueError(f"Failed to guess prefix from that value: {value}.")



    def __get_full_name(self) -> str:
        return self.__full_name

    full_name = property(fget=__get_full_name, doc=f"{__get_full_name.__doc__}")

    def __get_symbol(self) -> str:
        return self.__symbol

    symbol = property(fget=__get_symbol, doc=f"{__get_symbol.__doc__}")

    def __get_10_power(self) -> int:
        return self.__10_power

    ten_power = property(fget=__get_10_power, doc=f"{__get_10_power.__doc__}")
