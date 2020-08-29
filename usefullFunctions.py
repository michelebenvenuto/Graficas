import struct
import random
from math import sqrt
from collections import namedtuple

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def getcolor(r,g,b):
	return bytes([b,g,r])

def midPoint(start, end):
    return round((start+end)/2)


def JupiterShader(x, y,filler):
    # X goes from 253 to 503
    # Y goes from 255 to 505
    xmax = 503
    xmin = 253
    ymax = 505
    ymin = 255
    xmidPoint = midPoint(xmax,xmin)
    yMidPoint = midPoint(ymax,ymin)
    yLowerQuarter = midPoint(ymin, yMidPoint)
    yUpperQuarter = midPoint(yMidPoint, ymax)

    radius_counter = 1
    increase_radius = True
    intensity = 1

    while(increase_radius):
        if((x-xmidPoint)**2 + (y - yMidPoint)**2 <= radius_counter**2):
            increase_radius = False
        else:
            radius_counter += 1
            intensity-=0.005
            
    lightBrown = getcolor(round(210* intensity), round(105* intensity), round(30 *intensity))
    sandybrown = getcolor(round(244* intensity), round(164* intensity), round(96 *intensity))
    darkBrown = getcolor(round(139* intensity), round(69* intensity), round(19 *intensity))
    navajowhite = getcolor(round(255* intensity), round(222* intensity), round(173 *intensity))

    
    offset = random.randint(0,5)
    if((x-xmidPoint)**2 + (y - yLowerQuarter)**2 <=500+offset ):
        return lightBrown
    elif((x-xmidPoint)**2 + (y - yLowerQuarter)**2 <=800 +offset or y> yUpperQuarter + 30 + offset or y < yLowerQuarter -30 +offset):
        return sandybrown
    elif(y in range(yMidPoint-70 +offset, yMidPoint-30 - offset) or y in range(yMidPoint+30 + offset, yMidPoint+60 - offset)):
        return darkBrown
    else:
        return navajowhite

def bbox(*vertices):
    xs = [ vertex.x for vertex in vertices ]
    ys = [ vertex.y for vertex in vertices ]

    xs.sort()
    ys.sort()

    xmin = round(xs[0])
    xmax = round(xs[-1])
    ymin = round(ys[0])
    ymax = round(ys[-1])

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

class Matrix(object):
    def __init__(self, arrayOfArrays):
        self.createMatrix(arrayOfArrays)

    def createMatrix(self, arrayOfArrays):
        self.rows = len(arrayOfArrays)

        columnChecker = len(arrayOfArrays[0])

        for row in arrayOfArrays:
            if len(row) != columnChecker:
                raise Exception("Rows of a matrix have and inconsisten numer of colums")
            else:
                continue
        
        self.columns = columnChecker
        self.matrix = arrayOfArrays

    def __str__(self):
        result = '(\n'
        for row in self.matrix:
            result = result + '['
            for column in row:
                result =result + str(column) + ' '
            result = result + ']'
            result = result + '\n'
        result = result + ')'
        return result

def matrixMultiplication(a,b):
    if(a.columns != b.rows):
        raise Exception('Size of the given matrixes are not compatible')
    else:
        resultArray = []
        #Get the size of the result matrix 
        for row in range(a.rows):
            rowToAppend = []
            for column in range(b.columns):
                rowToAppend.append(0)
            resultArray.append(rowToAppend)
        #Populate the matrix with the correct numbers
        for i in range(a.rows):
            for j in range(b.columns):
                for k in range(b.rows):
                    resultArray[i][j] += a.matrix[i][k] * b.matrix[k][j]

        return Matrix(resultArray)


