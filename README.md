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

# Installation

```
$ git clone https://github.com/Che5hireC4t/units
$ python
>>> import units
```
Of course, `units` must be in `sys.path` python variable. This can be done among other by being in the same directory
as the newly cloned repository.

# Basic usage

```
>>> from units.dimensions import Length
>>> l = Length(1, 'm')
>>> l
1.0 m
```

`Length` class is derived from the builtin class `float`. This also the case for all the dimension classes (Mass,
Speed, etc...):
```
>>> isinstance(l, float)
True
```

If you try to add / sub quantities belonging to the same dimension, but with different units, the conversion is automatically
done internally. The result has the same unit that the first quantity:
```
>>> from units.dimensions import Mass
>>> m1 = Mass(1, 'kg')
>>> m2 = Mass(1, 'lb')
>>> m1 + m2
1.45359237 kg
```

If you try to add / sub quantities belonging to different dimensions, an exception is raised:
```
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
```
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

```
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