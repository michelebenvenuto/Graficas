from gl import Render
from obj import Texture
from usefullFunctions import Matrix, matrixMultiplication, V3, norm

r = Render(1024, 1024)
r.lookAt(V3(0, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
t= Texture('models/surface.bmp')
r.active_texture = t
r.light= norm(V3(1, 1, 1))
r.load('models/earth.obj',[0,0.2,20],[0.2,0.2,1], [0,0,0])
r.draw_arrays('TRIANGLE')
t= Texture('models/moon.bmp')
r.active_texture = t
r.load('models/sphere.obj',[0,-0.8,50],[2,1,1], [0,0,0])
r.draw_arrays('TRIANGLE')
t= Texture('models/saturnmap.bmp')
r.active_texture = t
r.load('models/saturn.obj',[-1.5,1,-50],[1,1,1], [0,0,0])
r.draw_arrays('TRIANGLE')
r.glFinish()
