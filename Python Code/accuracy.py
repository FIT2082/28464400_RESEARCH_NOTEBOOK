# Author: Surayez Rahman
# Created On: 18th Sept, 2018
# Topic: Auto Regressive Model

# References:
# https://www.youtube.com/watch?v=o7Ux5jKEbcw
# https://machinelearningmastery.com/grid-search-arima-hyperparameters-with-python/

import scipy.io
import numpy as np
import pandas as pd
import warnings
import scipy.signal as Pysignal
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
import statsmodels
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error



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

    return bounds_array

def plot_matrix(matrix):
    plt.pcolor(matrix)
    plt.gca().invert_yaxis()
    plt.show()


def current_forecast(day_data_matrix, updated_order, training_list, train_size,  prev_index, updated_matrix, day):
    train, actual_data = day_data_matrix[prev_index:prev_index + train_size], day_data_matrix[prev_index + train_size]
    new_train_list = [x for x in train]
    temp_train_list = []
    if len(training_list) == 0:
        temp_train_list = new_train_list

    # ARIMA
    try:
        if len(training_list) == 0:
            model = ARIMA(temp_train_list, order= updated_order)
        else:
            model = ARIMA(training_list, order=updated_order)
        model_fit = model.fit(disp=0)
        current_prediction = model_fit.forecast()[0]
        if (abs(current_prediction - actual_data) < 0.6 ):
            if len(training_list) != 0:
                # print(new_train_list[-1])
                if new_train_list[-1] != 10:
                    training_list.append(new_train_list[-1])
            else:
                for each in new_train_list:
                    if each != 10:
                        training_list.append(each)
        else:
            updated_matrix[prev_index][day] = 10
            # day_data_matrix[prev_index][day] = 10

        # print(train, training_list)
    except:
        print("Incompatible order:", updated_order)
        pass
    return training_list


def run_one_house(mat, mat2):
    day_ranges = []
    time_ranges = []

    # mat = scipy.io.loadmat(house, squeeze_me=True)

    # Get variable array rect as rect
    rect = mat['rect']
    # Get variable array image as matrix
    matrix = mat2['image']

    # Find the bounding data from rect
    current_bounds_array = find_bounds(rect, day_ranges, time_ranges)

    # Converts data into array (each array = 1 time slot, index(item) = day
    # find_rect_edge(matrix, 5)

    # Plot the edges detected from the rect array
    add_rect_edges(matrix, current_bounds_array)

    return matrix

def accuracy_check(saved_matrix, predicted_matrix):
    accurate_number_of_edges = 0
    predicted_number_of_edges = 0

    for times in range(0, 48):
        for days in range(0, 360):
            if saved_matrix[times][days] == 10:
                accurate_number_of_edges += 1

    for times in range(0, 48):
        for days in range(0, 360):
            if predicted_matrix[times][days] == 10:
                if saved_matrix[times][days] == 10:
                    predicted_number_of_edges += 1

    for times in range(0, 48):
        for days in range(0, 360):
            if saved_matrix[times][days] == 10:
                if predicted_matrix[times][days] != 10:
                    predicted_number_of_edges -= 1

    return (predicted_number_of_edges/accurate_number_of_edges)*100

if __name__ == "__main__":
    # Getting actual data as saved_matrix
    house_number = "00002"
    saved_house_data = scipy.io.loadmat('data/saved_rect' + house_number + '.mat', squeeze_me=True)
    temp_house_data = scipy.io.loadmat('data/house' + house_number + '.mat', squeeze_me=True)
    saved_matrix = run_one_house(saved_house_data, temp_house_data)
    # plot_matrix(saved_matrix)

    # Getting ARIMA predicted data as predicted_matrix
    house_data = scipy.io.loadmat('data/house' + house_number + '.mat', squeeze_me=True)
    matrix = house_data['image']
    matrixlist = np.squeeze(np.matrix(matrix)).tolist()
    matrix_Df = pd.DataFrame(matrixlist)
    training_list = []

    updated_matrix = matrix_Df.as_matrix()
    updated_order = (0, 0, 0)
    training_data_size = 4

    warnings.filterwarnings("ignore")

    number_of_days = 360
    total_hours = 48

    for days in range(number_of_days):
        day_data_matrix = matrix_Df[days].as_matrix()
        for hours in range(total_hours - training_data_size):
            # training_list = current_forecast(day_data_matrix, updated_order, training_list , training_data_size, hours, updated_matrix, days)

            train, actual_data = day_data_matrix[hours:hours + training_data_size], day_data_matrix[hours + training_data_size]
            new_train_list = [x for x in train]
            temp_train_list = []
            if len(training_list) == 0:
                temp_train_list = new_train_list

            # ARIMA
            try:
                if len(training_list) == 0:
                    model = ARIMA(temp_train_list, order=updated_order)
                else:
                    model = ARIMA(training_list, order=updated_order)
                model_fit = model.fit(disp=0)
                current_prediction = model_fit.forecast()[0]
                if (abs(current_prediction - actual_data) < 0.6):
                    if len(training_list) != 0:
                        # print(new_train_list[-1])
                        if new_train_list[-1] != 10:
                            training_list.append(new_train_list[-1])
                    else:
                        for each in new_train_list:
                            if each != 10:
                                training_list.append(each)
                else:
                    updated_matrix[hours+3][days] = 10
                    # print('UPDATED')

                # print(current_prediction, actual_data, current_prediction - actual_data, training_list)

            except:
                print("Incompatible order:", updated_order)
                pass

    predicted_matrix = []
    for item in updated_matrix:
        # item = ndImage.filters.minimum_filter1d(item, 50)
        item = Pysignal.medfilt(item, [11])
        predicted_matrix.append(item)

    plot_matrix(predicted_matrix)

    print("The accuracy of edge detection:", accuracy_check(saved_matrix, predicted_matrix))
