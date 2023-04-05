# What is this repo or project?

This project is a python module intended to handle physical quantities such as time, pressure, electric charge, etc...

Scientists often have to perform calculations with such quantities. This poses some issues when trying to write scripts
or programs because there are compatibility issues:
- You cannot add or withdraw unrelated quantities (Example: you cannot add 1°K (Temperature) with 1 m sec-1 (speed)).
- For same dimension quantities, you must ensure they have the same unit, eventually by performing a conversion before
(Example: if a = 1 mile and b = 1km, you must perform a conversion before adding).

When a script is running, python doesn't care natively of the dimension of a float contained in a variable. Thus, it
can perform unauthorized operations without raising any errors. This is a problem because in the best scenario, you may
be a bit puzzled while interpreting the output results, and at worst [you may crash your orbiter on Mars, and explain to
your boss this little 
mistake cost $494.84 million](https://en.wikipedia.org/wiki/Mars_Climate_Orbiter#Cause_of_failure).

# Dependencies

- Numpy
- (pytest, for running the unit tests)

# Installation

```shell
$ pip install --user --upgrade numpy pytest
$ git clone https://github.com/Che5hireC4t/units
$ python
>>> import units
```
Of course, `units` must be in `sys.path` python variable. This can be done among other by being in the same directory
as the newly cloned repository.

# Basic usage

```python
>>> from units.dimensions import Length
>>> l = Length(1, 'm')
>>> l
1.0 m
```

`Length` class is derived from the builtin class `float`. This is also the case for all the dimension classes (Mass,
Speed, etc...):
```python
>>> isinstance(l, float)
True
```

If you try to add / sub quantities belonging to the same dimension, but with different units, the conversion is automatically
done internally. The result has the same unit that the first quantity:
```python
>>> from units.dimensions import Mass
>>> m1 = Mass(1, 'kg')
>>> m2 = Mass(1, 'lb')
>>> m1 + m2
1.45359237 kg
```

If you try to add / sub quantities belonging to different dimensions, an `IncompatibleUnitError` exception is raised.
This exception is derived from `TypeError`.
```python
>>> from units.dimensions import Pressure
>>> p = Pressure(1, 'torr')
>>> p + m2
Traceback (most recent call last):
  File "/home/dev/units/dimensions/AbstractQuantity.py", line 122, in __add__
    converted_other = other.convert(self.symbol)
  File "/home/dev/units/dimensions/AbstractQuantity.py", line 76, in convert
    raise IncompatibleUnitError(f"{new_unit} is incompatible with {self.symbol}") from None
dimensions.exceptions.IncompatibleUnitError.IncompatibleUnitError: torr is incompatible with kg
```

If you perform a multiplication / division between 2 different dimensions, the result will have its dedicated dimension:
```python
>>> from units.dimensions import Time
>>> l = Length(1, 'km')
>>> t = Time(1, 'h')
>>> s = l/t
>>> type(s)
<class 'dimensions.Speed.Speed'>
>>> s
1.0 km h-1
```

# Constants

Many physical constants have been redefined. They are sorted in dedicated modules:
- fundamental (light celerity, Planck constant, elementary charge, etc...)
- geological (Earth radius, g, Atmosphere pressure, etc...)
- molar masses
- thermodynamics

```python
>>> from units.constants.geological import EARTH_RADIUS, PRESSURE_AT_SEA_LEVEL
>>> from units.constants.molar_masses import WATER, SULFUR_DIOXIDE
>>> EARTH_RADIUS
6371000.0 m
>>> PRESSURE_AT_SEA_LEVEL
101325.0 Pa
>>> WATER
18.015 g mol-1
>>> SULFUR_DIOXIDE
64.064 g mol-1
```

# Limitations

Some unittests have not been fixed yet. To run the unittests, run
```shell
$ cd units
$ pytest
```

Quantities objects are ***much*** slower than regular float, as highlighted by the following performance test:
```python
>>> from timeit import timeit
>>> 
>>> setup = \
... """
... from dimensions import Surface, Dobson
... from dimensions import Length, Time
... a = 2.0
... b = 3.0
... l = Length(a, 'm')
... t = Time(b, 'sec')
... """
>>> 
>>> timeit(stmt='res = a / b', setup=setup, number=10000)
0.000195320999409887
>>> timeit(stmt='res = l / t', setup=setup, number=10000)
0.8214943899947684
```

This is a problem I am currently working on. In the meantime, if you have a 10000 * 10000 floats matrix, don't fill it
with quantities or your program will never end. Instead, attach *one* quantity to that matrix, serving as unit
reference. For doing a conversion, calculate a conversion factor from that unit as a regular float and multiply all your
matrix item by that conversion factor.