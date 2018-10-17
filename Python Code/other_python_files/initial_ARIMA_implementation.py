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

# # evaluate an ARIMA model for a given order (p,d,q)
# def evaluate_arima_model(current_list, arima_order, prev_index):
#     # prepare training dataset
#     train_size = 3
#     train, test = current_list[prev_index:train_size], current_list[train_size:train_size + 1]
#     history = [x for x in train]
#
#     # Make predictions
#     prediction = 0
#     for t in range(len(test)):
#         model = ARIMA(history, order=arima_order)
#         model_fit = model.fit(disp=0)
#         y_hat = model_fit.forecast()[0]
#         prediction = y_hat
#         history.append(test[t])
#
#     # calculate out of sample error
#     error = mean_squared_error(test, prediction)
#     return error
#
#
# # evaluate combinations of p, d and q values for an ARIMA model
# def evaluate_models(dataset):
#     warnings.filterwarnings("ignore")
#     p_values = [0, 1, 2, 4, 6]
#     d_values = range(0, 3)
#     q_values = range(0, 3)
#
#     best_score, best_cfg, prev_index = float("inf"), None, 0
#     for p in p_values:
#         for d in d_values:
#             for q in q_values:
#                 order = (p,d,q)
#                 try:
#                     mse = evaluate_arima_model(dataset, order, prev_index)
#                     if mse < best_score:
#                         best_score, best_cfg = mse, order
#                     prev_index += 1
#                     print('ARIMA%s MSE=%.3f' % (order,mse))
#                 except:
#                     continue
#     print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
#     final_cfg = best_cfg
#
#     return final_cfg

def plot_matrix(matrix):
    plt.pcolor(matrix)
    plt.gca().invert_yaxis()
    plt.show()

def current_forecast(day_data_matrix, updated_order, training_list, train_size,  prev_index, updated_matrix, day):
    train, actual_data = day_data_matrix[prev_index:prev_index + train_size], day_data_matrix[prev_index + train_size]
    new_train_list = [x for x in train]
    temp_train_list = training_list + new_train_list

    # ARIMA
    try:
        model = ARIMA(temp_train_list, order= updated_order)
        model_fit = model.fit(disp=0)
        current_prediction = model_fit.forecast()[0]
        if (abs(current_prediction - actual_data) < 0.6 ):
            for each in new_train_list:
                if each != 10:
                    training_list.append(each)
        else:
            updated_matrix[prev_index + 1][day] = 10

    except:
        print("Incompatible order:", updated_order)
        pass
    return training_list


if __name__ == "__main__":
    # Loading Data
    data = scipy.io.loadmat('data/house00002.mat', squeeze_me=True)
    matrix = data['image']
    matrixlist = np.squeeze(np.matrix(matrix)).tolist()
    matrix_Df = pd.DataFrame(matrixlist)
    training_list = []

    updated_matrix = matrix_Df.as_matrix()
    updated_order = (0, 0, 0)
    training_data_size = 4

    warnings.filterwarnings("ignore")

    for days in range(20):
        day_data_matrix = matrix_Df[days].as_matrix()
        for hours in range(47 - training_data_size):
            training_list = current_forecast(day_data_matrix, updated_order, training_list , training_data_size, hours, updated_matrix, days)

    final_matrix = []
    for item in updated_matrix:
        # item = ndImage.filters.minimum_filter1d(item, 50)
        item = Pysignal.medfilt(item, [11])
        final_matrix.append(item)

    plot_matrix(final_matrix)
    plot_matrix(matrixlist)
