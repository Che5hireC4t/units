from unittests.Test_Dimensions_Module.dependencies.ConversionArray import ConversionArray


def get_simple_data_generator(*args: list, **kwargs: dict) -> tuple:
    conversion_table = ConversionArray(*args, **kwargs)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    test_values_generator = conversion_table.generate_test_values(yield_random)
    return dimension_class, test_values_generator



def get_conversion_data_generator(*args: list, **kwargs: dict) -> tuple:
    conversion_table = ConversionArray(*args, **kwargs)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    conversion_values_generator = conversion_table.generate_conversion_test_data(yield_random)
    return dimension_class, conversion_values_generator
