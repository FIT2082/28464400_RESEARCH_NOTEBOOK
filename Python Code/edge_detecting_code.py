import scipy.io
import scipy.ndimage as ndImage
import scipy.signal as Pysignal
import numpy as np
import math
import matplotlib.pyplot as plt

data = scipy.io.loadmat('data/house00003.mat')
matrix = data['image']
matrixlist = np.squeeze(np.matrix(matrix)).tolist()

#####################################################################################
### SECTION: Saved Rects Code
#####################################################################################

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

def find_rect_edge(matrix, val):
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

def run_one_house(mat):
    day_ranges = []
    time_ranges = []

    # mat = scipy.io.loadmat(house, squeeze_me=True)

    # Get variable array rect as rect
    rect = mat['rect']
    # Get variable array image as matrix
    matrix = mat['image']

    # Find the bounding data from rect
    current_bounds_array = find_bounds(rect, day_ranges, time_ranges)

    # Converts data into array (each array = 1 time slot, index(item) = day
    # find_rect_edge(matrix, 5)

    # Plot the edges detected from the rect array
    add_rect_edges(matrix, current_bounds_array)

    colormap(matrix)


#####################################################################################
def colormap(matrixlist):  # plotting
    plt.pcolor(matrixlist)
    plt.gca().invert_yaxis()
    plt.show()

def multiplot(start, ran):  # plotting multiple graphs (can be improved to edge multiple)
    for i in range(start, ran):
        data = scipy.io.loadmat(('data/house' + str(i).zfill(5)) + '.mat', squeeze_me=True)
        matrix = data['image']
        matrixlist = np.squeeze(np.matrix(matrix)).tolist()
        colormap(findedges(matrixlist, findmean(matrixlist, True)))
        run_one_house(data)

def findSD(matrixlist, eachday=False):
    # find the standard deviation of each time slot (per horizontal)
    if eachday == True:
        # if eachday is true, sd of each day
        matrixlist = np.swapaxes(matrixlist, 0, 1).tolist()
    SD = []
    for item in matrixlist:
        SD.append(np.std(item))
    return SD


def findVar(matrixlist, eachday=False):  # find the variance of each time slot (per horizontal)
    if eachday == True:
        matrixlist = np.swapaxes(matrixlist, 0, 1).tolist()
    var = []
    for day in matrixlist:
        var.append(np.var(day))
    return var


def findmean(matrixlist, eachday=False):  # find the mean of each time slot (per horizontal)

    if eachday == True:
        matrixlist = np.swapaxes(matrixlist, 0, 1).tolist()

    mean = []
    
    for day in matrixlist:
        mean.append(np.mean(day))

    return mean


def findmeansdratio(matrixlist, eachday=False):  # find the mean - standard deviation ratio of each time slot (per horizontal)
    if eachday == True:
        matrixlist = np.swapaxes(matrixlist, 0, 1).tolist()
    msr = []
    for day in matrixlist:
        msr.append(np.mean(day) / np.std(day))
    return msr


#####################################################################################

def findedges(matrixlist, varlist):
    matrix = []
    for item in matrixlist:
        # item = ndImage.filters.minimum_filter1d(item, 10)
        item  = Pysignal.medfilt(item, [99])

        matrix.append(item)

    matrix = np.swapaxes(matrix, 0, 1).tolist()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if abs(matrix[i][j] - matrix[i][j - 1]) > varlist[i] and matrix[i][j - 1] != 2:
                matrix[i][j] = 2
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 2:
                matrix[i][j] = 0

    return np.swapaxes(matrix, 0, 1).tolist()

#####################################################################################

def clean(matrixlist):  # remove noises
    pass

# Pysignal.medfilt(matrixlist)
# matrixlist = np.swapaxes(matrixlist,0,1).tolist()
multiplot(2, 4)