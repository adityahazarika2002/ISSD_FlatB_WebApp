import os
from flask import Flask, render_template, request, redirect, url_for
from funcs import voltage_output, graph_plot, phi_dipole, trapezoidal_csv, trapezoidal_fun, input_function
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas




app = Flask(__name__)
app.secret_key = 'flatband hazarika'

@app.route("/", methods=["POST", "GET"])
def home():
    flatb_volt= ""
    pngImageB64String = ""
    radio = ""
    filename = ""
    eps_0 = 8.854*(10**-14)

    try:
        if request.method == "POST":
            print("post")

            tox = float(request.form.get("T_ox"))
            phim = float(request.form.get("Phi_m"))
            epsilonx = float(request.form.get("Epsilon_x"))
            option = str(request.form.get("select"))
            dipole = float(request.form.get("dipole"))
            radio = str(request.form.get("IDradio"))

            if radio == "csv":
                print("csv")
                f = request.files['file']
                f.save(f.filename) 
                filename = f.filename
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

                flatb_volt = float(phim) - float(phi_dipole(option, dipole)) - ((10**-4)*float(tox))*(1/(eps_0*float(epsilonx)))*trapezoidal_csv(f"{filename}")
                data_csv.close()
                os.remove(filename)
                

            else:
                print("function")
                function = str(request.form.get("function"))
                lowerlimit = int(request.form.get("lowerlimit"))
                upperlimit = int(request.form.get("upperlimit"))
                num_points = int(request.form.get("points"))

                x = np.linspace(float(lowerlimit), float(upperlimit), int(num_points))
                fig = plt.figure(figsize=(8, 5))
                plt.plot(x, input_function(x, function), label='Input Function')
                # Convert plot to PNG image
                pngImage = io.BytesIO()
                FigureCanvas(fig).print_png(pngImage)
        
                # Encode PNG image to base64 string
                pngImageB64String = "data:image/png;base64,"
                pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
                
                flatb_volt = float(phim) - float(phi_dipole(option, dipole)) - ((10**-4)*float(tox))*(1/(eps_0*float(epsilonx)))*trapezoidal_fun((10**-4)*float(lowerlimit), (10**-4)*float(upperlimit), int(num_points), function)
    except:
        return render_template("flatb.html", message="Please enter valid values")
    return render_template("flatb.html", flatb_volt=flatb_volt, image=pngImageB64String)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)