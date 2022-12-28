import pytest
from unittests.Test_Syntax_Module.Test_Prefix.conftest import prefix_data_provider



@pytest.mark.parametrize('full_name, symbol, ten_exponent, prefix_instance', (data for data in prefix_data_provider()))
def test_properly_setup_instance_variables(full_name, symbol, ten_exponent, prefix_instance):
    assert prefix_instance._Prefix__full_name == full_name
    assert prefix_instance._Prefix__symbol == symbol
    assert prefix_instance._Prefix__10_power == ten_exponent
    return



@pytest.mark.parametrize('full_name, symbol, ten_exponent, prefix_instance', (data for data in prefix_data_provider()))
def test_properly_access_properties(full_name, symbol, ten_exponent, prefix_instance):
    assert prefix_instance.full_name == full_name
    assert prefix_instance.symbol == symbol
    assert prefix_instance.ten_power == ten_exponent
    return
