from pygeodesy import ellipsoidalVincenty as pg
from datetime import datetime


def storm_distance_bearing(point_a: pg.LatLon, point_b: pg.LatLon) -> list:
    """Computes and outputs the distance the storm moved between point_a and point_b

    :param point_a: A LatLon object defined in pygeodesy package. First parameter is Latitude and second is Longitude
    :param point_b: A LatLon object defined in pygeodesy package. First parameter is Latitude and second is Longitude
    :return: The distance between point_a and point_b as a float in nautical miles
    >>> storm_distance_bearing(pg.LatLon('0.0N', '90.0W'), pg.LatLon('0.0N', '90.0W'))
    [0, -1]
    """
    # If two points are the same, return 0 as distance. Otherwise throw exception
    if point_a == point_b:
        return [0, -1]

    # If two points are different, calculate distance and final bearing
    else:
        dist_bear = point_a.distanceTo3(point_b)
        return [dist_bear[0] / 1852.0, dist_bear[1]]


def test_hypothesis(bearing: float, wind_radii: list) -> int:
    """Computes the bearing of the storm, then checks the highest level of radii to see if it is in the quadrant
       90 degrees from the bearing. If so, it returns 1, otherwise returns 0. Returns -1 if radii is 0 or -999

    :param wind_radii: A list of 34-kt wind radii maximum extent in four quadrants (NE. SE, SW, NW)
    :param bearing: The bearing from the previous point.
    :return: 1 for following hypothesis; 0 for not following hypothesis; -1 for not enough data to test
    """
    max_radii = max(wind_radii)
    if max_radii == 0 or max_radii == -999:
        return -1
    if 0.0 <= bearing < 90.0:
        hypo = wind_radii[1]
    elif 90.0 <= bearing < 180:
        hypo = wind_radii[2]
    elif 180.0 <= bearing < 270.0:
        hypo = wind_radii[3]
    elif 270.0 <= bearing < 360.0:
        hypo = wind_radii[0]
    else:
        return -1
    if hypo == max(wind_radii):
        return 1
    else:
        return 0


def hours_elapsed(ts1: str, ts2: str) -> float:
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

    try:
        time1 = datetime.strptime(ts1, '%Y%m%d %H%M')
        time2 = datetime.strptime(ts2, '%Y%m%d %H%M')
        # the difference is in seconds, so divide by 3600 to get total hours
        if time1 > time2:
            difference = time1-time2
            return difference.total_seconds()/60/60
        elif time1 < time2:
            difference = time2-time1
            return difference.total_seconds()/60/60
        # if the 2 datetimes are equal
        else:
            return 0.0

    except ValueError:
        print("The values were not proper time and date values")


def storm_propogation(y):
    """Calculates the speed, in knots, for each storm sample, based on coordinates and time, then calculates the
    mean and maximum speed and outputs those quantities

    :param y:
    :return:
    """
    pass


def add_summary(current_year: int, year_storm: int, year_hur: int, summary: dict) -> list:
    """ Adds up the summary number of storms and hurricanes in each year

    :param summary: The current list of summary that will be processed
    :param year_hur: No. of hurricanes in current year
    :param year_storm: No. of storms in current year
    :param current_year: The year that will be processed
    :return: A processed list of summary
    """
    if year_storm != 0:
        if current_year in summary.keys():
            summary[current_year] = summary[current_year][0] + year_storm, summary[current_year][1] + year_hur
        else:
            summary[current_year] = year_storm, year_hur
    return summary


def cleanup_line(value_on_line: list) -> list:
    """ Removes the comma after each item in the list

    :param value_on_line: The list that has comma after each item
    :return: A list with commas removed and everything else remained
    """
    value = []
    for item in value_on_line:
        value.append(item.replace(",", ""))
    return value


def to_integer(x: str, default_output=0) -> int:
    """ Takes a string with only numbers and try to transform it into integer. Returns 0 if ValueError raises.

    :param default_output: Default output from the function if ValueError raises.
    :param x: The string to be transformed
    :return: The integer read from the input
    """
    try:
        x = int(x)
        return x
    except ValueError:
        return default_output


