#!/usr/bin/env python

# This example demonstrates the use of vtkSTLReader to load data into
# VTK from a file.  This example also uses vtkLODActor which changes
# its graphical representation of the data to maintain interactive
# performance.

import vtk

import sys
sys.path += ['/home/simon/git/SilverJet/Apps/SolarJet/Project/qt/Lib/']

import VtkShapes, GraphicsPrimitives

def Keypress(obj, event):
  key = obj.GetKeySym()
  if key == "b":
    ToggleBBox()
  elif key == "t":
      ToggleTray()
  elif key == "x":
      ToggleAxes()
    

# ToggleBBox toggles the bounding box of the model
def ToggleBBox():
  RenderWindow.BoundingBoxState = (RenderWindow.BoundingBoxState + 1)%3
    
  BBoxTransparentActor.SetVisibility(RenderWindow.BoundingBoxState == 1)
  BBoxWireFrameActor.SetVisibility(RenderWindow.BoundingBoxState == 2)
  BoundingBoxTextActor.SetVisibility(RenderWindow.BoundingBoxState > 0)

  Renderer.ResetCamera()
  RenderWindow.Render()

# ToggleBBox toggles the tray under the model
def ToggleTray():
  RenderWindow.TrayState = (RenderWindow.TrayState + 1)%2
    
  TrayActor.SetVisibility(RenderWindow.TrayState == 1)
  TrayTextActor.SetVisibility(RenderWindow.TrayState == 1)

  Renderer.ResetCamera()
  RenderWindow.Render()


def ToggleAxes():
  RenderWindow.AxesState = (RenderWindow.AxesState + 1)%2
    
  for Actor in [XArrowActor, XAxisActor, YArrowActor, YAxisActor, ZArrowActor, ZAxisActor]:
    Actor.SetVisibility(RenderWindow.AxesState == 1)

  Renderer.ResetCamera()
  RenderWindow.Render()
    

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-m", "--model",
                    dest="ModelFilename",
                    default = "",
                    help="Input Model filename")

parser.add_option("-p", "--parallel-view",
                    dest="DoShowParallelView",
                    action='store_true',
                    default = False,
                    help="Display in parallel view")


parser.add_option("-T", "--tray-Size",
                    dest="TraySizeInMM",
                    nargs = 2,
                    default = (100, 36),
                    help="Set Tray Size [(100,36)]")


parser.add_option("-W", "--window-Size",
                    dest="WindowSize",
                    nargs = 2,
                    default = (900, 900),
                    help="Set Window Size [(900,900)]")


(options, args) = parser.parse_args()

assert(len(options.ModelFilename) > 0 )
 
assert(len(options.TraySizeInMM) == 2 )
TraySizeInMM = [float(sz) for sz in options.TraySizeInMM]

assert(len(options.WindowSize) == 2 )
WindowSize = [int(sz) for sz in options.WindowSize]

if '.STL' in options.ModelFilename.upper():
  Model = vtk.vtkSTLReader()
elif '.OBJ' in options.ModelFilename.upper():
  Model = vtk.vtkOBJReader()
else:
  raise Exception('Unknown file type for model: %s'%options.ModelFilename)

Model.SetFileName(options.ModelFilename)
Model.Update()
ModelOutput = Model.GetOutput()

BoundingBox = ModelOutput.GetBounds()

Mapper = vtk.vtkPolyDataMapper()
Mapper.SetInputConnection(Model.GetOutputPort())

Actor = vtk.vtkLODActor()
Actor.SetMapper(Mapper)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
Renderer = vtk.vtkRenderer()
RenderWindow = vtk.vtkRenderWindow()
RenderWindow.AddRenderer(Renderer)

# Add the actors to the render; set the background and size
Renderer.SetBackground(0.1, 0.2, 0.4)
RenderWindow.SetSize(*WindowSize)

#Model
Renderer.AddActor(Actor)

#Add text
ModelNameTextActor = vtk.vtkTextActor()
ModelNameTextActor.GetTextProperty().SetFontSize (20);
Renderer.AddActor2D(ModelNameTextActor)
ModelNameTextActor.SetInput ("Model: {0}".format(options.ModelFilename))
ModelNameTextActor.GetTextProperty().SetColor (0.7,0.7,0.7);
ModelNameBBox = [0,0,0,0]
ModelNameTextActor.GetBoundingBox(Renderer, ModelNameBBox)
ModelNameTextActor.SetPosition (WindowSize[0]-ModelNameBBox[1]-5,
                                WindowSize[1]-ModelNameBBox[3]-5)



