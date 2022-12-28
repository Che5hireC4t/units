from __syntax import Prefix


def prefix_data_provider() -> (str, str, int, Prefix):
    prefix_map = getattr(Prefix, f"_{Prefix.__name__}__PREFIXES")
    for full_name, symbol, ten_exponent in prefix_map:
        instance = Prefix(full_name, symbol, ten_exponent)
        yield full_name, symbol, ten_exponent, instance
