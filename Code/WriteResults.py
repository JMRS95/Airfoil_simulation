# ***********************************************************************************
# MODULE FOR WRITING THE "log" FILES FROM THE FILES
# ***********************************************************************************
'''
This file will write for each Case Files for easy PostProcessing and Graphing
variables that OpenFOAM didn't print during simulation:

- In each Folder I will put these in:

# First I'll change the forceCoeffs, forces and Moments to this new folder which I'll create in a function
- Case{}/PostProcessing/Graphing
'''

# ---------------------------------------------------------
# LIBRARIES
# ---------------------------------------------------------

from FilePath import FilePath
import numpy as np
import linecache
import os
import sys
import shutil
from ReadFiles import *  # (Deacticvate to test it)


# ---------------------------------------------------------
# CREATE THE PATH FOR EACH FOLDER
# ---------------------------------------------------------
def PostProcessing_newpath(Write):
    Prb = os.path.exists(Write.path())
    if (Prb):
        print("\tDirectory: {} alredy exists\n".format(Write.path()))
    else:
        os.mkdir(Write.path())
        print("\tDirectory {} created\n".format(Write.path()))

# ---------------------------------------------------------
# DELETE THE PATH FOR EACH FOLDER (BETTER NOT USE IT)
# ---------------------------------------------------------
# CAUTION:
# This deletes the path and ALL ITS CONTENTS


def PostProcessing_deletepath(Write):
    # SECURE VERSION (SLOWS PROGRAM IF LOOPING)
    ''' 
    #print("Enter 0 to remove the directory")
    #b = input("Do yo want to remove it? ")
    #if(b == "0"):
          # FOR SECURITY OF BAD TYPING 
          #b = input("Are you sure? (Press 0) ")
          #if(b == "0"):
                #R = os.path.exists(Write.path())
                #if (not R):
                #      print("Current directory doesn't exist.")
                #else:
                #      shutil.rmtree(Write.path())
                #      print("Directory {} Removed\n".format(Write.path()))
          #else:
    #            print("Diretory {} kept\n".format(Write.path()))      
    #else:
    #      print("Diretory {} kept\n".format(Write.path()))
    '''

    # UNSECURE VERSION (CAUTION!)
    # Much better for looping but be careful beacause there's no going back
    R = os.path.exists(Write.path())
    if (not R):
        print("\tCurrent directory doesn't exist.\n")
    else:
        shutil.rmtree(Write.path())
        print("\tDirectory {} Removed\n".format(Write.path()))


# ---------------------------------------------------------
# CREATE THE FILE FOR EACH FOLDER
# ---------------------------------------------------------
# NOT RECOMENDED FOR LOOPING
# Requires:
#     1.    FilePath() object
#     2.    File's name
def PostProcessing_newfile(Write: FilePath, file: str):
    Write.File = file
    filename = Write.file_path(file)
    Write_exists = os.path.exists(Write.path())
    if (not Write_exists):
        print("\tCurrent directory doesn't exist.\n")
        print("\tCreating directory {}\n" .format(Write.path()))
        os.mkdir(Write.path())
    else:
        Prb = os.path.isfile(filename)
        if (Prb):
            print("\tFile: {} alredy exists in {}\n".format(
                Write.File, Write.path()))
            print("\tRewriting to file....\n")
        else:
            print("\tCreating file {} in {}\n".format(Write.File, Write.path()))
            with open(filename, "w") as new:
                print(" ")
            print("\tFile {} created in {}\n".format(Write.File, Write.path()))


# ---------------------------------------------------------
# DELETE THE FILE FOR EACH FOLDER
# ---------------------------------------------------------
def PostProcessing_deletefile(Write, file: str):
    Write.File = file
    filename = Write.file_path(file)
    Write_exists = os.path.exists(Write.path())
    if (not Write_exists):
        print("\tDirectory {} doesn't exist.\n".format(Write.path()))
    else:
        Prb = os.path.isfile(filename)
        if (Prb):
            print("\tRemoving file: {}  in {}\n".format(
                Write.File, Write.path()))
            os.remove(filename)
        else:
            print("\tFile {} doesn't exist in {}\n".format(
                Write.File, Write.path()))


