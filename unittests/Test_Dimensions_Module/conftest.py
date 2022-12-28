from dimensions import *


CONVERSION_TABLES_INIT_DATA =  \
    {
        'Length': {'test_dimension': Length, 'length_exponent': 1},
        'Mass': {'test_dimension': Mass, 'mass_exponent': 1},
        'Time': {'test_dimension': Time, 'time_exponent': 1},
        'SubstanceAmount': {'test_dimension': SubstanceAmount, 'substance_amount_exponent': 1},
        'Surface': {'test_dimension': Surface, 'length_exponent': 2},
        'Volume': {'test_dimension': Volume, 'length_exponent': 3},
        'Speed': {'test_dimension': Speed, 'length_exponent': 1, 'time_exponent': -1},
        'Frequency': {'test_dimension': Frequency, 'time_exponent': -1},
        'Acceleration': {'test_dimension': Acceleration, 'length_exponent': 1, 'time_exponent': -2},
        'Pressure': {'test_dimension': Pressure, 'mass_exponent': 1, 'length_exponent': -1, 'time_exponent': -2}
    }



MULTIPLICATION_DATA = \
    {
        (Length, Length): Surface,
        (Length, Surface): Volume,
        (ElectricCurrent, Time): ElectricCharge,
        (Length, Frequency): Speed
    }