def process_file(f, summary: dict) -> list:
    """Takes the file opened and process the file line by line

    :param f: the file connection that takes the file to read
    :param summary: a list that takes the summary data of processed storms of another file
    :return: a list of summarized data for all storms in the file
    """
    # define all variables that will be used throughout the function
    i = 1  # An indicator of current line for the storm. Reset to 1 after each storm
    j = 0  # An indicator of how many lines each storm has. Reset to 0 after each storm
    date_start = 0  # Start date of the current storm.
    date_end = 0  # End date of the current storm
    max_wind = 0  # Maximum wind recorded for the current storm
    max_date = 0  # The date of which the maximum wind is recorded for the first time
    max_time = ''  # The time of which the maximum wind is recorded for the first time
    landfall = 0  # Landfall indicator. 1 is added each time a landfall occurs. Reset to 0 after each storm
    s = []  # A list of data from the current storm processing. Reset to empty list after each storm
    storm = []  # A list of all storms processed
    current_year = 0  # The year that the storm in process is in. Changes when the year changes
    hur_ind = 0  # Hurricane indicator. Turns to 1 if the storm is a hurricane. Reset to 0 after each storm.
    year_storm = 0  # Number of storms in this year. Reset to 0 for each new year
    year_hur = 0  # Number of hurricanes in this year. Reset to 0 for each new year
    a = pg.LatLon  # Stores the LatLon data of the previous line
    dist = 0.00  # Total distance travelled by each storm. Reset to 0.00 after each storm
    total_sample = 0  # Total number of cases that can be used in testing hypothesis
    total_true = 0  # Total number of cases that follows the hypothesis
    current_time = None

    # Read one line from the file
    for line in f:

        # Split the line into list of elements. A comma will follow every value parsed from the line
        values_on_line = line.split()
        values_on_line = cleanup_line(values_on_line)

        # Reads the header line of a storm
        if j == 0:

            # Read storm ID and name and storm in list s
            s = [values_on_line[0], values_on_line[1]]
            if s[1] == 'UNNAMED':
                s[1] = ''  # Remove the name if it is unnamed

            # Read the number of lines for this storm
            j = to_integer(values_on_line[2])

        # Reads the observed data of a storm
        else:

            # Counts landfall if occurred
            if values_on_line[2] == 'L':
                landfall += 1

            # Process the line as the first line of a storm's records
            if i == 1:
                # Takes the time of the maximum wind
                max_time = values_on_line[1]

                # Records the coordinate read from this line and stores as a LatLon object
                a = pg.LatLon(values_on_line[4], values_on_line[5])

                # Reads the date information and wind speed on this line
                date_start = to_integer(values_on_line[0])
                date_end = date_start
                max_date = date_start
                max_wind = to_integer(values_on_line[6])

                current_time = date_start

                # Find the year of this storm
                year = int(date_start / 10000)

                # If the year of this storm is not the same as the previous one, store information about previous year
                # into summary and start a new year
                if current_year < year:
                    add_summary(current_year, year_storm, year_hur, summary)

                    # Set variables to default
                    current_year = year
                    year_storm = 0
                    year_hur = 0

                # Count the storm of current year
                year_storm += 1

            else:  # Reads a line that is not the first line of a storm

                # Records the coordinate read from this line and stores as a LatLon object
                b = pg.LatLon(values_on_line[4], values_on_line[5])

                dist_bear = storm_distance_bearing(a, b)

                # Add the distance travelled by the storm between current and previous point
                dist += dist_bear[0]

                radii = [to_integer(item, -999) for item in values_on_line[8:12]]
                hypothesis = test_hypothesis(dist_bear[1], radii)

                if hypothesis == 1:
                    total_true += 1
                    total_sample += 1
                elif hypothesis == 0:
                    total_sample += 1

                # Set the current point as previous point for next line
                a = b

                # Take the date, time, and wind speed of this line
                date = to_integer(values_on_line[0], date_end)
                wind = to_integer(values_on_line[6], max_wind)
                time = values_on_line[1]

                # Compare the wind speed to previously recorded maximum wind speed
                # If the new wind speed is greater, record this new speed and date & time occurred
                if wind > max_wind:
                    max_wind = wind
                    max_date = date
                    max_time = time
                if date > date_end:
                    date_end = date

                # If detected as a hurricane, change hurricane indicator to 1
                if values_on_line[3] == 'HU':
                    hur_ind = 1

            # Reached the last line of this storm.
            if i == j:

                # Record the date as the end date
                date_end = to_integer(values_on_line[0], date_end)

                # Add all data recorded into list s
                s += [date_start, date_end, max_wind, max_date, max_time, landfall, float("{0:.2f}".format(dist))]

                # Print the data of this storm
                print(s)

                # Add data into the list of all storms
                storm.append(s)

                # Reset all variables
                i = 1
                j = 0
                landfall = 0
                year_hur += hur_ind
                year_storm += 1
                hur_ind = 0
                s = []
                dist = 0.00

            # If not reached last line, add i by 1
            else:
                i += 1

    # Add the summary data of the last year processed in the file
    add_summary(current_year, year_storm, year_hur, summary)

    print(total_true / total_sample)

    # Return the list of storms
    return storm


def main():
    """

    :return:
    """
    summary = {}

    with open('hurdat2-1851-2017-050118.txt', 'r') as fi:
        process_file(fi, summary)

    with open('hurdat2-nepac-1949-2017-050418.txt', 'r') as fi:
        process_file(fi, summary)

    print(sum)


if __name__ == '__main__':
    main()
