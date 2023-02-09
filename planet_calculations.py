import math
from datetime import date
# ELEMENTS @ J2000: a(orbit size), e(orbit shape), i(orbit inclination), mean longitude (L), longitude of perihelion,
# longitude of ascending node
all_planetElements = [
    # mercury
    [0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593],
    # Venus
    [0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255],
    # Earth
    [1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0],
    # Mars
    [1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891],
    # Jupiter
    [5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909],
    # Saturn
    [9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448],
    # Saturn
    [19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503],
    # Neptune
    [30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574]]

all_planetRates = [
    # Mercury
    [0.00000037,0.00001906,-0.00594749,149472.67411175,0.16047689,-0.1253408],
    # Venus
    [0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418],
    # Earth
    [0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0],
    # Mars
    [0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343],
    # Jupiter
    [-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106],
    # Saturn
    [-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794],
    # Uranus
    [-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589],
    # Neptune
    [0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664]]


def gregorian_to_julian(year, month, day):
    i = int((month - 14) / 12)
    jd = day - 32075
    jd += int((1461 * (year + 4800 + i)) / 4)
    jd += int((367 * (month - 2 - (12 * i))) / 12)
    jd -= int((3 * int((year + 4900 + i) / 100)) / 4)
    jc = (jd - 2451545) / 36525  # 2451545: Julian date at J2000
    # 36525: 1 julian century in days
    return jc


#
# def gregorian_to_julian(year, month, day):
#     jd = date(year, month, day).toordinal() + 1721425
#     jc = (jd - 2451545) / 36525
#     return jc
def convert_to_km(my_distance, metric):
    if metric == 'KM':
        my_distance *= 149597870.7
    return my_distance


def calculate_distance(planet1, planet2):
    distance = (((planet2.x - planet1.x) ** 2) + (planet2.y - planet1.y) ** 2) ** 0.5
    return round(distance, 2)


def increment_date(year, month, day):
    if month == 12 and day > 31:
        year += 1
        month = 1
        day = 1
    elif day > 31:
        month += 1
        day = 1
    return year, month, day

def calc_ecc_anomaly(ecc, m, decimal_place, k):
    pi = math.pi
    max_iter = 30
    i = 0
    delta = 10**-decimal_place
    m = m/360
    m=2.0*pi*(m-math.floor(m))

    if ecc < 0.8:
        E = m
    else:
        E = pi
    F = E -ecc*math.sin(m)-m

    while abs(F)>delta and i<max_iter:
        E = E - F/(1.0-ecc*math.cos(E))
        F = E -ecc*math.sin(E)-m
        i += 1

    E = E/k
    return round(E*10**decimal_place/10**decimal_place)

def to_radians(degree):
    return degree * (math.pi / 180)
