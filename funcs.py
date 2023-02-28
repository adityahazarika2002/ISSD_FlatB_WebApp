import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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

def phi_dipole(option, dipole):
    if option == "Phi_s":
        phi_di = float(dipole)
    elif option == "Na":
        phi_di = 4.05 + (1.12/2) + 0.026 * (np.log(float(dipole)/np.power(10,10)))
    return phi_di


def input_function(x, function):
    y = x*eval(function)
    return y

def trapezoidal_fun(lowerlimit, upperlimit, num_points, function):
    h = (upperlimit - lowerlimit) / num_points
    sum = 0.5 * (input_function(lowerlimit, function) + input_function(upperlimit, function))
    for i in range(1, num_points):
        sum += 2*input_function(lowerlimit + i * h, function)
    return sum * h/2

def voltage_output(radio, dipole, option, phim, tox, epsilonx, lowerlimit, upperlimit, num_points, filename, function):
    eps_0 = 8.854*(10**-14)

    if radio == "csv":
        volts = float(phim) - float(phi_dipole(option, dipole)) - ((10**-4)*float(tox))*(1/(eps_0*float(epsilonx)))*trapezoidal_csv(f"{filename}")
    elif radio == "func":
        volts = float(phim) - float(phi_dipole(option, dipole)) - ((10**-4)*float(tox))*(1/(eps_0*float(epsilonx)))*trapezoidal_fun((10**-4)*float(lowerlimit), (10**-4)*float(upperlimit), int(num_points), function)

    return volts

def graph_plot(radio, filename, lowerlimit, upperlimit, num_points, function):
    if radio == "csv":
        data_csv = open(f'{filename}', 'r')
        array = np.loadtxt(data_csv, delimiter=',')

        arrx = np.zeros(len(array))
        arry = np.zeros(len(array))
        for i in range(len(array)):
            arrx[i] = array[i][0]
            arry[i] = array[i][1]
        fig = plt.figure(figsize=(8, 5))
        plt.plot(arrx, arry, label='Experimental Data')

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
    
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String
        

    elif radio == "func":
        x = np.linspace(float(lowerlimit), float(upperlimit), int(num_points))
        fig = plt.figure(figsize=(8, 5))
        plt.plot(x, input_function(x, function), label='Input Function')
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
    
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String
        
        