#Axes arrows
XArrowActor, XAxisActor = VtkShapes.AddArrowToRenderer(Renderer,Pos=(0,0,0),Len=15,Dir=(1,0,0),
                                                       ColorHead=(1,0,0), Stem = 0.1)

YArrowActor, YAxisActor = VtkShapes.AddArrowToRenderer(Renderer,Pos=(0,0,0),Len=15,Dir=(0,1,0),
                                                       ColorHead=(0,1,0), Stem = 0.1)

ZArrowActor, ZAxisActor = VtkShapes.AddArrowToRenderer(Renderer,Pos=(0,0,0),Len=15,Dir=(0,0,1),
                                                       ColorHead=(0,0,1), Stem = 0.1)

for Actor in [XArrowActor, XAxisActor, YArrowActor, YAxisActor, ZArrowActor, ZAxisActor]:
  Actor.SetVisibility(True)

RenderWindow.AxesState = 1  

#Tray
TrayPoints = [(0,0,0),
              (0,TraySizeInMM[1],0),
              (TraySizeInMM[0],TraySizeInMM[1], 0),
              (TraySizeInMM[0], 0, 0)]
    
TrayFaces = [(0,1,2,3)]
TrayActor = VtkShapes.AddVandFtoRender(Renderer, (TrayPoints, TrayFaces), Color = (.3, .3, .3), Opacity = 0.5)

TrayActor.SetVisibility(False)

RenderWindow.TrayState = 0

#Tray Text
TrayTextActor = vtk.vtkTextActor()
TrayTextActor.GetTextProperty().SetFontSize (20);
Renderer.AddActor2D(TrayTextActor)
TrayTextActor.SetInput ("Tray Size: ({0},{1})".format(TraySizeInMM[0], TraySizeInMM[1]))
TrayTextActor.GetTextProperty().SetColor (0.7,0.7,1)
TrayBBox = [0,0,0,0]
TrayTextActor.GetBoundingBox(Renderer, TrayBBox)
TrayTextActor.SetPosition (WindowSize[0]-TrayBBox[1]-5,5)
TrayTextActor.SetVisibility(False)

  
#BBox Wireframe  
BBoxWireFrameActor = VtkShapes.AddVandFtoRender(Renderer, GraphicsPrimitives.Box(BoundingBox),
                             Color = (1, 0, 0), Opacity = 1, DoSetWireframe = True)

BBoxWireFrameActor.SetVisibility(False)
#Transparent BoundingBox
BBoxTransparentActor = VtkShapes.AddVandFtoRender(Renderer, GraphicsPrimitives.Box(BoundingBox),
                             Color = (.3, .5, .3), Opacity = 0.2)

BBoxTransparentActor.SetVisibility(False)

#BBox Add text
BoundingBoxTextActor = vtk.vtkTextActor()
BoundingBoxTextActor.GetTextProperty().SetFontSize (20);
Renderer.AddActor2D(BoundingBoxTextActor)
BoundingBoxTextActor.SetInput ("Bounding Box: \n"+
                     "X: [{0:.3f}, {1:.3f}] mm\n".format(BoundingBox[0],BoundingBox[1])+
                     "Y: [{0:.3f}, {1:.3f}] mm\n".format(BoundingBox[2],BoundingBox[3])+
                     "Z: [{0:.3f}, {1:.3f}] mm".format(BoundingBox[4],BoundingBox[5])
                     )
BoundingBoxTextActor.SetPosition (0,0)
BoundingBoxTextActor.GetTextProperty().SetColor (0.7,0.7,1.0)

BoundingBoxTextActor.SetVisibility(False)

RenderWindow.BoundingBoxState = 0

if options.DoShowParallelView:
    Renderer.GetActiveCamera().ParallelProjectionOn() #This is not working so far... refine this.

#Interactor
Interactor = vtk.vtkRenderWindowInteractor()
Interactor.SetRenderWindow(RenderWindow)

#Set the default behaviour to be trackball
InteractorStyle = vtk.vtkInteractorStyleSwitch()
InteractorStyle.SetCurrentStyleToTrackballCamera()
Interactor.SetInteractorStyle(InteractorStyle)

Interactor.Initialize()

Interactor.AddObserver("KeyPressEvent", Keypress)

RenderWindow.Render()
Interactor.Start()


