'''
--------------------------------------------------------------------------------
            CODE TO MANAGE AIRFOIL'S DATA
--------------------------------------------------------------------------------
________________________________________________________________________________
Code by José Miguel Raygoza Serment. IIUNAM, Mexico.

For details mail to:
      jmrs@ciencias.unam.mx
      jmrayser@gmail.com
________________________________________________________________________________

The following code allows to export the airfoil coordinates to a .csv filed
using a paraview script, to 

(Recommended to run using Ubuntu's Shell.)
'''

import os
import subprocess
import shutil
import numpy as np
import matplotlib.pyplot as plt
from FilePath import FilePath
import WriteResults as WR
import Airfoil_curve as air


# -------------------------------------------
# WRITE TO .csv THE AIRFOIL (2D)
# -------------------------------------------
def write_csv_2D(x,y,i,cond:bool):
    '''
    This function pulls off the airfoil coordinates 
    & writes them in a .csv file

    An extra argument "i" as an index to iterate is used.
    The bool condition will be true if the airfoil is perturbed
    '''
    # 1. FILE DEFINITION
    # Define the path:
    csv_path=FilePath()

    # Set if you run from Windows or Ubuntu (WSL virtual machine...)
    #csv_path.windows_unit() # If windows is used
    csv_path.linux_unit() # If linux is used

    # Set the current path
    csv_path.set_current_path()

    # Or, if you want, set a path you'd like. For example:
    csv_path.set_complete_path("F/Maestria","Airfoil","PreProcessing","Points2D")

    # Set the name of the file to be written
    number = str(i) # To string
    csv_path.File = "Airfoil_" + number + "_Coords" + ".csv"

    if(cond):
        csv_path.File = "P_Airfoil_" + number + "_Coords" + ".csv"

    # Create a newfile (Creates path if it doesn't exist...)
    WR.PostProcessing_newfile(csv_path,csv_path.File)

    # We allocate in 2 lists our data
    Data_x = []
    Data_y = []

    #x[0] = x[2*np.pi] and so on,  and we don't want repeated points
    for j in range(len(x)):
        Data_x.append(x[j]) 
        Data_y.append(y[j])


    # Convert data to numpy
    Data = np.array([Data_x,Data_y])

    # Transpose the data to get the desired array.
    Data = Data.transpose()

    # N = Length of Data (Returns the number of rows)
    N = len(Data)

    # Now we set the column Titles
    Title = np.array(("x","y"))

    # Write_them in a csv.
    writefile = csv_path.file_path(csv_path.File)
    
    # Check if file exists, then write the points
    Prb = os.path.isfile(writefile)
    if (Prb):
        with open(writefile, "w") as postProcessfile:
            print(
                WR.fileformat(
                    Title, # Column's title
                    ",", # Delimiter
                    len(Title)), # Number of columns
                file=postProcessfile # Where to write
                ,end="") # End column
            for k in range(1):
                for j in range(N):
                    postProcessfile.write(
                        WR.fileformat(
                        Data[j],  # Writes the data
                        ",", # Delimiter
                        len(Title)))


