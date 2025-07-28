from FilePath import FilePath
import numpy as np
import linecache
import os
import sys
import shutil
import Airfoil_data as data


path = '/mnt/f/Maestria/Airfoil/'
number = 2001
file = 'Points2D/P_Airfoil_'+str(number)+'_Coords.csv'

path = path+file

write_path=path+'Code'

os.chdir(write_path)
os.chdir(path)