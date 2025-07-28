# ****************************************************************************
# MODULE FOR EXTRACTING THE NECESSARY DATA FROM THE LOG FILE
# ****************************************************************************
'''
This file allows the user to extract from the Openfoam's log file the 
following:
- Times
- Angular Velocity
- Resiudals ()
'''

# ---------------------------------------------------------
# LIBRARIES
# ---------------------------------------------------------

from FilePath import FilePath
import numpy as np
import os


# ---------------------------------------------------------
# TO DELETE THE FINAL CHARACTER IN A STRING
# ---------------------------------------------------------
def delete_final(X: str):
    n = len(X)
    newFloat = float(X[0:n-1])

    return newFloat


# ---------------------------------------------------------
# TO DELETE THE FIRST CHARACTER IN A STRING
# ---------------------------------------------------------
# Here I don't call this function but it's programmed just in case
def delete_initial(X: str):
    n = len(X)
    newFloat = float(X[1:n])

    return newFloat


# ---------------------------------------------------------
# EXTRACT THE INFORMATION FROM THE LOG
# ---------------------------------------------------------
# This will extract the following:
# Times
# Angular Velocity
# Resiudals (Be Aware of the LES MOdel)
def extract_log(logfile: str, # Name of the log file
                condition: bool # Condition to know if 
                                # there are 1 or 2 generators
                ):

    # 1. WE DEFINE THE VARIABLES TO BE EXTRACTED

    # Time
    Time = []
    Time_Title = "Time"

    # * If there's only one generator
    AngularVelocity = []
    AV_Title = "Angular_Velocity"

    # * When there are two generators
    AngularVelocity1 = []
    AV1_Title = "Angular_Velocity_1"

    AngularVelocity2 = []
    AV2_Title = "Angular_Velocity_2"

    # Residuals present in my log (PIMPLE)
    # Pressure (p)
    Psr_Residual = []
    Psr_Title = "Psr_Residual"

    # Turbulent kinetic energy (k)
    # ** In some LES models, the residual present is the 
    #    turbulent viscosity (nuTilda)
    TKE_Residual = []
    TKE_Title = "TKE_Residual"

    # Turbulence dissipation (epsilon in K-Epsilon, omega in K-Omega)
    # * This is only present in some RAS models. AWARE!
    Dis_Residual = []
    Dis_title = "Dis_Residual"

    # This line checks if the model is LES, (log changes)
    lES = "Selecting turbulence model type LES"
    condition_Not_LES = True

    # This lines are the ones that will be searched in the log file
    VarName = ["Time =", "Angular velocity", "PIMPLE: iteration 3"]

    # Condition is passed as an argument to the function. 
    # It is used to disntinguish if the program has
    # 1 or 2 generators as shown below:
    if (condition):
        Title = (Time_Title, AV1_Title, AV2_Title,
                 Psr_Title, TKE_Title, Dis_title)
        Variables = (Time, AngularVelocity1, AngularVelocity2,
                     Psr_Residual, TKE_Residual, Dis_Residual)
        counter = 0 
    else:
        Title = (Time_Title, AV_Title, Psr_Title, TKE_Title, Dis_title)
        Variables = (Time, AngularVelocity, Psr_Residual,
                     TKE_Residual, Dis_Residual)

    # 2. THE PROGRAM STARTS TO READ THE FILE
    for line in logfile:

        # If the model line is found
        if (lES in line):
            condition_Not_LES = False

        # Time Variable
        if (VarName[0] in line and "Execution" not in line):
            crop1 = line.strip(VarName[0])
            crop2 = crop1.split()
            Time.append(float(crop2[0]))

        # Angular Velocity Variable(s)
        if (VarName[1] in line):
            # This will execute only if 2 generators are present
            crop1 = line.strip(VarName[1])
            crop2 = crop1.split()
            if (condition):
                if (counter % 2 == 0):
                    AngularVelocity1.append(float(crop2[2]))
                else:
                    AngularVelocity2.append(float(crop2[2]))
                counter += 1
            else:
                # crop2[1] = crop2[1].replace("(","")
                AngularVelocity.append(float(crop2[2]))

        # Residuals
        if (VarName[2] in line):

            # Pressure residual:
            for i in range(0, 2):
                R_Aux = logfile.readline()
            crop1 = R_Aux.strip(VarName[2])
            crop2 = crop1.split()
            crop2[11] = delete_final(crop2[11])
            Psr_Residual.append(float(crop2[11]))

            # Dissipation residual (Epsilon or Omega)
            if (condition_Not_LES):
                for i in range(0, 2):
                    R_Aux = logfile.readline()
                crop1 = R_Aux.strip(VarName[2])
                crop2 = crop1.split()
                crop2[11] = delete_final(crop2[11])
                Dis_Residual.append(float(crop2[11]))

            else:
                Dis_Residual.append("NaN")

            # TKE residual
            R_Aux = logfile.readline()
            crop1 = R_Aux.strip(VarName[2])
            crop2 = crop1.split()
            crop2[11] = delete_final(crop2[11])
            TKE_Residual.append(float(crop2[11]))

    # 3. WE CONVERT OUR LIST TO A NUMPY ARRAY AND TRANPOSE THE DATA
    Variables = np.array(Variables)
    Variables = Variables.transpose()

    # To protect our arrays to be altered in a following file,
    # we convert them to a tuple.
    Title = tuple(Title)
    Variables = tuple(Variables)
    return (Title, Variables)


