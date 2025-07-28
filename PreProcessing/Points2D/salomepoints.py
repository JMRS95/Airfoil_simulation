import csv
import salome
salome.salome_init()
from salome.geom import geomBuilder
geompy = geomBuilder.New()

# Path to your CSV file
csv_file_path = 'F:\Maestria\Airfoil\Points2D\P_Airfoil_2001_Coords.csv'

# Read the CSV file
points = []
with open(csv_file_path, 'r') as fileo:
    line = fileo.readline()
    line = fileo.readline()
    while line:
        x,y = [float(x) for x in line.strip().split(",")]
        z = -0.1
        points.append(geompy.MakeVertex(x, y, z))
        line = fileo.readline()

# Add points to the geometry
for point in points:
    geompy.addToStudy(point, 'Point_%d' % len(points))

# Update the object browser
salome.sg.updateObjBrowser()
