# Author: Surayez Rahman and Adolphus Lee

import scipy.io
import numpy as np
import math
import matplotlib.pyplot as plot


def find_bounds(rect):
    # Bounds_array is created to return the bounds as an array
    bounds_array = []
    for bounds in rect:
        upper_bound = [bounds[0][0], bounds[0][1]]
        lower_bound = [bounds[0][2], bounds[0][3]]

        # Calculating the differences in the bounds obtained
        number_of_days = abs(upper_bound[0] - lower_bound[0])
        time_range = abs(upper_bound[1] - lower_bound[1])

        # Adding the bounds to the bounds_array
        bounds_array.append([bounds[0][0], bounds[0][1], bounds[0][2], bounds[0][3]])

        # Print the ranges of data obtained
        # print(time_range, "\t" , number_of_days)

    return bounds_array


# def plot_histogram():


def find_edge(userData, val):
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


def add_rect_edges(known_bounds):
    for bounds in known_bounds:
        start_day = math.floor(bounds[0])
        end_day = math.floor(bounds[2])
        start_time = math.floor(bounds[1])
        end_time = math.floor(bounds[3])

        if 0 <= int(start_day) <= 365 and 0 <= int(end_day) <= 365 and 0 <= int(start_time) <= 48 and 0 <= int(end_time) <= 48:
            print(start_time, end_time, start_day, end_day)

            for times in range(int(start_time), int(end_time)):
                for days in range(int(start_day), int(end_day)):
                    matrix[times][days] = 10
    # print(known_bounds)


# Plotting the matrix
def plot_matrix(matrix):
    plot.pcolor(matrix)
    plot.gca().invert_yaxis()
    plot.show()


if __name__ == "__main__":
    mat = scipy.io.loadmat('house00003.mat', squeeze_me=True)

    # Get variable array rect as rect
    rect = mat['rect']
    # Get variable array image as matrix
    matrix = mat['image']

    # Find the bounding data from rect
    current_bounds_array = find_bounds(rect)

    # Converts data into array (each array = 1 time slot, index(item) = day
    # find_edge(matrix, 5)

    #Plot the edges detected from the rect array
    add_rect_edges(current_bounds_array)

    # print(np.squeeze(np.matrix(matrix)))
    plot_matrix(matrix)