# -------------------------------------------
# WRITE TO .csv THE AIRFOIL (3D)
# -------------------------------------------
def write_csv_3D(x,y,i,cond:bool):
    '''
    This function pulls off the airfoil coordinates 
    & writes them in a .csv file

    An extra argument "i" as an index to iterate is used
    The bool condition will be true if the airfoil is perturbed
    '''
    # 1. FILE DEFINITION
    # Define the path:
    csv_path=FilePath()

    # Set if you run from Windows or Ubuntu (WSL virtual machine...)
    #csv_path.windows_unit() # I use Windows
    csv_path.linux_unit() # If linux is used

    # Set the current path
    csv_path.set_current_path()

    # Or, if you want, set a path you'd like. For example:
    csv_path.set_complete_path("F/Maestria","Airfoil","PreProcessing","Points3D")

    # Set the name of the file to be written
    number = str(i) # To string
    csv_path.File = "Airfoil_" + number + "_Coords" + ".csv"

    # Create a newfile (Creates path if it doesn't exist...)
    WR.PostProcessing_newfile(csv_path,csv_path.File)

    # SETTING THE Z COORDINATE FOR A 3D EXTRUSION
    z = np.zeros(len(x)) # IN 2D We only need one division

    # We allocate in 3 lists our data
    Data_x = []
    Data_y = []
    Data_z = []

    #x[0] = x[2*np.pi] and so on,  and we don't want repeated points
    for j in range(len(x)):
        Data_x.append(x[j]) 
        Data_y.append(y[j])
        Data_z.append(z[j])


    # Convert data to numpy
    Data = np.array([Data_x,Data_y,Data_z])

    # Transpose the data to get the desired array.
    Data = Data.transpose()

    # N = Length of Data (Returns the number of rows)
    N = len(Data)

    # Now we set the column Titles
    Title = np.array(("x","y","z"))

    # Write_them in a csv.

    writefile = csv_path.file_path(csv_path.File)
    
    Prb = os.path.isfile(writefile)
    if (Prb):
        with open(writefile, "w") as postProcessfile:
            print(
                WR.fileformat(
                    Title, # Column's title
                    ",", # Delimiter
                    len(Title)), # Number of columns
                file=postProcessfile # Where to write
                ,end="") # End column
            for k in range(2):
                for j in range(N):
                    Data[j][2] = -0.1+0.2*k # To get 2 identical curves
                               # at different z planes.
                    postProcessfile.write(
                        WR.fileformat(
                        Data[j],  #Writes the data
                        ",", # Delimiter
                        len(Title)))     

# -------------------------------------------
#       EXTRACT .csv DATA
# -------------------------------------------
def extract_csv(csvfile:str):
    '''
    Extracts the [x,y,z] points of the airfoil 
    (The inverse of the previous function)
    '''
    # Columns & Data.
    Col_Title = []
    Data = []

    # Counter to read the .csv
    line_counter = 0

    for line in csvfile:

    # We split using the delimiter ","
        chop1 = line.strip()
        chop2 = chop1.split(",")

    # Extract the column titles
        if line_counter==0:
            Col_Title = chop2[0:]
            line_counter+=1

    # Extract the data
        else:
            for j in range(len(chop2)):
                chop2[j] = float(chop2[j])
            Data.append(chop2)

    return (Col_Title, Data)

# -------------------------------------------
#       READ CSV
# -------------------------------------------
def read_csv(Read:FilePath, filename:str):
    '''
    Reads the .csv file written. It uses the previous function
    '''

    # Here we'll save our column titles & data.
    Info = []

    # Set the path and locate the file
    readfile=Read.file_path(filename)
    Read.locate_file()

    # Boolean to check if file exists
    Prb:bool = os.path.isfile(readfile)

    if Prb :
    # Extract the data via the previous function
        print("\tReading: {}..." .format(readfile))
        with open(readfile, "r") as csvfile:
            print("\tExtracting data from {} ..." .format(readfile))
            Info = extract_csv(csvfile)

    return Info


# --------------------------------------------
# EXTRACT CSV FOR PARAVIEW
# --------------------------------------------

# --------------------------------------------
# FILE FOR PARAVIEW TO READ
# --------------------------------------------
def set_index(Read,index):
    '''
    Write a number that contains a number for paraview
    to read --> Automate
    '''
    # Read_Idx = FilePath()
    # Read_Idx.linux_unit()
    # Read_Idx.set_current_path()

    print("Setting the index to {} in file Index".format(index))
    print(Read.path())

    # File name --> Nmbr
    writefile = Read.file_path("Index")
    with open(writefile,"w") as setfile:
        print(index,file=setfile)


