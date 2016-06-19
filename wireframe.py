import math


class Vertex:
    """
    Defines a vertex which holds its x, y and z coordinates
    """
    def __init__(self, coordinates, colour):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.colour = colour


class Edge:
    """
    Defines an edge which holds its starting and stopping points
    """
    def __init__(self, start, stop, colour):
        self.start = start
        self.stop = stop
        self.colour = colour


class Face:
    """
    Defines an face which holds all of its vertices
    """
    def __init__(self, vertices, colour):
        self.vertices = vertices
        self.colour = colour


class Wireframe:
    """
    A wireframe object that has a given number of vertices and a given number of edges
    """
    def __init__(self, vertices=(), edges=(), faces=(), facenames=('front', 'right', 'back', 'left', 'top', 'bottom'),
                 colours=((0, 0, 0), (10, 10, 10), (50, 50, 50))):
        """
        Defines the wireframe, with vertices and edges if necessary
        :param vertices: The wireframe's vertices
        :param edges: The wireframe's edges
        """
        self.vertexcolour, self.edgecolour, self.facecolour = colours
        self.vertices = []
        self.edges = []
        self.faces = {}
        self.show = True
        if len(vertices) > 0:
            self.addvertices(vertices)
        if len(edges) > 0:
            self.addedges(edges)
        if len(faces) > 0:
            self.addfaces(faces, facenames)

    def addvertices(self, vertexlist):
        """
        Allows the program to add in a given number of vertices
        :param vertexlist: The list of vertices to be added
        """
        for vertex in vertexlist:
            if type(vertex) == Vertex:
                self.vertices.append((vertex))
            else:
                self.vertices.append(Vertex(vertex, self.vertexcolour))

    def addedges(self, edgelist):
        """
        Allows the program to add in a given number of edges
        :param edgelist: The list of edges to be added
        """
        for (start, stop) in edgelist:
            self.edges.append(Edge(self.vertices[start], self.vertices[stop], self.edgecolour))

    def addfaces(self, facelist, facenames=('front', 'right', 'back', 'left', 'top', 'bottom')):
        """
        Allows the program to add in a given number of face
        :param facelist: The list of faces to be added
        """
        for i in range(len(facelist)):
            self.faces[facenames[i]] = Face(facelist[i], self.facecolour)

    def translate(self, axis, d):
        """
        Translate each vertex of a wireframe by 'd' in the given axis, 'axis'
        :param axis: The axis in which the wireframe is translated
        :param d: The amount by which the wireframe is translated
        """

        if axis in ['x', 'y', 'z']:
            for vertex in self.vertices:
                setattr(vertex, axis, getattr(vertex, axis) + d)

    def scale(self, centre, scale):
        """ Scale the wireframe from the centre of the screen """

        for vertex in self.vertices:
            vertex.x = centre[0] + scale * (vertex.x - centre[0])
            vertex.y = centre[1] + scale * (vertex.y - centre[1])
            vertex.z *= scale

    def findcentre(self):
        """ Find the centre of the wireframe. """

        num_vertices = len(self.vertices)
        meanx = sum([vertex.x for vertex in self.vertices]) / num_vertices
        meany = sum([vertex.y for vertex in self.vertices]) / num_vertices
        meanz = sum([vertex.z for vertex in self.vertices]) / num_vertices

        return meanx, meany, meanz

    def rotatex(self, centre, radians):
        for vertex in self.vertices:
            y = vertex.y - centre[1]
            z = vertex.z - centre[2]
            d = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            vertex.z = centre[2] + d * math.cos(theta)
            vertex.y = centre[1] + d * math.sin(theta)

    def rotatey(self, centre, radians):
        for vertex in self.vertices:
            x = vertex.x - centre[0]
            z = vertex.z - centre[2]
            d = math.hypot(x, z)
            theta = math.atan2(x, z) + radians
            vertex.z = centre[2] + d * math.cos(theta)
            vertex.x = centre[0] + d * math.sin(theta)

    def rotatez(self, centre, radians):
        for vertex in self.vertices:
            x = vertex.x - centre[0]
            y = vertex.y - centre[1]
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            vertex.x = centre[0] + d * math.cos(theta)
            vertex.y = centre[1] + d * math.sin(theta)

if __name__ == "__main__":
    cube_vertices = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    cube = Wireframe()
    cube.addvertices(cube_vertices)
    cube.addedges([(n, n + 4) for n in range(0, 4)])
    cube.addedges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addedges([(n, n + 2) for n in (0, 1, 4, 5)])

    # cube.outputvertices()
    # cube.outputedges()
