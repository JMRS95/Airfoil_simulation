'''
--------------------------------------------------------------------------------
            CODE TO GET THE AIRFOIL COORDINATES
--------------------------------------------------------------------------------
________________________________________________________________________________
Code by José Miguel Raygoza Serment. IIUNAM, Mexico.

For details mail to:
      jmrs@ciencias.unam.mx
      jmrayser@gmail.com
________________________________________________________________________________

The following code generates and provides the coordinates of an airfoil
based on Joukowski transform

The code is open for free usage. 

'''

import os
import subprocess
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from tqdm import tqdm
from celluloid import Camera
from FilePath import FilePath
import WriteResults as WR
import Airfoil_curve as air

matplotlib.use('TkAgg')

# -------------------------------------------
#           PLOT THE AIRFOIL
# -------------------------------------------

def plot_airfoil(x,y):
    '''
    This function plots the airfoil for given thickness, curvature and chord length:
    div_t: Tells you how many points of the airfoil curve are gonna be taken.
    x,y may be obtained from the curve directly or using a .csv file
    '''

    # Test validity of arguments
    # if (div_t > 0 and epsilon >= 0 and 0 <= phi0 <= np.pi/2 and c >= 0):

    #     # Parametrizations for each curve
    #     t = np.linspace(0, 2*np.pi, div_t)

    # # Notice that mu = 0 in the airfoil function (It returns the airfoil's shape)
    #     [x, y] = air.airfoil(t, 0, epsilon, phi0, c)

    #     clr = [0, 0, 0]
    #     plt.plot(x, y,
    #              color=clr, linestyle="-")

    # else:
    #     print("Invalid argument(s) found!\n\n")
    #     if (div_t <= 0):
    #         print("Invalid value in 1st argument.\nNumber must be a positive integer.\n")
    #     if (epsilon <= 0):
    #         print("Invalid value in 2nd argument.\nNumber must be positive.\n")
    #     if (phi0 <= 0 or phi0 >= np.pi/2):
    #         print(
    #             "Invalid value in 3rd argument.\nNumber must be between 0 & pi/2 (90 deg).\n")
    #     if (c <= 0):
    #         print("Invalid value in 4th argument.\nNumber must be positive.\n")
    clr = [0,0,0]
    plt.plot(x,y,color=clr,linestyle = '')




# -------------------------------------------
#           PLOT THE PARALLEL CURVES
# -------------------------------------------
def plot_airfoil_parallel_curves(div_t: int, 
                                 epsilon, 
                                 phi0, 
                                 c, 
                                 grid_size,
                                 M: int):
    '''
    Plots the parallel curves to the airfoil
    Here x,y are NOT EXTRACTED, you must provide the airfoil coordinates
    using all its parameters to guarantee the parallel curves.

    extra Args from air.airfoil()
    div_t --> Number of divisions
    grid_size -->  Controls the extension of the grid
    M --> Number of curves to be plotted
    '''
    # Test validity of arguments
    if (div_t > 0 and epsilon >= 0 and 0 <= phi0 <= np.pi/2 
        and c >= 0 and grid_size > 0 and M > 0):

        # Parametrizations for each curve
        t = np.linspace(0, 2*np.pi, div_t)
        for i in range(M):

            [x, y] = air.airfoil(t, grid_size*i/M, epsilon, phi0, c)

    # The airfoil is colored black, other curves will be colored blue....
            if (i == 0):
                clr = [0, 0, 0]
            else:
                clr = [0, 0, 1]
            plt.plot(x, y,
                     color=clr, linestyle="-")

    else:
        print("Invalid argument(s) found!\n\n")
        if (div_t <= 0):
            print("Invalid value in 1st argument. \
                  \nNumber must be a positive integer.\n")
        if (epsilon <= 0):
            print("Invalid value in 2nd argument.\
                  \nNumber must be positive.\n")
        if (phi0 <= 0 or phi0 >= np.pi/2):
            print(
                "Invalid value in 3rd argument.\
                \nNumber must be between 0 & pi/2 (90 deg).\n")
        if (c <= 0):
            print("Invalid value in 4th argument.\
                  \nNumber must be positive.\n")
        if (grid_size <= 0):
            print("Invalid value in 5th argument.\
                  \nNumber a positive integer.\n")
        if (M <= 0):
            print("Invalid value in 6th argument.\
                  \nNumber a positive integer.\n")


# -------------------------------------------
#           PLOT THE ORTHOGONAL CURVES
# -------------------------------------------

