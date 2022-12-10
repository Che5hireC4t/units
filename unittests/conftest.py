import pytest
from Fuzzer import Fuzzer


@pytest.fixture(scope='session', autouse=True)
def supply_fuzzer():
    return Fuzzer()


@pytest.fixture(scope='function')
def get_random_alphanum(supply_fuzzer) -> str:
    fuzzer = supply_fuzzer
    return fuzzer.get_randstring(0, 10, fuzzer.ASCII_ALPHANUM)


@pytest.fixture(scope='function')
def get_random_logarithmic_int(supply_fuzzer) -> int:
    fuzzer = supply_fuzzer
    return fuzzer.logarithmic_randint()


@pytest.fixture(scope='function')
def get_random_object(supply_fuzzer) -> object:
    fuzzer = supply_fuzzer
    return fuzzer.get_random_object()
