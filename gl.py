from usefullFunctions import *
from obj import Obj, Texture
from math import sin, cos
from shaders import gouradShader

White = getcolor(255,255,255)
Black = getcolor(0,0,0)

class Render(object):
    def __init__(self, width, height, fileName = 'test.bmp', clearColor = Black):
        self.width = width
        self.height = height
        self.fileName = fileName
        self.clearColor = clearColor
        self.framebuffer = []
        self.viewport = None
        self.drawColor = White
        self.active_texture = None
        self.active_vertex_array = []
        self.glCreateWindow(self.width,self.height)
        self.light = V3(0,0,1)
        self.active_shader = gouradShader
        

    def glInit(self):
        return('TODO')

    def glCreateWindow(self,width,height):
        self.framebuffer = [
            [self.clearColor for x in range(width)]
            for y in range(height) 
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def glViewPort(self,x,y, width, height):
        self.viewport = Viewport(x,y,height,width)
    
    def glClear(self):
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
            for y in range(self.height) 
        ]
    
    def paintBackground(self):
        image = open(self.active_texture.path, "rb")

        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)

        width = struct.unpack("=l", image.read(4))[0]  
        height = struct.unpack("=l", image.read(4))[0] 
        image.seek(header_size)

        for y in range(height):
            for x in range(width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.framebuffer[y][x] = getcolor(r,g,b)
        image.close()

    def glClearColor(self, r,g,b):
        self.clearColor = getcolor(r,g,b)

    def glVertex(self,x,y):
        XCoordinate = round((x+1)*(self.viewport.width/2)+self.viewport.x)
        YCoordinate = round((y+1)*(self.viewport.height/2)+self.viewport.y)
        self.point(V2(XCoordinate,YCoordinate))

    def glColor(self, r,g,b):
        self.drawColor = getcolor(r,g,b)

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

    def point(self,point, color = None):
        try:
            self.framebuffer[point.y][point.x] = color or self.drawColor
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
    
    def transform(self, vertex):
        augmented_vertex = Matrix([
            [vertex.x],
            [vertex.y],
            [vertex.z],
            [1]
        ])
        transform_vertex_part1 = matrixMultiplication(self.ViewportMatrix, self.ProjectionMatix)
        transform_vertex_theVengance = matrixMultiplication(transform_vertex_part1, self.ViewMatrix)
        transform_vertex_theReturn = matrixMultiplication(transform_vertex_theVengance, self.ModelMatrix)
        transform_vertex_final = matrixMultiplication(transform_vertex_theReturn, augmented_vertex)

        transformed_vertex = transform_vertex_final.matrix

        transformed_vertex = [
            (transformed_vertex[0][0]/transformed_vertex[3][0]),
            (transformed_vertex[1][0]/transformed_vertex[3][0]),
            (transformed_vertex[2][0]/transformed_vertex[3][0]),
        ]

        return V3(*transformed_vertex)

    def load(self, filename, translate, scale, rotate):
        self.loadModelMatrix(translate, scale, rotate)

        model = Obj(filename)
        vertex_buffer_object = []

        for face in model.faces:
            for x in face:
                vertex = self.transform(V3(*model.vertexes[x[0]-1]))
                vertex_buffer_object.append(vertex)
            
            if self.active_texture:
                for x in face:
                    if(len(model.tvertexes[x[1]-1]) == 3):
                        tvertex = V3(*model.tvertexes[x[1]-1])
                        vertex_buffer_object.append(tvertex)
                    else:
                        tvertex = V3(*model.tvertexes[x[1]-1],0)
                        vertex_buffer_object.append(tvertex)
                for x in face:
                    nvertex = V3(*model.nvertexes[x[2]-1])
                    vertex_buffer_object.append(nvertex)
        
        self.active_vertex_array = iter(vertex_buffer_object)
            

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

    def triangle(self):
        A = next(self.active_vertex_array)
        B=  next(self.active_vertex_array)
        C = next(self.active_vertex_array)

        if self.active_texture:
            tA = next(self.active_vertex_array)
            tB =  next(self.active_vertex_array)
            tC = next(self.active_vertex_array)
        
        nA = next(self.active_vertex_array)
        nB = next(self.active_vertex_array)
        nC = next(self.active_vertex_array)

        xmin, xmax, ymin, ymax = bbox(A, B, C)

        normal = norm(cross(sub(B,A), sub(C,A)))
        intensity = dot(normal, self.light)
        if intensity < 0:
            return

        for x in range(xmin, xmax +1):
            for y in range(ymin, ymax+1):
                P = V2(x, y)
                w, v ,u = barycentric(A, B, C, P)
                if w<0 or v<0 or u<0:
                    continue
                
                if self.active_texture:
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u

                color = self.active_shader(
                    self,
                    triangle = (A, B, C),
                    bar = (w, v, u),
                    texture_coords = (tx, ty),
                    varying_normals = (nA, nB, nC)
                )

                z = A.z * w + B.z * v + C.z * u

                if x<0 or y<0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
                    self.point(V2(x, y), color)
                    self.zbuffer[y][x] = z

    def draw_arrays(self, polygon_type):
        if(polygon_type == 'TRIANGLE'):
            try:
                while True:
                    self.triangle()
            except StopIteration:
                print('RENDER DONE')
        elif polygon_type =='WIREFRAME':
            pass
    
    #Matrix stuff
    def loadModelMatrix(self, translate,scale,rotate):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = Matrix([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z ],
            [0, 0, 0, 1]
        ])

        a = rotate.x
        rotation_matix_x = Matrix([
            [1, 0, 0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a),  cos(a), 0],
            [0, 0, 0, 1]
        ])

        a = rotate.y
        rotation_matrix_y = Matrix([
        [cos(a), 0,  -sin(a), 0],
        [0, 1, 0, 0],
        [sin(a), 0,  cos(a), 0],
        [0, 0, 0, 1]
        ])

        a = rotate.z
        rotation_matix_z = Matrix([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotaion_matrix1 = matrixMultiplication(rotation_matix_x, rotation_matrix_y)
        final_rotation_matrix = matrixMultiplication(rotaion_matrix1, rotation_matix_z)

        scale_matrix = Matrix([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        model_matrix_1 = matrixMultiplication(translation_matrix, final_rotation_matrix)
        self.ModelMatrix = matrixMultiplication(model_matrix_1, scale_matrix)
    
    def loadViewMatrix(self, x, y, z, center):
        M = Matrix([
            [x.x, x.y, x.z, 0], 
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ])

        O = Matrix([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ])

        self.ViewMatrix = matrixMultiplication(M, O)

    def loadProjectionMatix(self, coeff):
        self.ProjectionMatix = Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ])
    
    def loadViewportMatrix(self, x = 0, y = 0):
        self.ViewportMatrix = Matrix([
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ])
    
    def lookAt(self, eye, center, up):
        z = norm(sub(eye,center))
        x = norm(cross(up, z))
        y = norm(cross(z,x))
        self.loadViewMatrix(x,y,z,center)
        self.loadProjectionMatix(-1/length(sub(eye,center)))
        self.loadViewportMatrix()


#This class will be helpfull if more viewports are required in the future
class Viewport(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width