# ---------------------------------------------------------
# FORMATTING
# ---------------------------------------------------------
# This is defined to give format to the written file
# Requires:
def fileformat(
        arg: tuple, # Tuple of string
        Sep: str, # Delimiter
        N): # Number of columns
    init = ""
    finl = "\n"
    idx = init  # index
    if (len(arg) != 0):
        for i in range(N-1):
            # for i in range(len(arg)-1):
            idx += str(arg[i]) + Sep
        idx += str(arg[N-1]) + finl
        # h = idx.split(",")
        # k = idx.strip()
        # print(h)
        return idx
    else:
        list(arg)
        for i in range(N-1):
            # for i in range(len(arg)-1):
            g += str(arg) + Sep
        g += str(arg[N-1]) + finl
        print(g)
        return g


# ---------------------------------------------------------
# WRITE EXTRACTED DATA
# ---------------------------------------------------------
# Works with both: log, .dat files

def write_extracted(Write: FilePath, Fromlog: tuple):
    writefile = Write.file_path(Write.File)
    print(writefile)
    Prb = os.path.isfile(writefile)
    if (Prb):
        print("\tWriting to file: {}\n" .format(writefile))
        with open(writefile, "w") as postProcessfile:
            Col_Title = np.array(Fromlog[0]) #Title
            Col_Data = np.array(Fromlog[1]) #Column
            # Col_Data = Col_Data.transpose() #This differs in the other file
            N = len(Col_Data)
            # postProcessfile.write(fileformat(Col_Title, ",", len(Col_Title)))
            print(fileformat(Col_Title, ",", len(Col_Title)),
                  file=postProcessfile, end="")
            # for j in range(4):
            for j in range(N):
                # postProcessfile.write("\n")
                # postProcessfile.write (fileformat(Col_Data[j], ",", len(Col_Title)))
                postProcessfile.write(fileformat(
                    Col_Data[j], ",", len(Col_Title)))
        print("\tFinished writing {} \n".format(writefile))

    else:
        print("\tWriting failed\n {} doesn't exist..\n".format(writefile))


# ---------------------------------------------------------
# CREATE AND WRITE THE DATA:
# ---------------------------------------------------------
# This creates and writes files at once:
def write_newfile(Write: FilePath, file: str, Fromlog: tuple):
    PostProcessing_newfile(Write, file)
    write_extracted(Write, Fromlog)


# ********************************************
#            TESTING
# ********************************************

# -------------------------------------------
# Path and file creation and destruction
# -------------------------------------------
'''
A =FilePath()
B =FilePath()

# Setting the path
A.set_complete_path("F", "Case9", "Extra", "")
B.set_complete_path("F", "Case9", "Extras", "")

# We create the path
PostProcessing_newpath(A)

# We create file in the path
PostProcessing_newfile(A,"Try")

# Another file is created
PostProcessing_newfile(A,"Try2")

# Deleting a file that doesn't exist in path: 
#     Program prints that the file doesn't exist
PostProcessing_deletefile(A,"Try3")

# Deleteing an existing file in a path that wasn't created: 
#     Program prints that path doesn't exist
PostProcessing_deletefile(B,"Try2")

# Deleting an existing file in the path
PostProcessing_deletefile(A, "Try2")

# Deleting all path the directory (PLEASE BE CAREFUL USING THIS)
PostProcessing_deletepath(A)

# Deleting a non existent directory
PostProcessing_deletepath(B)
'''


