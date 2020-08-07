from gl import Render

r = Render(800, 800)

r.load('sphere.obj',[2,2,0],[200,200,200])

r.glFinish()