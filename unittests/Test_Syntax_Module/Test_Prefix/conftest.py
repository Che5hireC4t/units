import pytest
from units.__syntax import Prefix


@pytest.fixture(scope='function')
def supply_uninstantiated_prefix():
    setattr(Prefix, f"_{Prefix.__name__}__instances", None)
    setattr(Prefix, f"_{Prefix.__name__}__instances", dict())
    yield Prefix


@pytest.fixture(scope='module')
def supply_pre_instantiated_prefix() -> (type, tuple):
    from units.__syntax.Prefix import Prefix
    prefix_map = getattr(Prefix, f"_{Prefix.__name__}__PREFIXES")
    instances = list()
    for input_data in prefix_map:
        instances.append(Prefix(*input_data))
    return Prefix, tuple(instances)


def prefix_data_provider() -> (str, str, int, Prefix):
    prefix_map = getattr(Prefix, f"_{Prefix.__name__}__PREFIXES")
    for full_name, symbol, ten_exponent in prefix_map:
        instance = Prefix(full_name, symbol, ten_exponent)
        yield full_name, symbol, ten_exponent, instance
