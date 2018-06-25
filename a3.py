import pygeodesy
from pygeodesy import ellipsoidalVincenty as ev


def storm_distance(coords:list) -> (float, float):
    """Computes and ouputs total distance the storm moved

    :param coords: A list containing the ellapsed time and coordinates from the previous
    storm location to the current
    :return: the distance in miles as a float
    >>>storm_distance([6.0, '15.0N', '59.0W', '16.0N', '60.6W'])
    (204584.77333140429, 302.74119499532304)
    """
    loc1 = myLatLon(coords[1], coords[2])
    loc2 = myLatLon(coords[3], coords[4])
    return loc1.distanceTo3(loc2)[0], loc1.distanceTo3(loc2)[2]



def flip_direction(direction: str) -> str:
    """Given a compass direction 'E', 'W', 'N', or 'S', return the opposite.
    Raises exception with none of those.
    :param direction: a string containing 'E', 'W', 'N', or 'S'
    :return: a string containing 'E', 'W', 'N', or 'S'
    >>> flip_direction('E')
    'W'
    >>> flip_direction('S')
    'N'
    >>> flip_direction('SE')  # test an unsupported value
    Traceback (most recent call last):
    ...
    ValueError: Invalid or unsupported direction SE given.
    """
    if direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'N'
    else:
        raise ValueError('Invalid or unsupported direction {} given.'.format(direction))


def myLatLon(lat: str, lon: str) -> ev.LatLon:
    """Given a latitude and longitude, normalize the longitude if necessary,
    to return a valid ellipsoidalVincenty.LatLon object.
    :param lat: the latitude as a string
    :param lon: the longitude as a string
    >>> a = ev.LatLon('45.1N', '2.0E')
    >>> my_a = myLatLon('45.1N', '2.0E')
    >>> a == my_a
    True
    >>> my_b = myLatLon('45.1N', '358.0W')
    >>> a == my_b  # make sure it normalizes properly
    True
    >>> myLatLon('15.1', '68.0')
    LatLon(15°06′00.0″N, 068°00′00.0″E)
    """

    if lon[-1] in ['E', 'W']:
        # parse string to separate direction from number portion:
        lon_num = float(lon[:-1])
        lon_dir = lon[-1]
    else:
        lon_num = float(lon)
    if lon_num > 180.0:  # Does longitude exceed range?
        lon_num = 360.0 - lon_num
        lon_dir = flip_direction(lon_dir)
        lon = str(lon_num) + lon_dir

    return ev.LatLon(lat, lon)


def hours_elapsed(ts1: str, ts2:str) -> float:
    """Given 2 strings containing dates & clock times,
    return the number of elapsed hours between them
    (as a float).

    :param ts1: date & 24-hr time as a string like '20160228 1830'
    :param ts2: date & 24-hr time as a string like '20160228 2200'
    :return: elapsed hours between ts1 & ts2, as a float.
     >>> hours_elapsed('20160228 1830', '20160228 2200')
    3.5
    >>> hours_elapsed('20160229 1815', '20160301 0000')
    5.75
    >>> # this confirms timestamp order doesn't matter:
    >>> hours_elapsed('20160301 0000', '20160229 1800')
    6.0
    """

    # TODO: Implement this function
    pass


def storm_propogation(y):
    """Calculates the speed, in knots, for each storm sample, based on coordinates and time, then calculates the
    mean and maximum speed and outputs those quantities

    :param y:
    :return:
    """
    pass


def test_hypothesis(z):
    """Computes the bearing of the storm, then checks the highest level of non-zero radii to see if it is in the
    quadrant 45-90 degrees from the bearing. If so, it returns true, otherwise returns false

    :param z:
    :return:
    """
    high_wind_is_in_range = False
    return high_wind_is_in_range


def main():
    """

    :return:
    """
    pass


if __name__ == '__main__':
    main()