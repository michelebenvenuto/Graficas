from usefullFunctions import char, word, dword, color, V2, V3
from obj import Obj

White = color(1,1,1)

class Render(object):
    def __init__(self, width, height, fileName = 'test.bmp', clearColor = White):
        self.width = width
        self.height = height
        self.fileName = fileName
        self.clearColor = clearColor
        self.framebuffer = []
        self.viewport = None
        self.drawColor = White
        self.glCreateWindow(self.width,self.height)

    def glInit(self):
        return('TODO')

    def glCreateWindow(self,width,height):
        self.framebuffer = [
            [White for x in range(width)]
            for y in range(height) 
        ]
    
    def glViewPort(self,x,y, width, height):
        self.viewport = Viewport(x,y,height,width)
    
    def glClear(self):
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
            for y in range(self.height) 
        ]

    def glClearColor(self, r,g,b):
        self.clearColor = color(r,g,b)

    def glVertex(self,x,y):
        XCoordinate = round((x+1)*(self.viewport.width/2)+self.viewport.x)
        YCoordinate = round((y+1)*(self.viewport.height/2)+self.viewport.y)
        self.point(V2(XCoordinate,YCoordinate))

    def glColor(self, r,g,b):
        self.drawColor = color(r,g,b)

    def glFinish(self):
        f = open(self.fileName, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width*self.height*3))
        f.write(dword(0))
        f.write(dword(14 + 40 ))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width*self.height*3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()

    def point(self,point):
        try:
            self.framebuffer[point.y][point.x] = self.drawColor
        except:
            pass
        
    def line(self, A, B):
        x0 = A.x
        y0 = A.y
        x1 = B.x
        y1 = B.y
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        steep = dy> dx

        if steep :
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        threshold = 0.5 * 2 * dx

        y = y0
        

        for x in range(x0, x1+1):
            if steep:
                self.point(V2(y , x))
            else: 
                self.point(V2(x,y))
            
            offset += dy * 2
            if offset >= threshold:
                y+=1 if y0 < y1 else -1
                threshold += 2* dx 

    def glLine(self, x0, y0, x1, y1):
        if -1>x0>1 or -1>x0>1 or -1>x0>1 or -1>x0>1:
            raise Exception("One of the arguments of glLine is greater than 1 or smaller than -1")
        else:
            inicialX = round((x0+1)*(self.viewport.width/2)+self.viewport.x)
            inicialY = round((y0+1)*(self.viewport.height/2)+self.viewport.y)
            finalX = round((x1+1)*(self.viewport.width/2)+self.viewport.x)
            finalY = round((y1+1)*(self.viewport.height/2)+self.viewport.y)
            self.line(V2(inicialX, inicialY), V2(finalX,  finalY))
    
    def load(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j+1)% vcount][0]

                v1 = model.vertexes[f1 -1]
                v2 = model.vertexes[f2 -1]

                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])

                self.line(V2(x1, y1), V2(x2, y2))

    def paint(self, points):
        pointCount = len(points)
        for i in range(pointCount):
            self.line(V2(points[i][0], points[i][1]), V2(points[(i+1)%pointCount][0], points[(i+1)%pointCount][1]))
        topPoint = None
        bottomPoint = None
        leftPoint = None
        rightPoint = None
        for point in points:
            if(leftPoint == None or point[0]<= leftPoint ):
                leftPoint = point[0]
            if (rightPoint == None or point[0] >= rightPoint  ):
                rightPoint = point[0]
            if (topPoint ==None or point[1] >= topPoint  ):
                topPoint = point[1]
            if (bottomPoint == None or point[1] <= bottomPoint  ):
                bottomPoint = point[1]
        halfPoint = V2(round((leftPoint+ rightPoint)/2), round((bottomPoint+ topPoint)/2))
        border = []
        for y in range( bottomPoint, topPoint+1):
            for x in range(leftPoint, rightPoint+1):
                if(self.framebuffer[y][x]!= self.clearColor):
                    border.append([x,y])
        for point in border:
            self.line(halfPoint, V2(point[0], point[1]))

    # def triangle(self, A, B, C, color):
    #     xmin, xmax, ymin, ymax = bbox(A, B, C)

    #     for x in range(xmin, xmax +1):
    #         for y in range(ymin, ymax):
    #             P = V2(x, y)
    #             w, v ,u = barycentrinc(A,B,C, P)
    #             if w<0 or v<0 or u<0:
    #                 continue

    #             self.point(x, y)

#This class will be helpfull if more viewports are required in the future
class Viewport(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width