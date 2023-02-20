from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Speed(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1, time_exponent=-1)
    _UNITS = \
        {
            # n. mile (m) / sec in hour = 1852/60²
            Unit('knot', 'nautical mile per hour', 1.9438444924406046): 0.5144444444444445,
            Unit('mph', 'mile per hour', 0.44704): 0.44704
        }
