# trace generated using paraview version 5.11.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Paraview will read this file to get the current number
numberpath = "F:\\Maestria\\Airfoil\\Code\\Index"
# numberpath = "/mnt/f/Maestria/Airfoil/Code/Index"
with open(numberpath,"r") as numberfile:
    for line in numberfile:
        n = line.strip()

# ONLY FOR NOW
# n = 0
# LOOPING

idx = 0

while idx <= 1:
    # create a new 'OpenFOAMReader'
    casefoam = OpenFOAMReader(registrationName='Case.foam',
    FileName='F:\\Maestria\\Airfoil\\Simulations\\'+str(n)+'\\Case.foam')

    # What it's being seen
    casefoam.MeshRegions = ['internalMesh']

    # Files to be read
    casefoam.CellArrays = ['U', 'p', 'vorticity']

    # get animation scene
    animationScene1 = GetAnimationScene()

    # get the time-keeper
    timeKeeper1 = GetTimeKeeper()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    casefoamDisplay = Show(casefoam, renderView1, 'UnstructuredGridRepresentation')

    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # Properties modified on renderView1
    renderView1.OrientationAxesInteractivity = 0

    # ------ Setting the camera --------------
    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.622557416220005, 1.0762077589399408, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.622557416220005, 1.0762077589399408, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575


    # get color transfer function/color map for 'p'
    pLUT = GetColorTransferFunction('p')

    # get opacity transfer function/opacity map for 'p'
    pPWF = GetOpacityTransferFunction('p')

    # trace defaults for the display properties.
    casefoamDisplay.Representation = 'Surface'
    casefoamDisplay.ColorArrayName = ['POINTS', 'p']
    casefoamDisplay.LookupTable = pLUT
    casefoamDisplay.SelectTCoordArray = 'None'
    casefoamDisplay.SelectNormalArray = 'None'
    casefoamDisplay.SelectTangentArray = 'None'
    casefoamDisplay.OSPRayScaleArray = 'p'
    casefoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    casefoamDisplay.SelectOrientationVectors = 'U'
    casefoamDisplay.ScaleFactor = 4.4
    casefoamDisplay.SelectScaleArray = 'p'
    casefoamDisplay.GlyphType = 'Arrow'
    casefoamDisplay.GlyphTableIndexArray = 'p'
    casefoamDisplay.GaussianRadius = 0.22
    casefoamDisplay.SetScaleArray = ['POINTS', 'p']
    casefoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    casefoamDisplay.OpacityArray = ['POINTS', 'p']
    casefoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    casefoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
    casefoamDisplay.PolarAxes = 'PolarAxesRepresentation'
    casefoamDisplay.ScalarOpacityFunction = pPWF
    casefoamDisplay.ScalarOpacityUnitDistance = 1.3061938874298014
    casefoamDisplay.OpacityArrayName = ['POINTS', 'p']
    casefoamDisplay.SelectInputVectors = ['POINTS', 'U']
    casefoamDisplay.WriteLog = ''

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    casefoamDisplay.ScaleTransferFunction.Points = \
    [-465.7690734863281, 0.0, 0.5, 0.0, 268.47662353515625, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    casefoamDisplay.OpacityTransferFunction.Points = \
        [-465.7690734863281, 0.0, 0.5, 0.0, 268.47662353515625, 1.0, 0.5, 0.0]

    # reset view to fit data
    renderView1.ResetCamera(False)

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # find settings proxy
    colorPalette = GetSettingsProxy('ColorPalette')

    # Properties modified on colorPalette
    colorPalette.Background = [1.0, 1.0, 1.0]


    # ---------------- Pressure -------------------


    # get color transfer function/color map for 'p'
    pLUT = GetColorTransferFunction('p')

    # get 2D transfer function for 'p'
    pTF2D = GetTransferFunction2D('p')

    # get opacity transfer function/opacity map for 'p'
    pPWF = GetOpacityTransferFunction('p')

    # get color legend/bar for uLUT in view renderView1
    pLUTColorBar = GetScalarBar(pLUT, renderView1)


    # Properties modified on pLUTColorBar
    pLUTColorBar.AutoOrient = 0
    pLUTColorBar.Orientation = 'Horizontal'
    pLUTColorBar.WindowLocation = 'Any Location'
    pLUTColorBar.Position = [0.04867231638418085, 0.8296296296296297]
    pLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
    pLUTColorBar.TitleBold = 1
    pLUTColorBar.TitleFontSize = 25
    pLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
    pLUTColorBar.LabelBold = 1
    pLUTColorBar.LabelFontSize = 22
    pLUTColorBar.ScalarBarThickness = 20
    pLUTColorBar.ScalarBarLength =  0.825


    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # Properties modified on uLUTColorBar
    pLUTColorBar.TitleFontSize = 24
    pLUTColorBar.LabelFontSize = 20

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    pLUT.ApplyPreset('Magma (matplotlib)', True)

    # Go to the last step
    animationScene1.GoToLast()

    # View 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575

    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/p_1.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575

    # save animation (not done for now)
    
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/p_1.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])


    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # Go to the last step
    animationScene1.GoToLast()

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/p_2.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # save animation (Uncomment for the video)
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/p_2.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])

    # # --------------- U -------------------


    # set scalar coloring
    ColorBy(casefoamDisplay, ('POINTS', 'U', 'Magnitude'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(pLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'U'
    uLUT = GetColorTransferFunction('U')

    # get 2D transfer function for 'U'
    uTF2D = GetTransferFunction2D('U')

    # get opacity transfer function/opacity map for 'p'
    uPWF = GetOpacityTransferFunction('U')

    # get color legend/bar for uLUT in view renderView1
    uLUTColorBar = GetScalarBar(uLUT, renderView1)


    #  Properties modified on pLUTColorBar
    uLUTColorBar.AutoOrient = 0
    uLUTColorBar.Orientation = 'Horizontal'
    uLUTColorBar.WindowLocation = 'Any Location'
    uLUTColorBar.Position = [0.04867231638418085, 0.8296296296296297]
    uLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
    uLUTColorBar.TitleBold = 1
    uLUTColorBar.TitleFontSize = 25
    uLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
    uLUTColorBar.LabelBold = 1
    uLUTColorBar.LabelFontSize = 22
    uLUTColorBar.ScalarBarThickness = 20
    uLUTColorBar.ScalarBarLength =  0.825


    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # Properties modified on uLUTColorBar
    uLUTColorBar.TitleFontSize = 24
    uLUTColorBar.LabelFontSize = 20

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    uLUT.ApplyPreset('hsv', True)

    # Go to the last step
    animationScene1.GoToLast()

    # View 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575
    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/U_1.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575

    # # save animation (Uncomment for the video)
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/U_1.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])


    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # Go to the last step
    animationScene1.GoToLast()

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/U_2.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # # save animation (Uncomment for the video)
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/U_2.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])

    # # --------------- VORTICITY -------------------

    # Return to the previous view
    #change interaction mode for render view
    # set scalar coloring


    ColorBy(casefoamDisplay, ('POINTS', 'vorticity', 'Z'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(uLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'vorticity'
    vLUT = GetColorTransferFunction('vorticity')

    # get 2D transfer function for 'vorticity'
    vTF2D = GetTransferFunction2D('vorticity')

    # get opacity transfer function/opacity map for 'vorticity'
    vPWF = GetOpacityTransferFunction('vorticity')

    # get color legend/bar for uLUT in view renderView1
    vLUTColorBar = GetScalarBar(vLUT, renderView1)

    #  Properties modified on vLUTColorBar
    vLUTColorBar.AutoOrient = 0
    vLUTColorBar.Orientation = 'Horizontal'
    vLUTColorBar.WindowLocation = 'Any Location'
    vLUTColorBar.Position = [0.04867231638418085, 0.8296296296296297]
    vLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
    vLUTColorBar.TitleBold = 1
    vLUTColorBar.TitleFontSize = 25
    vLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
    vLUTColorBar.LabelBold = 1
    vLUTColorBar.LabelFontSize = 22
    vLUTColorBar.ScalarBarThickness = 20
    vLUTColorBar.ScalarBarLength =  0.825


    # show color bar/color legend
    casefoamDisplay.SetScalarBarVisibility(renderView1, True)

    # Properties modified on uLUTColorBar
    vLUTColorBar.TitleFontSize = 24
    vLUTColorBar.LabelFontSize = 20

    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    vLUT.ApplyPreset('Blue - Green - Orange', True)

    # Rescale transfer function
    vLUT.RescaleTransferFunction(-10.0, 10.0)

    # Rescale transfer function
    vPWF.RescaleTransferFunction(-10.0, 10.0)

    # Rescale 2D transfer function
    vTF2D.RescaleTransferFunction(-10.0, 10.0, 0.0, 1.0)

    # Go to the last step
    animationScene1.GoToLast()

    # View 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575
    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/Vorticity_1.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)


    # view 1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [11.796747107209415, 1.7967471072094252, 92.7905923264733]
    renderView1.CameraFocalPoint = [11.796747107209415, 1.7967471072094252, -0.600000012665987]
    renderView1.CameraParallelScale = 13.644048345371575

    # # save animation (Uncomment for video)
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/Vorticity_1.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])


    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # Go to the last step
    animationScene1.GoToLast()

    # save screenshot
    SaveScreenshot('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/Vorticity_2.png', renderView1, ImageResolution=[1416, 729])

    # layout/tab size in pixels
    layout1.SetSize(1416, 729)

    # view 2
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [2.642030663560465, 0.7246864061176227, 92.7905923264733]
    renderView1.CameraFocalPoint = [2.642030663560465, 0.7246864061176227, -0.600000012665987]
    renderView1.CameraParallelScale = 2.9693424500822223

    # save animation (Uncomment for video)
    # SaveAnimation('F:/Maestria/Airfoil/Simulations/'+str(n)+'/postProcessing/Vorticity_2.mp4', renderView1, ImageResolution=[1416, 728],
    #     FrameRate=10,
    #     FrameWindow=[0, 99])

    # ------------------------------ DATA EXTRACTION ENDS ----------------------

    ResetSession()

    # get animation scene
    animationScene1_1 = GetAnimationScene()

    # get the time-keeper
    timeKeeper1_1 = GetTimeKeeper()

    # get active view
    renderView1_1 = GetActiveViewOrCreate('RenderView')

    #================================================================
    # addendum: following script captures some of the application
    # state to faithfully reproduce the visualization during playback
    #================================================================

    # get layout
    layout1_1 = GetLayout()

    #--------------------------------
    # saving layout sizes for layouts

    # layout/tab size in pixels
    # layout1_1.SetSize(1416, 729)

    #--------------------------------------------
    # uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).

    # Reset session
    ResetSession()


    # Don't forget to increase the index by 1
    idx += 1