# ---------------------------------------------------------
# TO READ THE LOG FILE
# ---------------------------------------------------------
# Reads the log file from the openFOAM case
# Works with:
#     - 1st argument: A FilePath object to set the path of our file
#     - 2nd argument: The file's name we want to read ("log" in my case)
#     - 3rd argument: If we want One or Two generators in the log file.
#                     Set to true for 2 generators, and false for 1
#                     (Please see the extract log file)
def read_logfile(Read: FilePath, filename: str, condition: bool):

    # 1. We set our path and name
    readfile = Read.file_path(filename)
    Prb = os.path.isfile(readfile)

    # 2. Checks if file exists or not, to avoid closing
    if (Prb):
        print("\tReading: {}..." .format(readfile))
        with open(readfile, "r") as logfile:
            print("\tExtracting data from {} ..." .format(readfile))

            # We save in a variable the extracted data from log
            Info = extract_log(logfile, condition)
        print("\tClosing: {}\n".format(readfile))

        # We return that saved information
        return Info
    else:
        # Nothing to do ....
        print("\tFailed reading: {}\nFile doesn't exist".format(filename))


# ---------------------------------------------------------
# EXTRACT FROM THE .dat FILES FROM OPENFOAM
# ---------------------------------------------------------
# This extract files ".dat" from OpenFOAM cases
# In my case is used for the following:
#     - forces in PostProcessing/forces directory
#     - moments in PostProcessing/forces directory
#     - forceCoeffs1 in PostProcessing/forces directory
def extract_dat(datfile: str):

    # 1. WE SET VARIABLES

    # Title of the columns
    Col_Title = []

    # Data to be extracted
    Data = []

    # Auxiliar variables for reading file
    init = 0  # Set an initial position for reading data
    counter = 0  # Counter1 --> 
    N = 0  # Counter2 --> Number of data files

    # In open foam the columns titles begin with this name
    # so we search for it:
    Var = "# Time"

    # 2. WE START READING THE FILES
    for line in datfile:

        Number = str(N)
        N += 1
        counter += 1
        if (Var in line):

            # This is auxilar and tells user when the line "# Time"
            # was found
            print("Found {} in line {}: " .format(Var, Number))

            # Here we get the columns title
            chop1 = line.strip()
            chop2 = chop1.split()
            Col_Title = chop2[1:]  # We remove the "#" in the file

            # We set our initial number to the line the Title was found
            init = N

            # We increase the count by one
            counter += 1

    # 3. NOW WE EXTRACT THE DATA BELOW THE COLUMN'S TITLE:
        # Because counter = N+1 from now on, 
        # and N > init when the cycle repeats.
        # This will be executed
        if (counter > N & N > init):
            chop1 = line.strip()
            chop2 = chop1.split()
            Data.append(chop2)

    # 4. RETURN
    return (Col_Title, Data)


# ---------------------------------------------------------
# TO READ THE .dat FILES FROM OPENFOAM
# ---------------------------------------------------------
# Reads a ".dat" file from OpenFOAM
# Works with:
#     - 1st argument: A FilePath object to set the path of our file
#     - 2nd argument: The file's name we want to read ("log" in my case)
#
def read_dat(Read: FilePath, filename: str):

    readfile = Read.file_path(filename)
    print("\tFile:\t{}\n" .format(readfile))
    Prb = os.path.isfile(readfile)
    if (Prb):
        print("\tReading: {}..." .format(readfile))
        with open(readfile, "r") as datfile:
            print("\tExtracting data from {} ..." .format(readfile))

            # In this line differs from the read_logfile() function
            Info = extract_dat(datfile)

        print("\tClosing: {}\n".format(readfile))
        return Info
    else:
        print("\tFailed reading: {}\nFile doesn't exist".format(filename))

    # LOOK THAT THIS IS QUITE SIMILAR FROM THE read_logfile
    # so it could be merged with that one in fact.


# ********************************************
#            TESTING
# ********************************************
def test():
    Read = FilePath()
    Read.set_complete_path("F", "Maestria", "Cases", "Case20")  
    print(Read)
    #filename = "test2GeneratorsLES"
    filename = "log"
    a = read_logfile(Read, filename, False)
    #a[0] ---> Tuple of titles, a[1] ---> Tuple of datas
    for i in range(len(a[0])):
        for j in range(3):
            # for j in range(len(a[1][0])):
            print("{} : {}" .format(a[0][i], a[1][i][j]), end = "\t")
    print("\n",a[1][0])
#test()

