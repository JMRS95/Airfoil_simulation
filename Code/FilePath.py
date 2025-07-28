# *******************************************************************************
# CLASS:      FILEPATH
# *******************************************************************************
'''
The following class is meant to read OpenFOAM files for PostProcessing
This must always be included
'''

# ----------------------------------------------------------
# LIBRARIES
# ----------------------------------------------------------
import os

# ----------------------------------------------------------
# CLASS
# ----------------------------------------------------------


class FilePath():
    # --------------------------
    # ATRIBUTES:
    # --------------------------
    def __init__(self):

        # SYSTEM (Linux or Windows):
        self.__System = True

        # UNIT:
        self.__Unit = ""
        # Principal Folder:
        self.__PFolder = ""

        # Separator:
        self.__Sep = "\\"  # WINDOWS
        #self.__Sep = "/"  # LINUX

        # SubFolder 1:
        self.__SubFolder1 = ""

        # SubFolder 2:
        self.__SubFolder2 = ""

        # File:
        self.__File = ""


# --------------------------
# GET/SET METHODS
# --------------------------

# GETTERS: Print the attribute of classes


    @property
    def System(self):
        if (self.__System):
            print("\tCurrently in Windows\n")
            self.__System = False
        else:
            print("\tCurrently in Linux\n")
            self.__System = True

    @property
    def Unit(self):
        return self.__Unit

    @property
    def PFolder(self):
        return self.__PFolder

    @property
    def Sep(self):
        return self.__Sep

    @property
    def SubFolder1(self):
        return self.__SubFolder1

    @property
    def SubFolder2(self):
        return self.__SubFolder2

    @property
    def File(self):
        return self.__File

# SETTERS: Set the attribute classes (Sep & )

    @Unit.setter
    def Unit(self, Unit):
        # Windows
        if(self.__System):
            self.__Unit = Unit + ":"
        # Linux
        else:
            self.__Unit = "/mnt/" + str.lower(Unit )+ "/"

    @PFolder.setter
    def PFolder(self, PFolder):
        self.__PFolder = PFolder

    @SubFolder1.setter
    def SubFolder1(self, SubFolder1):
        self.__SubFolder1 = SubFolder1

    @SubFolder2.setter
    def SubFolder2(self, SubFolder2):
        self.__SubFolder2 = SubFolder2

    @File.setter
    def File(self, File):
        self.__File = File

