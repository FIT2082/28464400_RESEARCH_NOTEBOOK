import scipy.io
import numpy as np
import matplotlib.pyplot as plot

def find_edge(userData, val):
    for days in range(0, 365):
        current_day_array = []
        for hours in range(0,48):
            current_day_array.append(matrix[hours][days])
        current_day_sd = np.std(current_day_array)

        for hours in range(0,47):
            if abs(matrix[hours][days] - matrix[hours-1][days]) >= current_day_sd:
                matrix[hours][days] = val


    for days in range(0, 364):
        for hours in range(0, 48):
            if matrix[hours][days] == val and matrix[hours][days-1] == val:
                matrix[hours][days] = 10
                matrix[hours][days-1] = 10


data = scipy.io.loadmat('matlab.mat')
matrix = data['image']

#convert data into array (each array = 1 time slot, index(item) = day

# print(np.squeeze(np.matrix(matrix)))
find_edge(matrix, 5)

plot.pcolor(matrix) #plot
plot.gca().invert_yaxis()
plot.show()