# -------------------------------------------
#       RUN PARAVIEW SHELL
# -------------------------------------------
def paraview_csv_stl_windows(Read:FilePath,i):
    '''
    Run paraview script from Windows powershell using
     (Obsolete)
    '''

    os.system(
        "C:\\\"Program Files\"\\\"ParaView 5.11.1\"\\bin\\pvpython.exe" + \
            Read.path() + "\\Paraview_csv_to_stl.py")
    print("Inside loop")

def paraview_csv_stl_linux(Read:FilePath,i):
    '''
    Run paraview script from Ubuntu virtual machine for Windows
    using pvbatvch (Recomended)
    '''

    binroot = "/mnt/c/Program Files/ParaView 5.11.1/bin"
    os.chdir(binroot)

    print("Converting Airfoil_{}_Coords.csv to Airfoil_{}.stl"
          .format(str(i),str(i)))
    os.system("./pvbatch.exe " + 
              "F:\\Maestria\\\Airfoil\\\Code\\\Paraview_csv_to_stl.py")
    
    os.chdir(Read.path())
    # Obsolete
    # os.system("./pvbatch.exe " + Read.path() + "/Paraview_csv_to_stl.py")


# GET THE CURVE AND OBTAIN AN STL
def airfoil_2D_csv(t,mu,epsilon,phi,c,i,amp,omega,cond:bool):
    '''
    Gets the points and writes them to .csv
    '''

    # Get the airfoil
    [x,y] = air.airfoil(t,mu,epsilon,phi,c)
    

    # Convert the data to .csv
    write_csv_2D(x,y,i,cond)


def airfoil_3D_csv(t,mu,epsilon,phi,c,alpha,i):
    '''d
    Gets the points and writes them to .csv
    '''

    # Get the airfoil
    [x,y] = air.airfoil(t,mu,epsilon,phi,c)
    [x,y] = air.rotate_2D(x,y,alpha)
    

    # Convert the data to .csv
    # 4th arg is set to False because in paraview the algorithm doesn't work
    # for a perturbed airfoil
    write_csv_3D(x,y,i,False)


def airfoil_to_stl_pv(Read,t,mu,epsilon,phi,c,alpha,i):

    # Get the coordinates
    airfoil_3D_csv(t,mu,epsilon,phi,c,alpha,i)

    # Set the index for Paraview to read (For writing the file)
    set_index(Read,i)

    # Use Paraview to convert to .stl
    paraview_csv_stl_linux(Read,i)
    



def test():
    '''
    Testing that everything works
    '''

    # Setting the domain of the airfoil
    # t = np.linspace(-np.pi,np.pi,1600) # (-Pi,Pi) (Unperturbed - Sliced)
    t = np.linspace(0,2*np.pi,1600) # (0,2*Pi) (Perturbed - Original pert)

    # Setting a looping index

    # Setting the path and Linux unit
    Read = FilePath()
    Read.linux_unit()
    Read.set_current_path()

    # While loop to change our airfoil --> Write csv --> Convert to .stl
    # using paraview

    mu = 0.02
    epsilon = 0.3
    phi = np.pi/4
    c = 1
    i = 2005
    omega = 60 #must be impair


    while (i == 2005):
        amp = (i-1999)*c/160
        cond = True

        [x,y] = air.airfoil(t,mu,epsilon,phi,c,amp,omega)
        write_csv_2D(x,y,i,cond)
        i+=1

    # f = air.perturb(t,amp,omega)
    # #print(f)
    # plt.plot(t,f)
    # plt.show()

    #airfoil_to_stl_pv(Read,t,mu,epsilon,phi,c,i)
    #i=0
    #copy_case(i)
    #copy_stl(i)
# test()


# t = np.linspace(-np.pi,np.pi,1800) # Curve parameter (1000 points)
# mu = 0.02 # Parallel curve (To avoid the singularity for mu=0)
# epsilon = 0.18 # Airfoil thickness
# phi = 2*np.pi/7 # Airfoil curvature
# c = 1 # Chord 
# amp = c/40
# omega = 50
# [x,y] = air.airfoil_perturbed(t,mu,epsilon,phi,c,amp,omega)
# write_csv_2D(x,y,3000,False)