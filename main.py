from gl import Render
from obj import Texture
from usefullFunctions import Matrix, matrixMultiplication, V3, norm
from shaders import unlit, gouradShader

r = Render(1024, 1024)
r.lookAt(V3(0, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
r.light= norm(V3(0, 0, 1))

t= Texture('models/space.bmp')
r.active_texture = t
r.paintBackground()

t= Texture('models/surface.bmp')
r.active_texture = t
r.load('models/earth.obj',[0,0.2,0],[0.2,0.2,1], [0,0,0])
r.draw_arrays('TRIANGLE')
t= Texture('models/moon.bmp')
r.active_texture = t
r.active_shader = unlit
r.load('models/sphere.obj',[0,-0.8,50],[2,1,1], [0,0,0])
r.draw_arrays('TRIANGLE')
r.light = norm(V3(1,1,1))
t= Texture('models/saturnmap.bmp')
r.active_texture = t
r.active_shader = gouradShader
r.load('models/saturn.obj',[-1.5,1,-50],[1,1,1], [0,0,0])
r.draw_arrays('TRIANGLE')
t= Texture('models/satelite.bmp')
r.active_texture = t
r.load('models/satelite.obj',[-0.4,0,30],[0.025,0.025,1], [0,0,0.2])
r.draw_arrays('TRIANGLE')
t= Texture('models/viper.bmp')
r.active_texture = t
r.load('models/viper.obj',[0.4,-0.2,20],[0.1,0.1,1], [0.1,0,-0.2])
r.draw_arrays('TRIANGLE')



r.glFinish()
