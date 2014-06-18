import math
from euclid import Vector3

def icosahedron(subdivide=0):
    """Construct a 20-sided polyhedron"""
    faces = [ \
        (0,1,2),
        (0,2,3),
        (0,3,4),
        (0,4,5),
        (0,5,1),
        (11,7,6),
        (11,8,7),
        (11,9,8),
        (11,10,9),
        (11,6,10),
        (1,6,2),
        (2,7,3),
        (3,8,4),
        (4,9,5),
        (5,10,1),
        (6,7,2),
        (7,8,3),
        (8,9,4),
        (9,10,5),
        (10,6,1)
        ]
    verts = [ \
        ( 0.000,  0.000,  1.000 ),
        ( 0.894,  0.000,  0.447 ),
        ( 0.276,  0.851,  0.447 ),
        (-0.724,  0.526,  0.447 ),
        (-0.724, -0.526,  0.447 ),
        ( 0.276, -0.851,  0.447 ),
        ( 0.724,  0.526, -0.447 ),
        (-0.276,  0.851, -0.447 ),
        (-0.894,  0.000, -0.447 ),
        (-0.276, -0.851, -0.447 ),
        ( 0.724, -0.526, -0.447 ),
        ( 0.000,  0.000, -1.000 ) ]
    for i in range(subdivide):
        verts,faces = subdivide_triangles(verts, faces)
    return verts, faces

def octohedron(subdivide=0):
    """Construct an eight-sided polyhedron.
    If do_hemisphere is true, then a hemisphere in the z direction
    is returned.
    """
    f = math.sqrt(2.0) / 2.0
    verts = [ 
        ( 0,  0, 1),
        (-f,  f,  0),
        ( f,  f,  0),
        ( f, -f,  0),
        (-f, -f,  0),
        ( 0,  0,  -1) ]

    faces = [ 
        (0, 2, 1),
        (0, 3, 2),
        (0, 4, 3),
        (0, 1, 4),
        (5, 1, 2),
        (5, 2, 3),
        (5, 3, 4),
        (5, 4, 1) ]
    for i in range(subdivide):
        verts,faces = subdivide_triangles(verts, faces)
    return verts, faces

def cube():
    """Construct a cube"""
    f = -0.5
    verts = [ \
        (-f,-f,-f),
        (f,-f,-f),
        (f,f,-f),
        (-f,f,-f),
        (-f,-f,f),
        (f,-f,f),
        (f,f,f),
        (-f,f,f)]
    faces = [ \
        (0,3,2),
        (0,2,1),
        (4,5,6),
        (4,6,7),
        (0,1,5),
        (0,5,4),
        (1,2,6),
        (1,6,5),
        (2,3,7),
        (2,7,6),
        (3,0,4),
        (3,4,7)
        ]
    return verts, [list(reversed(f)) for f in faces]


def Box(BoxLimits=[0,1,0,1,0,1]):
    """Construct a Box from BoundingBox limits"""
    verts = [ \
        (BoxLimits[0],BoxLimits[2],BoxLimits[4]),
        (BoxLimits[1],BoxLimits[2],BoxLimits[4]),
        (BoxLimits[1],BoxLimits[3],BoxLimits[4]),
        (BoxLimits[0],BoxLimits[3],BoxLimits[4]),
        (BoxLimits[0],BoxLimits[2],BoxLimits[5]),
        (BoxLimits[1],BoxLimits[2],BoxLimits[5]),
        (BoxLimits[1],BoxLimits[3],BoxLimits[5]),
        (BoxLimits[0],BoxLimits[3],BoxLimits[5])
        ]
    faces = [ \
        (0,1,2,3),
        (0,1,5,4),
        (4,5,6,7),
        (6,7,3,2),
        (0,3,7,4),
        (1,2,6,5),                        
        ]
    return verts, faces#[list(reversed(f)) for f in faces]

        
def pyramid(subdivide=0):
    """Half an Octahedron. May be used as an arrow or as an
    hemispher is subdevide is applied"""
    f = math.sqrt(2.0) / 2.0
    verts = [ \
        ( 0,  0, 1),
        (-f,  f,  0),
        ( f,  f,  0),
        ( f, -f,  0),
        (-f, -f,  0),
        ]
    faces = [ \
        (0, 2, 1),
        (0, 3, 2),
        (0, 4, 3),
        (0, 1, 4),
        (1, 2, 3),
        (1,3,4),
    ]
    for i in range(subdivide):
        verts,faces = subdivide_triangles(verts, faces)
    return verts, faces

def disk(num_slices=8):
    """Return a disk with num_slices slices. Tiled from first vertex"""

    faces = []
    verts = []
    r = 0.5
    dt = math.pi*2.0/num_slices
    for i in range(num_slices):
        theta = dt * i
        if i>0 and i < num_slices-1:
            faces += [(0,i+1,i)]
        verts += [(r*math.cos(theta),r*math.sin(theta),0)]
    return verts, faces

def cone(num_slices=8):
    """Return a cone with the bases at z=0 and the apex at z=1"""
    v,f = disk(num_slices)
    # Add apex
    v += [(0,0,1)]

    # Add side walls
    for i in range(num_slices):
        f += [(i,(i+1)%num_slices, num_slices)]
    return v,f
    
def cylinder(num_slices=8):
    """Return a cylinder with num_slices = slices."""
    vt,ft = disk(num_slices)
    vb,fb = vt[:],ft[:]

    # Translate top and bottom vertices
    vt = [(x,y,-0.5) for x,y,z in vt]
    vb = [(x,y,0.5) for x,y,z in vt]

    # Reverse all the bottom faces and add num_slices to the indexes
    fb_new = []
    for p1,p2,p3 in fb:
        fb_new += [(p1+num_slices,p3+num_slices,p2+num_slices)]

    # Join together
    v = vt + vb
    f = ft + fb_new

    # Add side walls
    for i in range(num_slices):
        f += [(i,(i+1)%num_slices, i+num_slices),
              ((i+1)%num_slices, (i+1)%num_slices+num_slices, i+num_slices)
              ]

    return v,f
    

def subdivide_triangles(verts, faces):
    """Subdivide each triangle into four triangles, pushing verts to the unit sphere"""
    triangles = len(faces)
    for faceIndex in xrange(triangles):
    
        # Create three new verts at the midpoints of each edge:
        face = faces[faceIndex]
        a,b,c = (Vector3(*verts[vertIndex]) for vertIndex in face)
        verts.append((a + b).normalized()[:])
        verts.append((b + c).normalized()[:])
        verts.append((a + c).normalized()[:])

        # Split the current triangle into four smaller triangles:
        i = len(verts) - 3
        j, k = i+1, i+2
        faces.append((i, j, k))
        faces.append((face[0], i, k))
        faces.append((i, face[1], j))
        faces[faceIndex] = (k, j, face[2])

    return verts, faces

