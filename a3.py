from pygeodesy import ellipsoidalVincenty as pg


def storm_distance(point_a: pg.LatLon, point_b: pg.LatLon) -> float:
    """Computes and outputs the distance the storm moved between point_a and point_b

    :param point_a: A LatLon object defined in pygeodesy package. The first parameter is Latitude and second is Longitude
    :param point_b: A LatLon object defined in pygeodesy package. The first parameter is Latitude and second is Longitude
    :return: The distance between point_a and point_b as a float in nautical miles
    """
    # If two points are the same, return 0 as distance. Otherwise throw exception
    if point_a == point_b:
        return 0

    # If two points are different, calculate distance
    else:
        distance = point_a.distanceTo(point_b)/1852.0
        return distance


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


def add_summary(current_year, year_storm, year_hur, summary):
    """

    :param sum:
    :return:
    """
    if year_storm != 0:
        if current_year in summary.keys():
            summary[current_year] = summary[current_year][0] + year_storm, summary[current_year][1] + year_hur
        else:
            summary[current_year] = year_storm, year_hur
    return summary


def process_file(f,summary: list) -> list:
    """Takes the file opened and process the file line by line

    :param f: the file connection that takes the file to read
    :param summary: a list that takes the summary data of processed storms of another file
    :return: a list of summarized data for all storms in the file
    """
    # define all variables that will be used throughout the function
    i = 1           # An indicator of current line for the storm. Reset to 1 after each storm
    j = 0           # An indicator of how many lines each storm has. Reset to 0 after each storm
    date_start = 0  # Start date of the current storm.
    date_end = 0    # End date of the current storm
    max_wind = 0    # Maximum wind recorded for the current storm
    max_date = 0    # The date of which the maximum wind is recorded for the first time
    max_time = ''   # The time of which the maximum wind is recorded for the first time
    landfall = 0    # Landfall indicator. 1 is added each time a landfall occurs. Reset to 0 after each storm
    s = []          # A list of data from the current storm processing. Reset to empty list after each storm
    storm = []      # A list of all storms processed
    current_year = 0    # The year that the storm in process is in. Changes when the year changes
    hur_ind = 0     # Hurricane indicator. Turns to 1 if the storm is a hurricane. Reset to 0 after each storm.
    year_storm = 0  # Number of storms in this year. Reset to 0 for each new year
    year_hur = 0    # Number of hurricanes in this year. Reset to 0 for each new year
    a = pg.LatLon   # Stores the LatLon data of the previous line
    dist = 0.00     # Total distance travelled by each storm. Reset to 0.00 after each storm

    # Read one line from the file
    for line in f:

        # Split the line into list of elements. A comma will follow every value parsed from the line
        values_on_line = line.split()

        # Reads the header line of a storm
        if j == 0:

            # Read storm ID and name and storm in list s
            s = [values_on_line[0].replace(",", ""), values_on_line[1].replace(",", "")]
            if s[1] == 'UNNAMED':
                s[1] = ''   # Remove the name if it is unnamed

            # Read the number of lines for this storm
            try:
                j = int(values_on_line[2].replace(",", ""))
            except ValueError:
                j = 0

        # Reads the observed data of a storm
        else:

            # Counts landfall if occurred
            if values_on_line[2].replace(",", "") == 'L':
                landfall += 1

            # Process the line as the first line of a storm's records
            if i == 1:
                # Takes the time of the maximum wind
                max_time = values_on_line[1].replace(",", "")

                # Records the coordinate read from this line and stores as a LatLon object
                a = pg.LatLon(values_on_line[4].replace(",",""),values_on_line[5].replace(",",""))

                # Reads the date information and wind speed on this line
                try:
                    date_start = int(values_on_line[0].replace(",", ""))
                    date_end = int(values_on_line[0].replace(",", ""))
                    max_wind = int(values_on_line[6].replace(",", ""))
                    max_date = int(values_on_line[0].replace(",", ""))
                except ValueError:
                    date_start = 0
                    date_end = 0
                    max_wind = 0
                    max_date = 0

                # Find the year of this storm
                year = int(date_start/10000)

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

            else:   # Reads a line that is not the first line of a storm

                # Records the coordinate read from this line and stores as a LatLon object
                b = pg.LatLon(values_on_line[4].replace(",", ""), values_on_line[5].replace(",", ""))

                # Add the distance travelled by the storm between current and previous point
                dist += storm_distance(a,b)

                # Set the current point as previous point for next line
                a = b

                # Take the date, time, and wind speed of this line
                try:
                    date = int(values_on_line[0].replace(",", ""))
                    wind = int(values_on_line[6].replace(",", ""))
                except ValueError:
                    date = date_end
                    wind = max_wind
                time = values_on_line[1].replace(",", "")

                # Compare the wind speed to previously recorded maximum wind speed
                # If the new wind speed is greater, record this new speed and date & time occurred
                if wind > max_wind:
                    max_wind = wind
                    max_date = date
                    max_time = time
                if date > date_end:
                    date_end = date

                # If detected as a hurricane, change hurricane indicator to 1
                if values_on_line[3].replace(",", "") == 'HU':
                    hur_ind = 1

            # Reached the last line of this storm.
            if i == j:

                # Record the date as the end date
                try:
                    date_end = int(values_on_line[0].replace(",", ""))
                except ValueError:
                    continue

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

    # Return the list of storms
    return storm


def main():
    """ The main function that will be executed first

    :return:
    """

    # Define an empty dictionary to store summary from both datasets
    sum = {}

    # Process first file
    with open('hurdat2-1851-2017-050118.txt', 'r') as fi:
        process_file(fi,sum)

    # Process second file
    with open('hurdat2-nepac-1949-2017-050418.txt', 'r') as fi:
        process_file(fi,sum)

    # Print the summary data by year
    print(sum)


if __name__ == '__main__':
    main()