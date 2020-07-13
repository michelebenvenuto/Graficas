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

#This class will be helpfull if more viewports are required in the future
class Viewport(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

Render = Render(100,100)

Render.glClearColor(1,0,0)
Render.glClear()
Render.glViewPort(0,50,100,50)
Render.glColor(0,0,1)
Render.glVertex(0,0)
Render.glFinish()