# --------------------------
# METHODS
# --------------------------

    # BOOLEAN --> CHANGE UNIT TO WINDOWS:
    def windows_unit(self):
        self.__System = True
        #print("\tChanged to Windows\n")
        self.__Unit = "C:"
        return True

    # BOOLEAN --> CHANGE UNIT TO LINUX:
    def linux_unit(self):
        self.__System = False
        #print("\tChanged to Linux\n")
        self.__Sep = "/"
        self.__Unit = self.__Sep + "mnt" + self.__Sep + "c" + self.__Sep
        return False

    # STRING --> RETURN THE COMPLETE PATH:
    def path(self):
        if (self.__System):
            if (self.Unit == ""):
                return ""
            elif (self.__PFolder == ""):
                return self.__Unit
            elif (self.__SubFolder1 == ""):
                return self.__Unit + self.__Sep + self.__PFolder
            elif (self.__SubFolder2 == ""):
                return self.__Unit + self.__Sep + self.__PFolder + self.__Sep \
                    + self.__SubFolder1
            else:
                return self.__Unit + self.__Sep + self.__PFolder + self.__Sep \
                    + self.__SubFolder1 + self.__Sep + self.__SubFolder2
        else:
            self.__Sep = "/"
            if (self.Unit == ""):
                return ""
            elif (self.__PFolder == ""):
                return self.__Unit
            elif (self.__SubFolder1 == ""):
                return self.__Unit + self.__PFolder
            elif (self.__SubFolder2 == ""):
                return self.__Unit + self.__PFolder + self.__Sep + self.__SubFolder1
            else:
                return self.__Unit + self.__PFolder + self.__Sep \
                    + self.__SubFolder1 + self.__Sep + self.__SubFolder2

    # STRING --> SET THE COMPLETE PATH FROM UNIT:
    def set_complete_path(self, Unit, PFolder, SubFolder1, SubFolder2):
        if (self.__System):
            self.__Unit = Unit + ":"
            self.__PFolder = PFolder
            self.__SubFolder1 = SubFolder1
            self.__SubFolder2 = SubFolder2
            return self.__Unit + self.__Sep + self.__PFolder + self.__Sep \
                + self.__SubFolder1 + self.__Sep + self.__SubFolder2
        else:
            self.__Sep = "/"
            Unit = str.lower(Unit)
            self.__Unit = "/mnt/" + Unit + self.__Sep
            self.__PFolder = PFolder
            self.__SubFolder1 = SubFolder1
            self.__SubFolder2 = SubFolder2
            return self.__Unit + self.__Sep + self.__PFolder + self.__Sep \
                + self.__SubFolder1 + self.__Sep + self.__SubFolder2

    # STRING --> SET THE PATH IN THE UNIT:
    def set_path(self, PFolder, SubFolder1, SubFolder2):
        self.__PFolder = PFolder
        self.__SubFolder1 = SubFolder1
        self.__SubFolder2 = SubFolder2
        return self.__PFolder + self.__Sep + self.__SubFolder1 + self.__Sep \
            + self.__SubFolder2

    # STRING --> SET FROM THE SUBFOLDER1 PATH:
    def set_path_sub(self, SubFolder1, SubFolder2):
        self.__SubFolder1 = SubFolder1
        self.__SubFolder2 = SubFolder2
        return self.__SubFolder1 + self.__Sep + self.__SubFolder2

    # STRING --> SET THE CURRENT PATH:
    def set_current_path(self):
        path = os.getcwd()
        crop1 = path.strip()
        if(self.__System):
            crop2 = path.split("\\")
            self.__Unit = crop2[0]
            self.__PFolder = crop2[1]
            self.__SubFolder1 = crop2[2]
            self.__SubFolder2 = crop2[3]
        else:
            crop2 = path.split("/")
            self.__Unit = "/" + crop2[1] + "/" + crop2[2] + "/"
            self.__PFolder = crop2[3]
            self.__SubFolder1 = crop2[4]
            self.__SubFolder2 = crop2[5]
        return path

    # VOID --> PRINT THE COMPLETE PATH:
    def printpath(self):
        print(FilePath.path(self))

    # VOID --> RESET THE PATH TO DEFAULTS:
    def reset(self):
        self.__PFolder = ""
        self.__SubFolder1 = ""
        self.__SubFolder2 = ""
        self.__File = ""
        print("\tPath reseted...\n")
        if (self.__System):
            FilePath.windows_unit(self)
        else:
            FilePath.linux_unit(self)

    # BOOLEAN --> LOCATING FILE:
    def locate_file(self):
        if (self.__File == ""):
            print("\n\tNo file set to be found\n")
            return False
        else:
            Aux = FilePath.path(self)

            srch = os.listdir(Aux)
            lensrch = len(srch)

            Var = self.__File
            i = 0
            while (i < lensrch):
                # print(i)
                if (srch[i] == Var):
                    print("\n\tFound: {}  in:\t{}\n".format(self.__File, Aux))
                    return True
                    break
                i += 1
            else:
                print("\n\tFile: {} not found in:\t{}\n" .format(self.__File, Aux))
                return False

    # LIST --> PRINT PATH CONTENT:
    def path_content(self):
        Aux = FilePath.path(self)
        ls = os.listdir(Aux)
        print("Path content:\n{}\n".format(ls))
        return ls

    # VOID --> PRINT PATH TO FILE:
    def print_file_path(self):
        if (self.__File == ""):
            print("\tNo file to be shown\n")
        else:
            S = FilePath.locate_file(self)
            Path = FilePath.path(self) + self.Sep
            File = self.__File
            Aux = Path + File
            if (S):
                print("\tFile path is: {}\n" .format(Aux))
            else:
                print("\tFile: {}, doesn't exist in {}\n". format(File, Path))

    # STRING --> JOIN FILE TO READ IN PATH:
    def file_path(self, filename):
        self.__File = filename
        if (self.__Unit == ""):
            print("\tNo unit set, please set the unit:")
            print("Options:\n\t{}\n\t{}\n\t{}"
                  .format("C: ---> windows_unit method",
                          "Root (/): ---> linux_unit method"
                          "Own unit: ---> Read.Unit method"))
        elif (self.__PFolder == ""):
            return self.__Unit + self.__Sep + self.__File
        elif (self.__SubFolder1 == ""):
            return self.__Unit + self.__Sep + self.__PFolder \
                + self.__Sep + self.__File
        elif (self.__SubFolder2 == ""):
            return self.__Unit + self.__Sep + self.__PFolder \
                + self.__Sep + self.__SubFolder1 + self.__Sep \
                + self.__File
        else:
            return self.__Unit + self.__Sep + self.__PFolder + self.__Sep \
                + self.__SubFolder1 + self.__Sep + self.__SubFolder2  \
                + self.__Sep + self.__File


