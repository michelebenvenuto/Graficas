class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertexes = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix =='v':
                    self.vertexes.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                     self.faces.append([list(map(int , face.split('/'))) for face in value.split(' ')])
