import math
planet_lst = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
# ELEMENTS @ J2000: a(orbit size), e(orbit shape), i(orbit inclination), mean longitude (L),
# longitude of perihelion, longitude of ascending node

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


def gregorian_to_julian(day, month, year):
    i = int((month - 14) / 12)
    jd = day - 32075
    jd += int((1461 * (year + 4800 + i)) / 4)
    jd += int((367 * (month - 2 - (12 * i))) / 12)
    jd -= int((3 * int((year + 4900 + i) / 100)) / 4)
    jc = (jd - 2451545) / 36525  # 2451545: Julian date at J2000
    # 36525: 1 julian century in days
    return jc # number of Julian centuries

#
# def gregorian_to_julian(year, month, day):
#     jd = date(year, month, day).toordinal() + 1721425
#     jc = (jd - 2451545) / 36525
#     return jc
def convert_to_km(my_distance):
    my_distance *= 149597870.7
    return round(my_distance, 2)

def calculate_distance(planet1_x, planet1_y, planet2_x, planet2_y):
    try:
        distance_squared = (((planet2_x- planet1_x) ** 2) + (planet2_y - planet1_y) ** 2)
        distance = math.sqrt(distance_squared)
        return round(distance, 2)
    except:
        print('Error')



def calculate_true_anomaly(anomaly_arg):
    try:
        k = math.pi / 180.0
        true_anomaly = 2 * (math.atan(anomaly_arg) / k)
        print(true_anomaly)
        return round(true_anomaly, 3)
    except Exception:
        print('Error')

def increment_date(year, month, day):
    if month == 12 and day > 31: # end of the year
        year += 1
        month = 1
        day = 1
    elif day > 31: # end of the month
        month += 1
        day = 1
    return year, month, day
# Deriving E from equation for M
def calc_ecc_anomaly(e, M): # e: Eccentricity, M: Mean anomaly
    try:
        m = M/360
        m=2.0*math.pi*(m-math.floor(m))

        if e < 0.8:
            E = m
        else:
            E = math.pi
        F = E -e*math.sin(m)-m

        while abs(F)>1e-06:
            E = E - F/(1.0-e*math.cos(E))
            F = E -e*math.sin(E)-m

        E = E/(math.pi / 180)

        return round(E)
    except Exception:
        print('Error')

def calculate_mean_anomaly(L, long_peri):
    try:
        mean_anomaly = L - long_peri # mean longitude - longitude of Perihelion
        return round(mean_anomaly, 3)
    except:
        Exception

def to_radians(degrees):
    return degrees * (math.pi / 180)
def calculate_anomaly_arg(e, E): # eccentricity and eccentric anomaly passed in
    try:
        anomaly_arg = (math.sqrt((1 + e) / (1 - e))) * (
        math.tan(to_radians(E) / 2))
        return round(anomaly_arg, 4)
    except Exception:
        print('Error')
def calculate_radius_vector(a, e, E):
    try:
        radius_vector = a * (1 - (e * (math.cos(to_radians(E)))))
        return round(radius_vector, 4)
    except Exception:
        print('Error')
# to_radians(-230.7)
print(calculate_radius_vector('hello', 0.2056, 192))
def calculate_elements(planet, jul_centuries):
    i = planet_lst.index(planet) # index of the planet
    planet_elements = all_planetElements[i] # use index to find the elements for the planet
    planet_rates = all_planetRates[i]

    # Semi major axis (a)
    semi_major = planet_elements[0] + (planet_rates[0] * jul_centuries)
    # Eccentricity (e)
    eccentricity = planet_elements[1] + (planet_rates[1] * jul_centuries)

    # ORBIT INCLINATION (i)
    orbit_incl = planet_elements[2] + (planet_rates[2] * jul_centuries)
    orbit_incl = orbit_incl % 360 # keeps angle between 0 and 360

    # LONGITUDE OF ASCENDING NODE (long_asc)
    long_asc_node = planet_elements[5] + (
            planet_rates[5] * jul_centuries)
    long_asc_node = long_asc_node % 360 # keeps angle between 0 and 360

    # LONGITUDE OF PERIHELION (long_peri)
    long_perihelion = planet_elements[4] + (planet_rates[4] * jul_centuries)
    long_perihelion = long_perihelion % 360 # keeps angle between 0 and 360

    # MEAN LONGITUDE (L)
    L = planet_elements[3] + (planet_rates[3] * jul_centuries)
    L = L % 360

    # MEAN ANOMALY
    mean_anomaly = calculate_mean_anomaly(L, long_perihelion)

    # ECCENTRIC ANOMALY

    eccentric_anomaly = calc_ecc_anomaly(eccentricity, mean_anomaly)

    # ANOMALY ARG

    anomaly_argument = calculate_anomaly_arg(eccentricity, eccentric_anomaly)

    # TRUE ANOMALY
    true_anomaly = calculate_true_anomaly(anomaly_argument)

    # RADIUS VECTOR
    radius_vector = calculate_radius_vector(semi_major, eccentricity, eccentric_anomaly)

    if round(long_perihelion, 3) == 131.602 and round(long_asc_node, 3) == 76.680 and round(true_anomaly, 3)\
            == 61.340 and round(radius_vector, 3) == 0.721:
        print(orbit_incl)
    return semi_major, eccentricity, orbit_incl, long_asc_node, long_perihelion, \
           true_anomaly, radius_vector





def calculate_coords(radius_vector, long_asc_node, true_anomaly, long_perihelion, I):
    # Calculating planet x heliocentric coordinate
    try:
        planet_x = radius_vector * (math.cos(to_radians(long_asc_node))
                                         * math.cos(
                    to_radians(true_anomaly + long_perihelion - long_asc_node))
                                         - math.sin(to_radians(long_asc_node))
                                         * math.sin(
                    to_radians(true_anomaly + long_perihelion - long_asc_node))
                                         * math.cos(to_radians(I)))
        # Calculating planet y heliocentric coordinate
        planet_y = radius_vector * (math.sin(to_radians(long_asc_node))
                                         * math.cos(
                    to_radians(true_anomaly + long_perihelion - long_asc_node))
                                         + math.cos(to_radians(long_asc_node))
                                         * math.sin(
                    to_radians(true_anomaly + long_perihelion - long_asc_node))
                                         * math.cos(to_radians(I)))

        return round(planet_x, 4), round(planet_y, 4)

    except Exception:
        print('Error')



