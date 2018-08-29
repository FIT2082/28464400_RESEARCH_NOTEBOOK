# Author: Surayez Rahman and Adolphus Lee

import scipy.io
import numpy as np
import math
import matplotlib.pyplot as plot


def plot_histogram(hist_array, label):
    num_bins = 50
    plot.hist(hist_array, num_bins, label= label , facecolor='blue', alpha=0.5)
    plot.legend()
    plot.show()


def find_bounds(rect, day_ranges, time_ranges):
    # Bounds_array is created to return the bounds as an array
    bounds_array = []

    for bounds in rect:
        upper_bound = [bounds[0][0], bounds[0][1]]
        lower_bound = [bounds[0][2], bounds[0][3]]

        # Calculating the differences in the bounds obtained
        number_of_days = abs(float(upper_bound[0]) - float(lower_bound[0]))
        day_ranges.append(number_of_days)
        time_range = abs(float(upper_bound[1]) - float(lower_bound[1]))
        time_ranges.append(time_range)

        # Adding the bounds to the bounds_array
        bounds_array.append([bounds[0][0], bounds[0][1], bounds[0][2], bounds[0][3]])
        # print([bounds[0][0], bounds[0][1], bounds[0][2], bounds[0][3]]) tracke

        # Print the ranges of data obtained
        # print(time_range, "\t" , number_of_days)

    return bounds_array


def find_edge(matrix, val):
    for days in range(0, 365):
        current_day_array = []
        for hours in range(0,47):
            current_day_array.append(matrix[hours][days])
        current_day_sd = np.std(current_day_array)

        for hours in range(0,47):
            if (matrix[hours][days] - matrix[hours-1][days]) >= current_day_sd:
                matrix[hours][days] = val

            if (matrix[hours][days] - matrix[hours+1][days]) >= current_day_sd:
                matrix[hours][days] = val

    for days in range(0, 365):
        for hours in range(0, 47):
            if matrix[hours][days] == val and matrix[hours][days-1] == val:
                matrix[hours][days] = 10
                matrix[hours][days-1] = 10


def add_rect_edges(matrix, known_bounds):
    for bounds in known_bounds:
        start_day = math.floor(bounds[0])
        end_day = math.floor(bounds[2])
        start_time = math.floor(bounds[1])
        end_time = math.floor(bounds[3])

        if 0 <= int(start_day) <= 365 and 0 <= int(end_day) <= 365 and 0 <= int(start_time) <= 48 and 0 <= int(end_time) <= 48:
            # print(start_time, end_time, start_day, end_day)

            for times in range(int(start_time), int(end_time)):
                for days in range(int(start_day), int(end_day)):
                    matrix[times][days] = 10
    # print(known_bounds)

def plot_matrix(matrix):
    plot.pcolor(matrix)
    plot.gca().invert_yaxis()
    plot.show()


def run_all_house_data():
    day_ranges = []
    time_ranges = []

    for i in range(1, 3500):
        try:
            string1 = 'data/saved_rect'
            string2 = '.mat'
            dif = 24 - (len(string1) + len(string2) + len(str(i)))

            file_name = string1 + str(dif * "0") + str(i) + string2

            mat = scipy.io.loadmat(file_name, squeeze_me=True)

            # Get variable array rect as rect
            rect = mat['rect']

            # Find the bounding data from rect
            find_bounds(rect, day_ranges, time_ranges)

        except:
            pass

    plot_histogram(day_ranges, "Day Lengths")
    plot_histogram(time_ranges, "Time Ranges")


def run_one_house(house):
    day_ranges = []
    time_ranges = []

    mat = scipy.io.loadmat(house, squeeze_me=True)

    # Get variable array rect as rect
    rect = mat['rect']
    # Get variable array image as matrix
    matrix = mat['image']

    # Find the bounding data from rect
    current_bounds_array = find_bounds(rect, day_ranges, time_ranges)

    # Converts data into array (each array = 1 time slot, index(item) = day
    find_edge(matrix, 5)

    # Plot the edges detected from the rect array
    # add_rect_edges(matrix, current_bounds_array)

    # print(np.squeeze(np.matrix(matrix)))
    plot_matrix(matrix)
    plot_histogram(day_ranges, "Day Lengths")
    plot_histogram(time_ranges, "Time Ranges")

if __name__ == "__main__":

    ### Run the following function on one house ONLY
    run_one_house('data/house00002.mat')

    ### Run the following function on all houses
    # run_all_house_data()

    print("Complete")