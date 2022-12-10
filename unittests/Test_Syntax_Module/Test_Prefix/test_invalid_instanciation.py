import pytest
from random import randint
from units.unittests.Fuzzer import Fuzzer
from units.unittests.Test_Syntax_Module.Test_Prefix.conftest import prefix_data_provider


@pytest.mark.parametrize('_', range(1000))
def test_raise_for_unordered_data(_, supply_uninstantiated_prefix):
    Prefix = supply_uninstantiated_prefix
    prefix_map = getattr(Prefix, f"_{Prefix.__name__}__PREFIXES")
    upper_limit = len(prefix_map) - 1
    index_1, index_2, index_3 = randint(0, upper_limit), randint(0, upper_limit), randint(0, upper_limit)
    while index_1 == index_2 == index_3:
        index_1, index_2, index_3 = randint(0, upper_limit), randint(0, upper_limit), randint(0, upper_limit)
    random_symbol = [line[1] for line in prefix_map][index_2]
    random_name = [line[0] for line in prefix_map][index_1]
    random_power = [line[2] for line in prefix_map][index_3]
    with pytest.raises(ValueError):
        Prefix(random_name, random_symbol, random_power)
    assert len(Prefix._Prefix__instances) == 0
    return


@pytest.mark.parametrize('__', range(20))
@pytest.mark.parametrize('full_name, symbol, ten_exponent, _', (data for data in prefix_data_provider()))
def test_raise_for_invalid_exponent(full_name, symbol, ten_exponent, _, __, supply_uninstantiated_prefix):
    Prefix = supply_uninstantiated_prefix
    invalid_exponent = randint(-30, 30)
    while invalid_exponent == ten_exponent:
        invalid_exponent = randint(-30, 30)
    with pytest.raises(ValueError):
        Prefix(full_name, symbol, invalid_exponent)
    assert len(Prefix._Prefix__instances) == 0
    return



fuzzer = Fuzzer()
@pytest.mark.parametrize("invalid_symbol", (fuzzer.get_randstring(0, 10, fuzzer.ASCII_ALPHANUM) for _ in range(10)))
@pytest.mark.parametrize("invalid_name", (fuzzer.get_randstring(0, 10, fuzzer.ASCII_ALPHANUM) for _ in range(10)))
@pytest.mark.parametrize("invalid_exponent", (fuzzer.logarithmic_randint() for _ in range(10)))
def test_fuzzing(invalid_symbol, invalid_name, invalid_exponent, supply_uninstantiated_prefix):
    Prefix = supply_uninstantiated_prefix
    with pytest.raises(ValueError):
        Prefix(invalid_name, invalid_symbol, invalid_exponent)
    assert len(Prefix._Prefix__instances) == 0
    return


@pytest.mark.parametrize('_', range(1000))
def test_fuzzing2(supply_uninstantiated_prefix, supply_fuzzer, _):
    Prefix = supply_uninstantiated_prefix
    fuzzer = supply_fuzzer
    invalid_symbol = fuzzer.get_random_object()
    invalid_name = fuzzer.get_random_object()
    invalid_exponent = fuzzer.get_random_object()
    with pytest.raises(ValueError):
        Prefix(invalid_name, invalid_symbol, invalid_exponent)
    assert len(Prefix._Prefix__instances) == 0
    return
