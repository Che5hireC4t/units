import pytest
from units.unittests.Test_Syntax_Module.Test_Prefix.conftest import prefix_data_provider


@pytest.mark.parametrize('full_name, symbol, ten_exponent, _', (data for data in prefix_data_provider()))
def test_properly_create_instance(full_name: str, symbol: str, ten_exponent: int, _, supply_uninstantiated_prefix) -> None:
    Prefix = supply_uninstantiated_prefix
    assert len(Prefix._Prefix__instances) == 0
    instance = Prefix(full_name, symbol, ten_exponent)
    assert isinstance(instance, Prefix),\
        f"instance is of type ({type(instance)} for input values {full_name}, {symbol}, {ten_exponent}."
    return


@pytest.mark.parametrize('full_name, symbol, ten_exponent, _', (data for data in prefix_data_provider()))
def test_properly_return_already_instantiated(full_name: str, symbol: str, ten_exponent: int, _, supply_uninstantiated_prefix) -> None:
    Prefix = supply_uninstantiated_prefix
    assert len(Prefix._Prefix__instances) == 0
    first_instance = Prefix(full_name, symbol, ten_exponent)
    second_instance = Prefix(full_name, symbol, ten_exponent)
    assert first_instance is second_instance
    return
