from units.dimensions import Length, Acceleration, Pressure, Temperature

# Source : https://wiki.gis.com/wiki/index.php/Flattening
EARTH_RADIUS = Length(6371000, 'm')
EQUATORIAL_EARTH_RADIUS = Length(6378137, 'm')
POLAR_EARTH_RADIUS = Length(6356752, 'm')
G_FORCE = Acceleration(9.80665, 'm sec-2')

# https://fr.wikipedia.org/wiki/Atmosph%C3%A8re_normalis%C3%A9e#Atmosph%C3%A8re_type_OACI
__temperature_gradient_class = Temperature / Length
OACI_NORMALIZED_ATMOSPHERE_TEMPERATURE_GRADIENT = __temperature_gradient_class(0.0065, 'K m-1')
PRESSURE_AT_SEA_LEVEL = Pressure(101325, 'Pa')
TEMPERATURE_AT_SEA_LEVEL = Temperature(288.15, 'K')
