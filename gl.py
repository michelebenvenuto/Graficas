from usefullFunctions import char, word, dword, color

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
        self.point(XCoordinate,YCoordinate)

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

    def point(self,x,y):
        self.framebuffer[y][x] = self.drawColor

    def line(self, x0,y0, x1, y1):
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
                self.point(y , x)
            else: 
                self.point(x,y)
            
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
            self.line(inicialX, inicialY, finalX,  finalY)

#This class will be helpfull if more viewports are required in the future
class Viewport(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width