# ---------------------------
# LOG FILE
# ----------------------------
def testlog():
    # PFOLDER's name:
    Name = "Case"  # Folders
    index = 9
    Number = str(index)
    Folder = Name + Number
    Unit = "F"
    myCPU = True
    if (myCPU):
        Unit = "E"

    # READ FILEPATH OBJECT
    Read = FilePath()
    # Read.set_complete_path("F",Folder, "","") # UNAM CPU
    Read.set_complete_path(Unit, Folder, "", "")  # my CPU

    selector = 0
    strselector = str(selector)
    options = ["test1GeneratorsRAS", "test1GeneratorsLES",
               "test2GeneratorsRAS", "test2GeneratorsLES"]

    print("Select the your file to test")
    print("Options:")
    for j in options:
        strselector = str(selector)
        print("Option {}:\t {}".format(strselector, j))
        selector += 1
    while True:
        try:
            strselector = input()
            selector = int(strselector)
        except (ValueError):

            print("Unknown option")
        if ((selector < 0 or selector > 3)):
            print("Number out of range")
        else:
            readfilename = options[selector]
            break

    Multiple = True

    if (selector == 0 or selector == 1):
        Multiple = False
    a = read_logfile(Read, readfilename, Multiple)

    print(type(a))
    print(type(a[0]), type(a[1]))

    # WRITE FILEPATH OBJECT
    Write = FilePath()

    # SINCE IT'S IN THE SAME DIRECTORY WE ONLY DEFINE ITS subFolders NAME
    SubFolder1 = "PostProcessing"
    SubFolder2 = "Graphing"
    Write.set_complete_path(Unit, Folder, SubFolder1, SubFolder2)

    # THIS PROCESS WILL AUTOMATICALLY WRITE THE ENTIRE LOGFILE TO A NEW ONE
    # First we create the file in the directory then we write file

    ext = ".csv"
    copy = ""
    writename = options[selector] + copy + ext

    # PostProcessing_newfile(Write, writename)
    # write_extracted(Write, a, writename)
    write_newfile(Write, writename, a)

    # PostProcessing_newpath(Write)
    # PostProcessing_deletepath(Write) ! This asks user to delete

    Ttl = np.array(a[0])
    Var = np.array(a[1])
    print("1st arguement: {}" .format(Ttl))
    print("2nd arguement: {}" .format(Var))
# testlog()


# ----------------------------------------
# .dat FILES
# ----------------------------------------

def testdat():
    Unit = "E"
    Name = "Case"
    index = 9
    Number = str(index)
    Folder = Name + Number
    SubFolder1 = "postProcessing"

    ForceCoeffs_Dir = "forceCoeffs1\\0"
    Force_Dir = "forces\\0"
    Anex = [ForceCoeffs_Dir, Force_Dir]
    ForcesFile = ["coefficient", "force", "moment"]
    ext = [".dat", ".csv"]
    ReadFOAM = FilePath()

    ReadFOAM.set_complete_path(Unit, Folder, SubFolder1, Anex[0])
    ReadFOAM.File = ForcesFile[0] + ext[0]
    ReadFOAM.locate_file()
    readfile = ReadFOAM.File

    b = read_dat(ReadFOAM, readfile)

    Writecsv = FilePath()
    Writecsv.set_complete_path(Unit, Folder, SubFolder1, "Graphing")
    ext = ".csv"
    Writecsv.File = ForcesFile[0] + ext
    file = Writecsv.File
    # PostProcessing_newfile(Writecsv, file)
    write_newfile(Writecsv, file, b)

# testdat()


# +++++++++++++++++++++++++++++++++++
# SUGGESTIONS:
# +++++++++++++++++++++++++++++++++++
'''
1.    Write to inidividual files:
            * Time vs Angular velocity
            * Time vs Residuals
      Instead of writing everything in the same file, for memory optimizations

2.    Define a writing_format function which takes:
      Tuple of data

'''


# log_File = FilePath()
# Unit = "F"
# log_File.set_complete_path(Unit,"Maestria","Cases", "Case20")
# log_File.File = "log"

# log_File.locate_file()
# readfile = log_File.File
# PostProcessing_newfile(log_File,readfile + ".csv")

# a = read_logfile(log_File, readfile,False)

# Write = FilePath()
# Write.set_complete_path(Unit,"Maestria\Cases\Case20","postProcessing","Graphing")
# ext = ".csv"
# readfile = readfile + ext
# #PostProcessing_newfile(Write, readfile)
# write_newfile(Write,readfile,a)
