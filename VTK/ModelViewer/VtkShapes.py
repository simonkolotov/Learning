#!/usr/bin/python

import math
import vtk
import GraphicsPrimitives
import euclid

def Transform(M, Points):
  return [M*euclid.Point3(*p) for p in Points]

def Perp(u):
  """Randomly picks a reasonable perpendicular vector"""
  v = euclid.Vector3(1, 0, 0)
  u_prime = u.cross(v)
  if u_prime.magnitude_squared() < 0.01:
    v = euclid.Vector3(0, 1, 0)
    u_prime = u.cross(v)
  return u_prime.normalized()

def VandFtoPoly(Vertices,
                Faces):
  points = vtk.vtkPoints()
  for v in Vertices:
     points.InsertNextPoint(v)

  polygons = vtk.vtkCellArray()
  for f in Faces:
    poly = vtk.vtkPolygon()
    Pids = poly.GetPointIds()
    Pids.SetNumberOfIds(len(f))
    for i,pid in enumerate(f):
      Pids.SetId(i,pid)
    polygons.InsertNextCell(poly)

  polygonPolyData = vtk.vtkPolyData()
  polygonPolyData.SetPoints(points)
  polygonPolyData.SetPolys(polygons)
  return polygonPolyData
  
def VandFtoActor(Vertices,
                 Faces,
                 Color,
                 Opacity=1.0,
                 DoSetWireframe = False):
  Actor = vtk.vtkActor()
  poly = VandFtoPoly(Vertices,Faces)
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(poly)
  Actor.SetMapper(mapper)
  Actor.GetProperty().SetColor(*Color)
  Actor.GetProperty().SetOpacity(Opacity)

  if DoSetWireframe:
    Actor.GetProperty().SetRepresentationToWireframe()
  return Actor

def AddVandFtoRender(Renderer,
                     VandF,
                     Pos=None,
                     Dir=None,
                     Scale=(1,1,1),
                     Color=(1,0,0),
                     Opacity=1.0,
                     DoSetWireframe = False):
  """Add an actor to a vtk scene"""
  Vertices,Faces = VandF

  if Pos is None:
    Pos = (0,0,0)
    MPos = euclid.Matrix4.new_identity()
  else:
    MPos = euclid.Matrix4.new_translate(*Pos)

  if Dir is None:
    MDir = euclid.Matrix4.new_identity()
  else:
    Dir = euclid.Vector3(*Dir)
    Dir /= math.sqrt(Dir.magnitude_squared())
    nX = Perp(Dir)
    nY = Dir.cross(nX)
    MDir = euclid.Matrix4.new_rotate_triple_axis(nX,
                                                 nY,
                                                 Dir)

  M = (MDir * euclid.Matrix4.new_scale(*Scale)).pre_translate(*Pos)
  Vertices = Transform(M,Vertices)
  Actor = VandFtoActor(Vertices,Faces,Color,Opacity,DoSetWireframe)
  Renderer.AddActor(Actor)

  return Actor

def AddLine(Renderer,
            PolyLine,
            LineWidth=5,
            Color=(1,0,0)):
  if isinstance(PolyLine, vtk.vtkObject):
    if not PolyLine.GetClassName() == 'vtkPolyData':
      raise Exception('No support for %s'%PolyLine.GetClassName())
    polygonPolyData = PolyLine
  else:
    points = vtk.vtkPoints()
    for v in PolyLine:
       points.InsertNextPoint(v)
    lines = vtk.vtkCellArray()
    for i in range(len(PolyLine)-1):
      line = vtk.vtkLine()
      line.GetPointIds().SetId(i,i)
      line.GetPointIds().SetId(i+1,i+1)
      lines.InsertNextCell(line)
      
    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetLines(lines)
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(polygonPolyData)
  Actor=vtk.vtkActor()
  Actor.GetProperty().SetLineWidth(LineWidth)
  Actor.GetProperty().SetColor(*Color)
  Actor.SetMapper(mapper)
  Renderer.AddActor(Actor)

  
def AddArrowToRenderer(Renderer,
                       Pos=None,
                       Len=10,
                       Dir=None,
                       CylinderSlicesNum=16,
                       ColorHead=(1,0,0),
                       ColorCyl=(0.5,0.5,0.5),
                       Stem=0.25):
  """Add an actor to a vtk scene"""
  cylV,cylF = GraphicsPrimitives.cylinder(num_slices=CylinderSlicesNum)
  headV,headF = GraphicsPrimitives.cone(num_slices=CylinderSlicesNum)

  if Pos is None:
    Pos = (0,0,0)
    MPos = euclid.Matrix4.new_identity()
  else:
    MPos = euclid.Matrix4.new_translate(*Pos)

  if Dir is None:
    MDir = euclid.Matrix4.new_identity()
  else:
    Dir = euclid.Vector3(*Dir).normalized()
    nX = Perp(Dir)
    nY = Dir.cross(nX)
    MDir = euclid.Matrix4.new_rotate_triple_axis(nX,
                                                 nY,
                                                 Dir)

  M = (MDir * euclid.Matrix4.new_scale(Stem,Stem,Len).translate(0,0,0.5)).pre_translate(*Pos)
  cylV = Transform(M,cylV)

  M = (MDir * euclid.Matrix4.new_scale(Stem*2,Stem*2,Stem*3).pre_translate(0,0,Len)).pre_translate(*Pos)
  headV = Transform(M,headV)

  # Add the cylinder and the head to the renderer
  ArrowActor = VandFtoActor(headV,headF,ColorHead)
  AxisActor = VandFtoActor(cylV,cylF,ColorCyl)
  Renderer.AddActor(ArrowActor)
  Renderer.AddActor(AxisActor)

  return ArrowActor, AxisActor


if __name__ == '__main__':
  # Placing graphics primitives in a vtk scene
  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  renWin.SetSize(600,600)
  
  AddArrowToRenderer(ren,Pos=(0,0,0),Len=5,Dir=(1,0,0), ColorHead=(1,0,0), Stem = 0.1)
  AddArrowToRenderer(ren,Pos=(0,0,0),Len=5,Dir=(0,1,0), ColorHead=(0,1,0), Stem = 0.1)
  AddArrowToRenderer(ren,Pos=(0,0,0),Len=5,Dir=(0,0,1), ColorHead=(0,0,1), Stem = 0.1)

  AddVandFtoRender(ren,
                   GraphicsPrimitives.icosahedron(subdivide=5),
                   Pos=(2,2,2),
                   #Dir=(1,1,1),
                   Scale=(.01,.01,.01),
                   Color=(1,0,0)
                   )

  AddLine(ren,
          [(2,2,2),(3,3,3), (2,3,2)],
          LineWidth = 1)
  
  # enable user interface interactor
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)
  inStyle = vtk.vtkInteractorStyleSwitch()
  inStyle.SetCurrentStyleToTrackballCamera()
  iren.SetInteractorStyle(inStyle)
  
  ren.SetBackground(0.1, 0.2, 0.4)
  renWin.Render()
  iren.Start()
