# trace generated using paraview version 5.7.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'CSV Reader'
airfoil_0_Coordscsv = CSVReader(
    FileName=['/mnt/f/Maestria/Airfoil/Points/Airfoil_0_Coords.csv'])

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# show data in view
airfoil_0_CoordscsvDisplay = Show(airfoil_0_Coordscsv, spreadSheetView1)

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# create a new 'Table To Points'
tableToPoints1 = TableToPoints(Input=airfoil_0_Coordscsv)
tableToPoints1.XColumn = 'x'
tableToPoints1.YColumn = 'x'
tableToPoints1.ZColumn = 'x'

# Properties modified on tableToPoints1
tableToPoints1.YColumn = 'y'
tableToPoints1.ZColumn = 'z'

# show data in view
tableToPoints1Display = Show(tableToPoints1, spreadSheetView1)

# hide data in view
Hide(airfoil_0_Coordscsv, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Delaunay 3D'
delaunay3D1 = Delaunay3D(Input=tableToPoints1)

# show data in view
delaunay3D1Display = Show(delaunay3D1, spreadSheetView1)

# hide data in view
Hide(tableToPoints1, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=delaunay3D1)

# show data in view
extractSurface1Display = Show(extractSurface1, spreadSheetView1)

# hide data in view
Hide(delaunay3D1, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# save data
SaveData('/mnt/f/Maestria/Airfoil/Stl/Airfoil_0.stl', proxy=extractSurface1)

ResetSession()

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).