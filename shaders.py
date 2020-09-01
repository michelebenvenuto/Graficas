from usefullFunctions import dot, getcolor

def gouradShader(render, **kwargs):
    w, v, u = kwargs['bar']

    tx, ty = kwargs['texture_coords']
    tcolor = render.active_texture.get_color(tx,ty)

    nA, nB, nC = kwargs['varying_normals']

    iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC

    return getcolor(
      int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )
  
def unlit(render, **kwargs):
    tx, ty = kwargs['texture_coords']

    if render.active_texture:
        texColor = render.active_texture.get_color(tx, ty)
        b = texColor[0] 
        g = texColor[1]
        r = texColor[2] 
    return getcolor(r,g,b)