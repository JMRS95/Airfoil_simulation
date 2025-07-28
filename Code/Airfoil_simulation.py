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

The following code is intented to automate OpenFOAM simulations based on a 
base case directory

The code is open for free usage. 

'''

import os
import shutil
import tempfile
from FilePath import FilePath

# --------------------------------------------
# COPY THE OPEN FOAM CASE TO A NEW DIRECTORY
# --------------------------------------------
def copy_case(i,cond):
    '''
    Copy the OpenFoam base case from a succesful previous run to a new case
    (We need to change the .stl geometry in each folder)
    '''
    # We have prepared a base case with all its directories
    Base = FilePath()
    Base.linux_unit()
    Base.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/base")

    # Copy the case to a new directory
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i))

    print(Trgt.path)
    Trgt_exists = os.path.exists(Trgt.path())
    if (not Trgt_exists):
        print("Current directory doesn't exist.\n")
        print("Copying the base directory to {}".format(Trgt.path()))
        os.system("cp -r "+Base.path()+" "+Trgt.path())
    else:
        print("Path alredy exists.\n")
        print("Copying contents....\n")
        os.system("cp -r "+Base.path()+"/* "+Trgt.path())
        

# -------------------------------------------
#       CREATING THE MESH WITH BLOCKMESH
# -------------------------------------------
def blockMesh(Case :FilePath):
    '''
    Runs blockMesh from the directory
    '''
    os.chdir(Case.path())

    print("Running blockMesh in {}\n" .format(Case.path()))
    os.system("blockMesh > blockMesh")
    print("Finished blockMesh in {}\n" .format(Case.path()))


    # Create the paraview case
    os.system("touch Case.foam")

    return None


# --------------------------------------------
# COPY THE .stl TO THE OPENFOAM CASE
# --------------------------------------------
def copy_stl(i,cond:bool):
    '''
    Copies the .stl file from the STL folder to the Foam Case
    '''
    file = "Airfoil_"+ str(i) + ".stl"

    # Original file location
    Org = FilePath()
    Org.linux_unit()
    Org.set_complete_path("F/Maestria",
                          "Airfoil",
                          "PreProcessing",
                          "Stl")
    org_file = Org.file_path(file)

    # Target file location (To be edited)
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/constant/triSurface")

    trgt_file = Trgt.file_path(file)

    # Copy the file
    print("\tCopying {} to {}\n".format(file,Trgt.path()))
    shutil.copyfile(org_file,trgt_file)


# --------------------------------------------
# EDIT THE .stl GEOMETRY IN THE
# surfaceFeatureExtractDict
# --------------------------------------------
def edit_sFE(Case:FilePath,i,cond):
    '''
    Edits the target geometry that appears in the surfaceFeatureExtractDict
    for snappyHexMesh to mesh
    '''

    # Original path
    Path = FilePath()
    Path.linux_unit()
    Path.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # Original file name
    orig_file_path = Path.file_path("surfaceFeatureExtractDict")

    # Target path (Same but python doesn't do deepcopying)
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # New file name (Provisional)
    new_file_path = Trgt.file_path("New")

    # Get the Airfoil key name from the base case
    orig_name = "Airfoil_0.stl" # EDIT

    # Define a new name for the airfoil key name in the file.
    # (See Airfoil_data.write_csv() & Airfoil_data.csv_to_stl()
    #  for details... )
    new_name = "Airfoil_"+ str(i) + ".stl"


    # Change the file (We create a copy of the old file --> Modify the copy \
    # --> Remove the file --> Change copy name to the original)
    print("Editing surfaceFeatureExtractDict in {}\n".format(Case.path()))
    with open(orig_file_path,"r") as basefile:
        with open(new_file_path, "w") as newfile:
            for line in basefile:
                newline = line
                if (orig_name in line):
                    newline = line.replace(orig_name,new_name)
                newfile.write(newline)

    os.remove(orig_file_path)
    shutil.move(new_file_path,orig_file_path)
    print("Finished editing surfaceFeatureExtractDict file in {}\n"
          .format(Case.path()))



# --------------------------------------------
# EDIT THE .stl GEOMETRY IN THE
# surfaceFeatureExtractDict
# --------------------------------------------
def surfaceFeatureExtract(Case: FilePath):
    '''
    Runs blockMesh from the directory
    '''
    os.chdir(Case.path())
    print("Running surfaceFeatureExtract in {}\n" .format(Case.path()))
    os.system("surfaceFeatureExtract > surfaceExtract")
    print("Finished surfaceFeatureExtract in {}\n" .format(Case.path()))
    return None 


# --------------------------------------------
# EDIT SNAPPYHEXMESH
# --------------------------------------------
def edit_snappyHexMesh(Case:FilePath,i,cond):

    # Original path
    Path = FilePath()
    Path.linux_unit()
    Path.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # Original file name
    orig_file_path = Path.file_path("snappyHexMeshDict")

    # Target path (Same but python doesn't do deepcopying)
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # New file name (Provisional)
    new_file_path = Trgt.file_path("New")

    # Get the Airfoil key name from the base case
    orig_name_stl = "Airfoil_0.stl" # EDIT
    orig_name_eMesh = "Airfoil_0.eMesh" # EDIT

    # Define a new name for the airfoil key name in the file.
    # (See Airfoil_data.write_csv() & Airfoil_data.csv_to_stl()
    #  for details... )
    new_name_stl = "Airfoil_"+ str(i) + ".stl"
    new_name_eMesh = "Airfoil_"+ str(i) + ".eMesh"

    # Change the file (We create a copy of the old file --> Modify the copy \
    # --> Remove the file --> Change copy name to the original)
    print("Editing snappyHexMeshDict in {}\n".format(Case.path()))
    with open(orig_file_path,"r") as basefile:
        with open(new_file_path, "w") as newfile:
            for line in basefile:
                newline = line
                # Change the .stl file
                if (orig_name_stl in line):
                    newline = line.replace(orig_name_stl,new_name_stl)

                # Change the .eMesh file
                if (orig_name_eMesh in line):
                    newline = line.replace(orig_name_eMesh,new_name_eMesh)
                newfile.write(newline)

    os.remove(orig_file_path)
    shutil.move(new_file_path,orig_file_path)
    print("Finished editing snappyHexMeshDict file in {}\n"
          .format(Case.path()))  


# --------------------------------------------
# RUN SNAPPYHEXMESH
# --------------------------------------------
def snappyHexMesh(Case: FilePath):
    '''
    Runs snappyHexMesh in parallel with 4 cores
    '''
    os.chdir(Case.path())
 
    # Run in parallel
    print("Decomposing Case in {}" .format(Case.path()))
    os.system("decomposePar -copyZero > decomposeParMesh")

    # I run with 4 cores in my computer, you can change it in your case
    print("Running snappyHexMesh in {}\n".format(Case.path()))
    os.system("mpirun -np 4 snappyHexMesh -parallel -overwrite > \
              snappy")
    print("Finished snappyHexMesh in {}\n".format(Case.path()))

    # Reconstruct the mesh
    print("Reconstructing mesh in {}\n".format(Case.path()))
    os.system("reconstructParMesh -constant > reconstructMesh")

    # Remove the directories
    print("Removing extra processor files in {}\n".format(Case.path()))
    os.system("rm -rf processor*")


# --------------------------------------------
# EDIT THE .stl GEOMETRY IN THE
# surfaceFeatureExtractDict
# --------------------------------------------
def edit_extrudeMesh(Case:FilePath,i,cond):
    '''
    Edits the target geometry that appears in the surfaceFeatureExtractDict
    for snappyHexMesh to mesh
    '''

    # Base path
    Path = FilePath()
    Path.linux_unit()
    Path.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # Original file name
    orig_file_path = Path.file_path("extrudeMeshDict")

    # Target path (Same but python doesn't do deepcopying)
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/system")
    
    # New file name (Provisional)
    new_file_path = Trgt.file_path("New")

    # Get the base case name from the base case
    orig_name = "/mnt/f/Maestria/Airfoil/Simulations/base" 

    # Define a new name for the airfoil key name in the file.
    # (See Airfoil_data.write_csv() & Airfoil_data.csv_to_stl()
    #  for details... )
    new_name ="/mnt/f/Maestria/Airfoil/Simulations/"+str(i) 

    # Change the file (We create a copy of the old file --> Modify the copy \
    # --> Remove the file --> Change copy name to the original)
    print("Editing extrudeMeshDict in {}\n".format(Case.path()))
    with open(orig_file_path,"r") as basefile:
        with open(new_file_path, "w") as newfile:
            for line in basefile:
                newline = line
                if (orig_name in line):
                    newline = line.replace(orig_name,new_name)
                newfile.write(newline)

    os.remove(orig_file_path)
    shutil.move(new_file_path,orig_file_path)
    print("Finished editing extrudeMeshDict file in {}\n"
          .format(Case.path()))


# --------------------------------------------
# RUN EXTRUDEMESH
# --------------------------------------------
def extrudeMesh(Case: FilePath):
    '''
    Runs extrudeMesh to get a 2D Mesh
    '''
    os.chdir(Case.path())
    print("Transforming into a 2D Mesh in {}\n".format(Case.path()))
    os.system("extrudeMesh > extrudeMesh")


# --------------------------------------------
# EDIT THE POLYMESH DICT
# --------------------------------------------
def edit_polymesh(Case: FilePath,i,cond):
    '''
    Edits the constant/polyMesh/boundary file to get the correct B.C
    for 3 patches which need a different name.
    (Look the 0/p or blockMeshDict files for details)
    '''

    # Original path
    Path = FilePath()
    Path.linux_unit()
    Path.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/constant/polyMesh/")
    
    # Original file name
    orig_file_path = Path.file_path("boundary")

    # Target path (Same but python doesn't do deepcopying)
    Trgt = FilePath()
    Trgt.linux_unit()
    Trgt.set_complete_path("F",
                           "Maestria",
                           "Airfoil",
                           "Simulations/"+str(i)+"/constant/polyMesh/")
    
    # New file name (Provisional)
    new_file_path = Trgt.file_path("New")


    # Get the patches name
    key_names = ["front","back","topdown"]
    key_idx = 0

    # Define a new name for the airfoil key name in the file.
    # (See Airfoil_data.write_csv() & Airfoil_data.csv_to_stl()
    #  for details... )
    new_patches = ["empty","empty","symmetry"]

    # Change the file (We create a copy of the old file --> Modify the copy \
    # --> Remove the file --> Change copy name to the original)
    # TRY TO EDIT THIS CODE --> TOO MANY NESTED IF'S
    print("Editing constant/polyMesh/boundary in {}\n".format(Case.path()))
    with open(orig_file_path,"r") as basefile:
        with open(new_file_path, "w") as newfile:
            for line in basefile:
                newline = line
                if (key_names[key_idx] in line): #(orig_name in line):
                    newfile.write(newline)
                    Aux = basefile.readline()
                    newline = Aux
                    newfile.write(newline) 
                    Aux = basefile.readline()
                    if( "patch" in Aux):
                        newline = Aux.replace("patch",new_patches[key_idx])
                        newfile.write(newline)
                        if(key_idx < len(key_names)-1): 
                            newline = line
                            key_idx += 1
                    else:
                        newfile.write(newline)   
                else:
                    newfile.write(newline) 



    os.remove(orig_file_path)
    shutil.move(new_file_path,orig_file_path)
    print("Finished editing constant/polyMesh/boundary in {}\n"
          .format(Case.path()))

    # Return to the case
    Path.SubFolder2 = "Simulations/"+str(i)

def simpleFoam(Case:FilePath):
    '''
    Runs the simpleFoam solver in parallel with 4 cores
    '''
    os.chdir(Case.path())
 
    # Run in parallel
    print("Decomposing Case in {}" .format(Case.path()))
    os.system("decomposePar > decomposePar")

    # I run with 4 cores in my computer, you can change it in your case
    print("Running simpleFoam in {}\n".format(Case.path()))
    os.system("mpirun -np 4 simpleFoam -parallel > \
              log")
    print("Finished simpleFoam in {}\n".format(Case.path()))

    # Reconstruct the mesh
    print("Reconstructing the results in {}\n".format(Case.path()))
    os.system("reconstructPar > reconstructSim")

    # Remove the directories
    print("Removing extra processor files in {}\n".format(Case.path()))
    os.system("rm -rf processor*")  

def pimpleFoam(Case:FilePath):
    '''
    Runs the simpleFoam solver in parallel with 4 cores
    '''
    os.chdir(Case.path())
 
    # Run in parallel
    print("Decomposing Case in {}" .format(Case.path()))
    os.system("decomposePar > decomposePar")

    # I run with 4 cores in my computer, you can change it in your case
    print("Running pimpleFoam in {}\n".format(Case.path()))
    os.system("mpirun -np 4 simpleFoam -parallel > \
              log")
    print("Finished pimpleFoam in {}\n".format(Case.path()))

    # Reconstruct the mesh
    print("Reconstructing the results in {}\n".format(Case.path()))
    os.system("reconstructPar > reconstructSim")

    # Remove the directories
    print("Removing extra processor files in {}\n".format(Case.path()))
    os.system("rm -rf processor*")  

def cleancase(Case:FilePath,i,cond):
    os.chdir(Case.path())

    print("Cleaning_Case in {}\n".format(Case.path()))
    os.system("rm -rf *")

    print("Copying original case")
    copy_case(i,cond)

def rmcase(i):
    Case = FilePath()
    Case.linux_unit()
    Case.set_complete_path("F",
                           "Maestria",
                           "Airfoil/Simulations/",str(i))
    print("Removing {}".format(Case.path()))
    os.system("rm -rf {}".format(Case.path()))


def run_simple(Case:FilePath,i,cond):
    Header = "------------------------------\n"
    case_nmbr = "Case "+str(i)
    print("{}\t{}\n{}" .format(Header,case_nmbr,Header) )
    print("\nRUNNING SIMULATION IN {}\n\n".format(Case.path()))

    # Run the simulation
    copy_case(i,cond)
    blockMesh(Case)
    copy_stl(i,cond)
    edit_sFE(Case,i,cond)
    surfaceFeatureExtract(Case)
    edit_snappyHexMesh(Case,i,cond)
    snappyHexMesh(Case)
    edit_extrudeMesh(Case,i,cond)
    extrudeMesh(Case)
    edit_polymesh(Case,i,cond)
    simpleFoam(Case)

    print("SIMULATION FINISHED\n")

def run_pimple(Case:FilePath,i,cond):
    Header = "------------------------------\n"
    case_nmbr = "Case "+str(i)
    print("{}\t{}\n{}" .format(Header,case_nmbr,Header) )
    print("\nRUNNING SIMULATION IN {}\n\n".format(Case.path()))

    # Run the simulation
    copy_case(i,cond)
    blockMesh(Case)
    copy_stl(i,cond)
    edit_sFE(Case,i,cond)
    surfaceFeatureExtract(Case)
    edit_snappyHexMesh(Case,i,cond)
    snappyHexMesh(Case)
    edit_extrudeMesh(Case,i,cond)
    extrudeMesh(Case)
    edit_polymesh(Case,i,cond)
    pimpleFoam(Case)

    print("SIMULATION FINISHED\n")


def test():
    # Case = FilePath()
    # Case.linux_unit()

    # index = 3000
    # while index == 3000:
    #     Case.set_complete_path("F","Maestria","Airfoil/Simulations",str(index))
    #     # Case.SubFolder2="P_"+str(index)
    #     # Case.printpath()
    #     run_simple(Case,index,False)
    #     # copy_case(index,True)
    #     # blockMesh(Case)
    #     # copy_stl(index)
    #     # edit_sFE(Case,index)
    #     # surfaceFeatureExtract(Case)
    #     # edit_snappyHexMesh(Case,index)
    #     # snappyHexMesh(Case)
    #     # edit_extrudeMesh(Case,index)
    #     # extrudeMesh(Case)
    #     # edit_polymesh(Case,index)
    #     # simpleFoam(Case)
    #     # rmcase(index)
    #     # cleancase(Case,index)
    #     # Case.set_complete_path("F","Maestria","Airfoil/Simulations",str(index))
    #     # run_simple(Case,index,False)
    #     index +=1
    # #cleancase(Case,index)
    binroot = "/mnt/c/Program Files/ParaView 5.11.1/bin"
    os.chdir(binroot)   
    os.system("./pvbatch.exe " + 
            "F:\\Maestria\\\Airfoil\\\Code\\\Paraview_postprocess.py")
# test()