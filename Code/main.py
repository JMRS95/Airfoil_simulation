'''
--------------------------------------------------------------------------------
         MAIN FILE
--------------------------------------------------------------------------------
________________________________________________________________________________
Code by José Miguel Raygoza Serment. IIUNAM, Mexico.

For details mail to:
      jmrs@ciencias.unam.mx
      jmrayser@gmail.com
________________________________________________________________________________

The following code is intented to automate OpenFOAM simulations based on a 
base case directory. It simulates the flow around different airfoil geometries
that were generated using a parametric curve. It allows to vary the thickness,
curvature, angle of attack among other parameters.

The code is open for free usage. 

'''
# Python libraries
import os
import numpy as np
from PIL import Image

# Created libraries 
from FilePath import FilePath
import Airfoil_data as a_data
import Airfoil_simulation as a_sim

def run_all_simple(Read :FilePath,Case:FilePath,t,mu,epsilon,phi,c,alpha,i):
    '''
        Works only for an unperturbed airfoil for now....
        1. Converts airfoil curve to .csv (Code in airfoil_3D_csv)
        2. Uses Paraview to convert .csv to .extl and save the file
        3. Runs the simulation with the current airfoil
    '''
    # Data airfoil coords --> .csv ---> .stl
    a_data.airfoil_to_stl_pv(Read,t,mu,epsilon,phi,c,alpha,i)

    a_sim.run_simple(Case,i,False)

    return None


def run_all_pimple(Read :FilePath,Case:FilePath,t,i):

    # Data airfoil coords --> .csv ---> .stl
    a_data.data_adquisition(Read,t,i)

    a_sim.run_pimple(Case,i)

    return None


def main():
    '''
        Main program
    '''

    # Set the coordinates
    t = np.linspace(0,2*np.pi,400)

    # Set the Code path ()
    Read = FilePath()
    Read.linux_unit()
    Read.set_complete_path("F","Maestria","Airfoil","Code")

    # Set the simulation case
    Case = FilePath()
    Case.linux_unit()
  
    # Img case
    Img = FilePath()
    Img.linux_unit()
    Img.set_complete_path("F","Maestria","Airfoil","Simulations")


    # Ortogonal coordinate
    mu = 0.02

    # Thickness
    epsilon = 0.1

    # Curvature
    phi = 0

    # Chord
    c = 1

    # Angle of attack (in degrees)
    alpha = 15

    # Number of iterations
    N = 1

    # Index for iterarations
    i = 0

    # Loop
    while i <= N:
        
        Read.set_complete_path("F","Maestria","Airfoil","Code")
        Case.set_complete_path("F","Maestria","Airfoil/Simulations",str(i))


        path = Read.path()

        # Perturbed airfoil ---
        # Case.SubFolder2="P_"+str(index)
    
        # alpha = -20 +40*(i/N)         # ANGLE OF ATTACK
        epsilon = 0.025 + 0.275*(i/N)     # THICKNESS
        phi = 0 + np.pi/3*(i/N)         # PHI
        if (N==0):
            epsilon = 0.05    # THICKNESS
            phi = 0         # PHI     

        run_all_simple(Read,Case,t,mu,epsilon,phi,c,alpha,i)

        binroot = "/mnt/c/Program Files/ParaView 5.11.1/bin"
        os.chdir(binroot)

        print("\nProducing the screenshots of the visualization...\n")
        os.system("./pvbatch.exe " + 
              "F:\\Maestria\\\Airfoil\\\Code\\\Paraview_postprocess.py")
    
        os.chdir(Case.path())

        # a_data.set_index(index)
        i += 1
    
    i = 0
    while i <= N:
        image_path = Img.set_complete_path("F","Maestria","Airfoil",
                              "Simulations/"+str(i)+"/postProcessing/U_2.png")
        img = Image.open(image_path)
        img.show()
        i+=1

    return 0

main()
