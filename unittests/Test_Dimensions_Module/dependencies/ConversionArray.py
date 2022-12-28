import csv
from random import sample, uniform
from numpy import ndarray, array, stack, nditer

from dimensions import *



class ConversionArray(ndarray):

    __slots__ = ('__symbol_map', '__as_array', '__salt', '__single_symbol_conversion_data', '__dimension_class')

    __CONVERSION_TABLE_PATH = 'unittests/Test_Dimensions_Module/Conversion_Tables'

    __TIME_TABLE = f"{__CONVERSION_TABLE_PATH}/{Time.__name__}.csv"
    __MASS_TABLE = f"{__CONVERSION_TABLE_PATH}/{Mass.__name__}.csv"
    __LENGTH_TABLE = f"{__CONVERSION_TABLE_PATH}/{Length.__name__}.csv"
    __TEMPERATURE_TABLE = f"{__CONVERSION_TABLE_PATH}/{Temperature.__name__}.csv"
    __SUBSTANCE_AMOUNT_TABLE = f"{__CONVERSION_TABLE_PATH}/{SubstanceAmount.__name__}.csv"
    __ELECTRIC_CURRENT_TABLE = f"{__CONVERSION_TABLE_PATH}/{ElectricCurrent.__name__}.csv"
    __LIGHT_INTENSITY_TABLE = f"{__CONVERSION_TABLE_PATH}/{LightIntensity.__name__}.csv"

    __TABLE_ORDER_OF_PROCESS = \
        (
            __LENGTH_TABLE,
            __TIME_TABLE,
            __MASS_TABLE,
            __TEMPERATURE_TABLE,
            __SUBSTANCE_AMOUNT_TABLE,
            __ELECTRIC_CURRENT_TABLE,
            __LIGHT_INTENSITY_TABLE
        )

    __data_transmission_to_init = dict()

    __MAX_NUMBER_OF_ITEMS = 300



    def __new__ \
            (
                cls,
                test_dimension: type,
                length_exponent: int = 0,
                time_exponent: int = 0,
                mass_exponent: int = 0,
                temperature_exponent: int = 0,
                substance_amount_exponent: int = 0,
                electric_current_exponent: int = 0,
                light_intensity_exponent: int = 0
            ):
        index = -1
        symbol_map = list()
        conversion_table = array((1.0,), dtype=float)
        exponent_map = \
            (
                length_exponent,
                time_exponent,
                mass_exponent,
                temperature_exponent,
                substance_amount_exponent,
                electric_current_exponent,
                light_intensity_exponent
            )
        for exponent in exponent_map:
            index += 1
            if exponent == 0:
                continue
            conversion_data = cls.__get_conversion_data(cls.__TABLE_ORDER_OF_PROCESS[index], exponent)
            conversion_table = cls.__stack_dimensions(conversion_table, tuple(conversion_data.values()))
            symbol_map.append(tuple(conversion_data.keys()))
        conversion_table = conversion_table.squeeze(axis=-1)
        symbol_map.reverse()
        cls.__data_transmission_to_init[exponent_map] = tuple(symbol_map)
        return conversion_table.view(cls)



    def __init__ \
            (
                self,
                test_dimension: type,
                length_exponent: int = 0,
                time_exponent: int = 0,
                mass_exponent: int = 0,
                temperature_exponent: int = 0,
                substance_amount_exponent: int = 0,
                electric_current_exponent: int = 0,
                light_intensity_exponent: int = 0
            ) -> None:
        exponent_map = \
            (
                length_exponent,
                time_exponent,
                mass_exponent,
                temperature_exponent,
                substance_amount_exponent,
                electric_current_exponent,
                light_intensity_exponent
            )
        self.__dimension_class = test_dimension
        self.__symbol_map = self.__data_transmission_to_init.pop(exponent_map)
        self.__as_array = self.view(ndarray)
        salt = self.__define_salt()
        self.__salt = salt
        self.__as_array *= salt
        try:
            if sum(exponent_map) == 1:
                raise FileNotFoundError
            csv_filename = f"{self.__CONVERSION_TABLE_PATH}/{test_dimension.__name__}.csv"
            single_symbol_conversion_data = self.__get_conversion_data(csv_filename, 1)
            single_symbol_conversion_data = \
                {
                    symbol: value * salt
                    for symbol, value in single_symbol_conversion_data.items()
                }
            self.__single_symbol_conversion_data = single_symbol_conversion_data
        except FileNotFoundError:
            self.__single_symbol_conversion_data = dict()
        self.setflags(write=False)
        return



    def parse_combined_conversion_data(self, yield_random: bool = False) -> (float, str):
        self_as_array = self.__as_array
        number_of_yielded_items = 0
        max_number_of_iterations = min\
            (
                max
                (
                    1,
                    self.__MAX_NUMBER_OF_ITEMS - len(self.__single_symbol_conversion_data)
                ),
                self.size
            )
        if yield_random:
            pointer_to_offset = 0
            random_offsets_test = self.__setup_random_offsets(max_number_of_iterations)
        with nditer(self_as_array, flags=['multi_index']) as test_data_iterator:
            while number_of_yielded_items < max_number_of_iterations:
                if yield_random:
                    [next(test_data_iterator) for _ in range(random_offsets_test[pointer_to_offset]-1)]
                    pointer_to_offset += 1
                test_number = float(next(test_data_iterator))
                test_symbol_indexes = test_data_iterator.multi_index
                test_symbol = self.__get_symbol_from_multi_index(test_symbol_indexes)
                yield test_number, test_symbol
                number_of_yielded_items += 1



    def generate_test_data(self, yield_random: bool = False) -> (float, str, str, float):
        for test_number, source_symbol in self.parse_specific_conversion_data():
            for expected_number, target_symbol in self.parse_specific_conversion_data():
                yield test_number, source_symbol, target_symbol, expected_number
        for test_number, source_symbol in self.parse_specific_conversion_data():
            for expected_number, target_symbol in self.parse_combined_conversion_data(yield_random):
                yield test_number, source_symbol, target_symbol, expected_number
        for test_number, source_symbol in self.parse_combined_conversion_data(yield_random):
            for expected_number, target_symbol in self.parse_specific_conversion_data():
                yield test_number, source_symbol, target_symbol, expected_number
        for test_number, source_symbol in self.parse_combined_conversion_data(yield_random):
            for expected_number, target_symbol in self.parse_combined_conversion_data(yield_random):
                yield test_number, source_symbol, target_symbol, expected_number



    def generate_test_values(self, yield_random: bool = False) -> (float, str):
        for test_number, symbol in self.parse_specific_conversion_data():
            yield test_number, symbol
        for test_number, symbol in self.parse_combined_conversion_data(yield_random):
            yield test_number, symbol



    def parse_specific_conversion_data(self) -> (float, str):
        single_symbol_conversion_data = self.__single_symbol_conversion_data
        for test_symbol, test_number in single_symbol_conversion_data.items():
            yield test_number, test_symbol



    def __setup_random_offsets(self, max_number_of_iterations: int) -> tuple:
        indexes_to_yield = sorted(sample(range(self.size), k=max_number_of_iterations))
        indexes_to_yield_copy = indexes_to_yield.copy()
        indexes_to_yield_copy.pop()
        indexes_to_yield_copy.insert(0, 0)
        offsets = [b - a for b, a in zip(indexes_to_yield, indexes_to_yield_copy)]
        return tuple(offsets)



    @staticmethod
    def __get_conversion_data(csv_conversion_table: str, dimension_exponent: int) -> dict:
        conversion_data = dict()
        exponent_str = str(dimension_exponent) if dimension_exponent != 1 else ''
        with open(csv_conversion_table, 'r') as file_descriptor:
            reader = csv.reader(file_descriptor, delimiter=',', quotechar='"')
            next(reader)  # Skipping first row
            prefix_symbols = next(reader)[2:]  # Retrieving prefix symbols of second row
            next(reader)  # Skipping third row
            for row in reader:
                base_symbol = row[1]
                data = row[2:]
                conversion_data.update \
                    (
                        {
                            f"{pref_symb}{base_symbol}{exponent_str}": pow(float(test_number), dimension_exponent)
                            for pref_symb, test_number in zip(prefix_symbols, data)
                        }
                    )
        return conversion_data



    def __get_symbol_from_multi_index(self, multi_index: tuple) -> str:
        final_symbols = list()
        for index, dimension_specific_symbols in zip(multi_index, self.__symbol_map):
            final_symbols.append(dimension_specific_symbols[index])
        return ' '.join(final_symbols)



    @staticmethod
    def __define_salt() -> float:
        salt = 0.0
        while salt == 0.0 or salt == 1.0:
            salt = uniform(-100, 100)
        return salt



    @staticmethod
    def __stack_dimensions(conversion_table: ndarray, conversion_data: tuple) -> ndarray:
        data_to_be_stacked = [conversion_table * data for data in conversion_data]
        return_value = stack(data_to_be_stacked)
        return return_value



    def __get_dimension_class(self):
        return self.__dimension_class

    dimension_class = property(fget=__get_dimension_class, doc=f"{__get_dimension_class.__doc__}")
