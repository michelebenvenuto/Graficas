from gl import Render

r = Render(800, 800)

r.load('sphere.obj',[1.5,1.5,0],[250,250,250])

r.glFinish()