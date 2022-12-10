from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class ElectricCharge(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(time_exponent=1, electric_current_exponent=1)
    _UNITS = {Unit('C', 'coulomb', 1.0): 1.0}
