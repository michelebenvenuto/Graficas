import struct
from collections import namedtuple

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def color(r,g,b):
	return bytes([b,g,r])

def bbox(*vertices):
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]

    xs.sort()
    ys.sort()

    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]

    return xmin, xmax, ymin, ymax

#MATH STUFF

def sum(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element sum
    """
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element substraction
    """
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element multiplication
    """
    return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Scalar with the dot product
    """
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
    """
        Input: 1 size 3 vector
        Output: Scalar with the length of the vector
    """  
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    """
        Input: 1 size 3 vector
        Output: Size 3 vector with the normal of the vector
    """  
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )

def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y),
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx/cz
    v = cy/cz
    w = 1 - (cx + cy) / cz

    return w, v, u