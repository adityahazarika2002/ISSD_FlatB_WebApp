import numpy as np

# Define the function to calculate area under the curve
def trapezoidal_csv(user_input):
    
    # Set up the parameters
    csv_filename = f"{user_input}"

    # Read data from csv file
    data_csv = open(f'{csv_filename}', 'r')
    array = np.loadtxt(data_csv, delimiter=',')

    area = 0
    for i in range(len(array)-1):
        h = (array[i+1, 0] - array[i, 0])
        area += (array[i, 1]*array[i, 0] + array[i+1, 1]*array[i+1, 0]) * (h / 2)
    return area
#print(trapezoidal_csv("csv_files/exp4b_final.csv"))