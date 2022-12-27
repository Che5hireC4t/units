from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class SubstanceFlow(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(substance_amount_exponent=1, time_exponent=-1)
