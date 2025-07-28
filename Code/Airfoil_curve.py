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

# ----------------------------------------
# Python Libraries
# ----------------------------------------

# import os
# import subprocess
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import hsv_to_rgb
# from tqdm import tqdm
# from celluloid import Camera
# from FilePath import FilePath
# import WriteResults as WR

# -------------------------------------------
#     AIRFOIL CURVE
# -------------------------------------------
# Parametric equations are generated for the curve (x,y):
# Args:
#
#  t:       Generates the airfoil-parallel curves. It's sufficent to be in the
#           interval [0,2*PI] or [-PI,PI].
#
#  mu:      Generates the airfoil-orthogonal curves. It must be defined in an
#           interval of positive numbers: [0,|a|]. mu=0 returns the airfoil.
#
#  epsilon: This parameter controls the airfoil thickness and must be a
#           positive real number. (suggestion: keep it in the range: 0-0.3)
#
#  phi:     This parameter controls the airfooil's curvature and must be
#           between -np.pi < phi < np.pi
#
#  c:       Defines the airfoil's chord

def xcoord(t, mu, epsilon, phi, c):
    '''
     Defines the x coordinate of the airfoil
    '''
    numer = c*((1+mu)*(np.cos(t)+epsilon*np.cos(t-phi))-epsilon*np.cos(phi))
    denom = ((1+mu)**2)*(1+epsilon**2 + 2*epsilon*np.cos(phi)) - 2 * \
        epsilon*(1+mu)*(np.cos(t+phi)+epsilon*np.cos(t)) + epsilon**2

    return numer*(1+1/denom)

def ycoord(t, mu, epsilon, phi, c):
    '''
    Defines the y coordinate of the airfoil
    '''
    numer = c*((1+mu)*(np.sin(t)+epsilon*np.sin(t-phi))+epsilon*np.sin(phi))
    denom = ((1+mu)**2)*(1+epsilon**2 + 2*epsilon*np.cos(phi)) - 2 * \
        epsilon*(1+mu)*(np.cos(t+phi)+epsilon*np.cos(t)) + epsilon**2

    return numer*(1-1/denom)

def airfoil(t, mu, epsilon, phi, c):
    '''
    The following function generates the airfoil curve. 
    It relies on the previous two functions for the coords
    '''
    x = xcoord(t, mu, epsilon, phi, c)
    y = ycoord(t, mu, epsilon, phi, c)

    return [x, y]

                                                                                                                         
# -------------------------------------------
#           AIRFOIL CURVE (LINEARIZED)
# -------------------------------------------
# The following function generates a linealized version of the airfoil
# Works the same as the previous one and parameters have the same meaning.
# The two will be similar for epsilon < 0.3

def xcoord_lin(t, mu, epsilon, phi, c):
    '''
    Generates the x coordiante of a linearized version of the airfoil
    '''
    numer = 2*c*(np.cos(t) + epsilon*(np.cos(t-phi)-np.cos(phi) +
                 (np.cos(t+phi)-np.cos(phi))*np.cos(t)))

    return numer

def ycoord_lin(t, mu, epsilon, phi, c):
    '''
    Generates the y coordiante of a linearized version of the airfoil
    '''
    numer = 2*c*epsilon*(np.cos(phi)-np.cos(t+phi))*np.sin(t)

    return numer

def airfoil_lin(t, mu, epsilon, phi, c):
    '''
    Generates the  a linearized version of the airfoil
    '''
    x = xcoord_lin(t, mu, epsilon, phi, c)
    y = ycoord_lin(t, mu, epsilon, phi, c)

    return [x, y]


# -------------------------------------------
#           AIRFOIL MANIPULATION
# -------------------------------------------
# Here we define functions to rotate, traslate or reescale the airfoil

def trasl_2D(x, y, x0, y0):
    '''
    Function to traslate the curve (2D)
    '''
    return[x0 + x, y + y0]

def trasl_3D(x, y, z, x0, y0, z0):
    '''
    Function to traslate the curve (3D)
    '''
    return [x0 + x, y0 + y, z0 + z]

def rotate_2D(x, y, theta):
    '''
    Function to 2D-rotate the curve in the x-y plane:
    The input MUST BE in degrees. You can change it to radians deactivating
    the first line
    '''
    theta = np.pi*theta/180
    xr = x*np.cos(theta) + y*np.sin(theta)
    yr = -x*np.sin(theta) + y*np.cos(theta)
    return [xr, yr]

def rotate_3D(x,y,z,theta,n):
    '''
    Function to 3D-rotate the curve (Uses Olinde-Rodrigues Formula)
    ** Notation: ^n --> Unit vector, _r --> Vector, 
                < _a , _b > --> Scalar product, _a * _b --> Vector product
    _r_rot = cos(theta)_r + (1-cos(theta))< ^n , _r > ^n + sin(theta)(^n * _r)

    Args:
    Coords [x,y,z]
    Angle theta
    Rotation pseudovector n = [nx,ny,nz]
    '''
    # In case the vector is not a numpy
    n = np.array(n)

    # Test that the vector is 3-dimensional
    if (len(n)!=3):
        print("Normal vector should have 3 components but {} were given" \
              .format(str(len(n))))
        
        return 0
    else:
    # Make the vector unitary
        n_mag = n[0]**2 + n[1]**2 + n[2**2]
        for i in range(len(n)):
            n[i] = n[i]/n_mag

    # Compute the scalar product
        proy = n[0]*x + n[1]*y + n[2]*z

    # Compute the vector product components
        nr_x = z*n[1] - y*n[0]
        nr_y = x*n[2] - z*n[1]
        nr_z = y*n[0] - x*n[2]
    
    # Compute the new coordiantes
        xr = np.cos(theta)*x +(1-np.cos(theta))*proy*n[0] + np.sin(theta)*nr_x
        yr = np.cos(theta)*y +(1-np.cos(theta))*proy*n[1] + np.sin(theta)*nr_y
        zr = np.cos(theta)*z +(1-np.cos(theta))*proy*n[2] + np.sin(theta)*nr_z

        return [xr,yr,zr]

def reescale_2D(x, y, fx, fy):
    '''
    Function to reescale the curve
    '''
    return [x*fx, y*fy]

def test():

    t = np.linspace(-np.pi,np.pi,1800) # Curve parameter (1000 points)
    # t = np.linspace(0,2*np.pi,1000) # Curve parameter (1000 points)

    mu = 0.02 # Parallel curve (To avoid the singularity for mu=0)
    epsilon = 0.18 # Airfoil thickness
    phi = 2*np.pi/7 # Airfoil curvature
    c = 1 # Chord 
    
    amp = c/100 # Amplitude of the oscillations
    amp = c/40 # Amplitude of the oscillations
    omega = 50 # Frequency

    [x0,y0] = airfoil(t,mu,epsilon,phi,c)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)

    # plt.plot(x0,y0,color=[0,0,0],linewidth = 1)
    plt.xlim([-3.4,3.1])
    plt.ylim([-1.25,1.25])
    
    plt.show()

# test()