import pytest
from unittests.Test_Syntax_Module.Test_Prefix.conftest import prefix_data_provider



@pytest.mark.parametrize('full_name, symbol, ten_exponent, instance', (data for data in prefix_data_provider()))
def test_properly_guess(full_name, symbol, ten_exponent, instance):
    Prefix = instance.__class__
    guess_prefix_method = getattr(Prefix, f"_{Prefix.__name__}__guess_prefix")
    expected_result = (full_name, symbol, ten_exponent)
    assert guess_prefix_method(full_name) == expected_result
    assert guess_prefix_method(symbol) == expected_result
    assert guess_prefix_method(ten_exponent) == expected_result
    return
