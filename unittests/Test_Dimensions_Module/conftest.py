from dimensions import *


CONVERSION_TABLES_INIT_DATA =  \
    (
        {'test_dimension': Length, 'length_exponent': 1},
        {'test_dimension': Mass, 'mass_exponent': 1},
        {'test_dimension': Time, 'time_exponent': 1},
        {'test_dimension': SubstanceAmount, 'substance_amount_exponent': 1},
        {'test_dimension': Surface, 'length_exponent': 2},
        {'test_dimension': Volume, 'length_exponent': 3},
        {'test_dimension': Speed, 'length_exponent': 1, 'time_exponent': -1},
        {'test_dimension': Frequency, 'time_exponent': -1},
        {'test_dimension': Acceleration, 'length_exponent': 1, 'time_exponent': -2},
        {'test_dimension': Pressure, 'mass_exponent': 1, 'length_exponent': -1, 'time_exponent': -2}
    )



MULTIPLICATION_DATA = \
    {
        (Length, Length): Surface,
        (Length, Surface): Volume,
        (ElectricCurrent, Time): ElectricCharge,
        (Length, Frequency): Speed
    }