# --------------------------
# OBJECT PRINTING FORMAT
# --------------------------
# When you print in screen the object it will be done with the following format:
    def __str__(self):
        if (self.__System):
            Aux = FilePath.path(self)
            if (Aux != ""):
                msg = "\tCurrently in Windows: \n\t"
                return ("{} Your current path is {}\n".format(msg, Aux))
            else:
                return ("\tNo path set\n")
        else:
            Aux = FilePath.__path(self)
            msg = "\tCurrently in Linux: \n"
            return ("{} Your current path is {}\n".format(msg, Aux))


# ----------------------------------------------------------
# TESTING
# ----------------------------------------------------------

def test():
    # FilePath object:
    File1 = FilePath()
    # Must print "No path Set"
    print(File1)

    # If you work with Windows hard disk OS you must use the method below:
    File1.windows_unit()
    # If you work with Linux, use the method below:
    File1.linux_unit()
    # Here I change the defaults to windows again:
    File1.windows_unit()

    # Now we set the Unit (Be aware that this is for Windows Users.)
    # This is helpful for working with external hard drives.
    # ONLY TYPE THE LETTER, NOT THE CHARACTERS ":"
    File1.Unit = "F"

    # Now if you print the File1 object it must show your current path:
    print(File1)
    # This is another way of showing your current path. Use the one you prefer
    File1.printpath()

    # If we try to print the Parent Folder name it won't show anything
    print(File1.PFolder)

    # Now set Folder's name and we show its path
    File1.PFolder = "Parent"
    File1.printpath()

    # Same for SubFolders: (for now)
    # Be aware that this for now only supports 2 SubFolders,
    # if you nedd more, you must add the complete route.
    # Show the path
    File1.SubFolder1 = "Sub1"
    File1.printpath()
    File1.SubFolder2 = "Sub2"
    File1.printpath()
    # Finally this shows your actual path_content(). (Uses the Python's module: os)
    File1.path_content()

    # Showing file. Must print that no file is meant to be found:
    File1.locate_file()
    # If we'd also like the path to the complete file will show a message that the file isn't found
    File1.print_file_path()

    # Now let's change in the directory an existent file named: "Test.txt"
    File1.File = "Test.txt"
    # We call the file methods used before:
    # This will show that the file has been found.
    File1.locate_file()

    # This will show the file's path
    File1.print_file_path()
    # Suppose you typed "Test.txt" incorrectly, such as "Twst.txt":
    File1.File = "Twst.txt"
    # Now the methods will show you that The file wasn't found
    File1.locate_file()
    # And that the file doesn't exist in route (Also shows the locate_file message)
    File1.print_file_path()
    # Here we reset the path
    File1.reset()
    # If you want to set the complete path in one line, instead of going 1 by 1 use the set_complete_path() method
    File1.set_complete_path("F", "ParentPath", "SubFolder1", "SubFolder2")
    # Printing:
    File1.printpath()

    # We reset again here:
    File1.reset()

    # If you don't want the unit to be changed, a method named set_path is avaiable:
    File1.set_path("ParentPath", "SubFolder1", "SubFolder2")
    # Printing:
    File1.printpath()

    # Or just the subfolder1, use set_path_sub():
    File1.set_path_sub("X", "Y")
    # Printing:
    File1.printpath()

    # We reset again here:
    File1.reset()

    # THANK YOU. Any suggestion is accepted!


def main():
    return 0
