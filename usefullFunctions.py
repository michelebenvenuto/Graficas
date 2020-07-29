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
	if (0>r>1 or 0>g>1 or 0>b>1):
		raise Exception("Color inputs must be values between 0 and 1")
	else: 
		r *= 255
		g *= 255
		b *= 255
		return bytes([b,g,r])

def bbox(*vertexes):
	xs = [ vertex.x for vertex in vertexes ]
	ys = [ vertex.y for vertex in vertexes ]

	xs.sort()
	ys.sort()

	xmin = xs[0]
	ymin = ys[0]
	xmax = xs[-1]
	ymax = ys[-1]

	return xmin, ymin, xmax, ymax

def crossProduct(v1, v2):
	return V3(
		v1.y
	)

def barycentric(A, B, C, P):
	cx, cy, cz = crossProduct(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if abs(cz)< 1:
		return -1,-1,-1

	u = cx/cz
	v = cy/cz
	w = 1- (u + v)

	return w,v,u 