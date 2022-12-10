class _MetaQuantity(type):

    __SPECIAL_CLASSES = \
        {
            (2, 0, 0, 0, 0, 0, 0): 'Surface',
            (3, 0, 0, 0, 0, 0, 0): 'Volume',
            (1, -1, 0, 0, 0, 0, 0): 'Speed',
            (1, -2, 0, 0, 0, 0, 0): 'Acceleration',
            (0, -1, 0, 0, 0, 0, 0): 'Frequency',
            (3, -1, 0, 0, 0, 0, 0): 'VolumetricFlow'
        }

    __instances = {(0, 0, 0, 0, 0, 0, 0): float}



    def __new__(mcs, name: str, bases: tuple, attributes: dict):
        dimensional_array_as_tuple = tuple(attributes['_DIMENSIONAL_ARRAY'])
        user_friendly_name = mcs.__catch_common_dimensions(name, dimensional_array_as_tuple)
        try:
            class_to_return = mcs.__instances[dimensional_array_as_tuple]
        except KeyError:
            class_to_return = super(_MetaQuantity, mcs).__new__(mcs, user_friendly_name, bases, attributes)
            mcs.__instances[dimensional_array_as_tuple] = class_to_return
        return class_to_return



    @classmethod
    def which_dimension_has(mcs, unit) -> type | None:
        instances = [dimension_class for dimension_class in mcs.__instances.values() if dimension_class is not float]
        for dimension_class in instances:
            if unit in dimension_class.UNITS:
                return dimension_class
        return None



    # @classmethod
    # def which_dimension_has(mcs, unit_symbol: str) -> tuple:
    #     instances = [dimension_class for dimension_class in mcs.__instances.values() if dimension_class is not float]
    #     for dimension_class in instances:
    #         for unit in dimension_class.UNITS:
    #             if unit.symbol == unit_symbol:
    #                 return dimension_class, unit
    #     raise ValueError()



    def __mul__(cls, other_cls) -> type:
        """
        :param cls:         type        The class calling the multiplication operator
        :param other_cls:       type        The multiplied class

        :return:            type        A new class combining both.
        """
        new_dimensional_array = cls._DIMENSIONAL_ARRAY + other_cls.DIMENSIONAL_ARRAY
        new_unit_set = cls.__craft_new_unit_set(other_cls)
        new_class_name = f"{cls.__name__}_{other_cls.__name__}"
        return cls.__craft_new_dimension_class(new_class_name, new_dimensional_array, new_unit_set)



    def __pow__(cls, power: int, modulo=None) -> type:
        new_dimensional_array = cls._DIMENSIONAL_ARRAY * power
        new_unit_set = dict()
        for unit_cls, exponent_cls in cls._UNITS.items():
            new_exponent = exponent_cls * power
            if new_exponent != 0:
                new_unit_set[unit_cls] = new_exponent
        new_class_name = f"{cls.__name__}{power}"
        return cls.__craft_new_dimension_class(new_class_name, new_dimensional_array, new_unit_set)



    def __invert__(cls) -> type:
        return pow(cls, -1)



    def __truediv__(cls, other_cls):
        return cls * ~other_cls



    def __craft_new_dimension_class(cls, class_name: str, dimensional_array, unit_set: dict) -> type:
        this_metaclass = cls.__class__
        abstract_quantity_class = cls.__instances[(127, 127, 127, 127, 127, 127, 127)]
        class_attributes = dict()
        class_attributes['_UNITS'] = unit_set
        class_attributes['_DIMENSIONAL_ARRAY'] = dimensional_array
        new_class = this_metaclass(class_name, (abstract_quantity_class,), class_attributes)
        return new_class



    def __craft_new_unit_set(cls, other_cls) -> dict:
        new_unit_set = dict()
        for unit_cls, exponent_cls in cls._UNITS.items():
            for unit_other, exponent_other in other_cls.UNITS.items():
                if unit_cls is unit_other:
                    new_exponent = exponent_cls + exponent_other
                    if new_exponent != 0:
                        new_unit_set[unit_cls] = new_exponent
                else:
                    new_unit_set[unit_cls] = exponent_cls
                    new_unit_set[unit_other] = exponent_other
        return new_unit_set



    @classmethod
    def __catch_common_dimensions(mcs, name: str, dimensional_array: tuple) -> str:
        dimensional_array_as_tuple = tuple(dimensional_array)
        try:
            return mcs.__SPECIAL_CLASSES[dimensional_array_as_tuple]
        except KeyError:
            return name



    def __get_dimensional_array(cls):
        return cls._DIMENSIONAL_ARRAY

    DIMENSIONAL_ARRAY = property(fget=__get_dimensional_array, doc=f"{__get_dimensional_array.__doc__}")

    def __get_units(cls) -> tuple:
        return cls._UNITS

    UNITS = property(fget=__get_units, doc=f"{__get_units.__doc__}")
