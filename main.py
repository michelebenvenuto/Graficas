from gl import Render

r = Render(500, 600)

r.glClearColor(1,0,0)
r.glClear()
r.glViewPort(0,50,100,50)
r.glLine(0,0,1,1)
r.glColor(0,0,1)
r.line(499,0,50,50)
r.glFinish()