def plot_airfoil_orthogonal_curves(div_t: int, 
                                   epsilon, 
                                   phi0,
                                   c,
                                   grid_size, 
                                   M: int):
    '''
    Similar to the previous function but we plot the orthogonal curves to the
    airfoil and their parallel curves. Like a conformal grid

    M ---> Number of orthogonal plots to be plotted
    '''

    # Test validity of arguments
    if (div_t > 0 and epsilon >= 0 and 0 <= phi0 <= np.pi/2 and c >= 0 and grid_size and M > 0):
        # Parametrizations for each curve
        t = np.linspace(0, grid_size, div_t)
        for i in range(M):

            # NORMAL
            [x, y] = air.airfoil(2*np.pi*i/M, t, epsilon, phi0, c)

            # PCOLORS
            if (i == 0):
                clr = [0.5, 0, 0]
            else:
                clr = [1, 0, 0]
            plt.plot(x, y,
                     color=clr, linestyle="-")


    else:
        print("Invalid argument(s) found!\n\n")
        if (div_t <= 0):
            print("Invalid value in 1st argument. \
                  \nNumber must be a positive integer.\n")
        if (epsilon <= 0):
            print("Invalid value in 2nd argument.\
                  \nNumber must be positive.\n")
        if (phi0 <= 0 or phi0 >= np.pi/2):
            print(
                "Invalid value in 3rd argument.\
                \nNumber must be between 0 & pi/2 (90 deg).\n")
        if (c <= 0):
            print("Invalid value in 4th argument.\
                  \nNumber must be positive.\n")
        if (grid_size <= 0):
            print("Invalid value in 5th argument.\
                  \nNumber a positive integer.\n")
        if (M <= 0):
            print("Invalid value in 6th argument.\
                  \nNumber a positive integer.\n")

# -------------------------------------------
#           PLOT THE COMPLETE GRID
# -------------------------------------------
def plot_both_airfoil_curves(div_t: int,
                             div_u: int, 
                             epsilon, 
                             phi0, 
                             c, 
                             paral_size, 
                             orth_size, 
                             Nx, 
                             Ny):
    '''
    Plots both curves for the complete grid

    extra Args:
    div_t ---> Number of divisions for parallel curves.
    div_u ---> Number of divisions for orthogonal curves.
    epsilon,phi0,c --> Come from air.airfoil() in Airfoil_curve and have the
                        same meaning.
    paral_size --> Extension of the orthogonal curves
    orth_size --> Extension of parallel curves (Inverted but come from the
                  previous functions....)
    Nx ---> Number of parallel curves
    Ny ---> Number of orthogonal curves
    ''' 
 
    plot_airfoil_parallel_curves(div_t, epsilon, phi0, c, orth_size, Nx)
    plot_airfoil_orthogonal_curves(div_u, epsilon, phi0, c, paral_size, Ny)


# -------------------------------------------
#           SAVE PLOT
# -------------------------------------------

def save_fig(plt_title: str, # title of the plot
            font_title_size: int, # Fontsize of the title
            xlim: list, # limits of x --> 2 list
            ylim: list, # limits of y --> 2 list
            save_title: str, # plot_saved title
            pxls: int): # Size of the figure
    '''
    Function to save the figure
    '''
    plt.title(plt_title, size=font_title_size)
    plt.xlim(xlim)
    plt.ylim(ylim)
    save_title
    path = "F:\\"
    path = path + save_title + ".png"
    plt.savefig(path,
                dpi=pxls,
                format='png',
                pad_inches=0.6
                )


# -------------------------------------------
#           ANIMATION
# -------------------------------------------
# TO BE EDITED
def save_animation():
    '''
    Function to save an animated figure
    '''
    fig = plt.figure()
    camera = Camera(fig)
    plt_title = r""
    N = 60
    plt.title(plt_title, size=20)
    plt.xlim([-3, 3])
    plt.ylim([-3, 3])
    # for i in range(N):
    #       plot_both_airfoil_curves(200,200,0.2,np.pi/2*(np.sin(np.pi*i/(N))**2),1,10,10,40,60)
    #       #plot_both_airfoil_curves(200,200,0.2*(np.sin(np.pi*i/(N))**2),np.pi/6,1,10,10,40,60)
    #       #plot_airfoil(400,0.1+0.2*(np.sin(np.pi*i/(2*N))**2),np.pi/3*(np.sin(np.pi*i/N)**2),1)
    #       camera.snap()

    for i in range(2*N):
        if i <= N:
            plot_both_airfoil_curves(
                200, 200, 0.2*(np.cos(np.pi*i/(N))**2), 0, 1, 10, 10, 40, 60)
        else:
            plot_both_airfoil_curves(
                200, 200, 0.2, np.pi/2*(np.sin(np.pi*i/(N))**2), 1, 10, 10, 40, 60)
        camera.snap()
    for i in range(2*N+1, 3*N):
        plot_both_airfoil_curves(200, 200, 0.2-0.1*(np.sin(np.pi*i/(N))**2),
                                 np.pi/4*(np.sin(np.pi*3*i/(N))**2), 1, 10, 10, 40, 60)
        camera.snap()

    animation = camera.animate()

    animation.save('F:\\airf.gif',
                   dpi=200,
                   )


# -------------------------------------------
#           TEST FUNCTION
# -------------------------------------------
def test():
    t = np.linspace(0,2*np.pi,400)
    # [x,y] = air.airfoil(t,0.0,0.2,np.pi/6,1)
    x = np.linspace(0,1,100)
    y = np.linspace(0,2,100)
    print(np.shape(x),np.shape(y))

    plot_airfoil(x,y)
    plot_airfoil_orthogonal_curves(100,0.2,np.pi/6,1,1,10)
    plot_airfoil_parallel_curves(100,0.2,np.pi/6,1,1,10)
    plt.show()


test()


