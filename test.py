import pygame
import wireframe

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (185, 185, 185)
CYAN = (26, 184, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 16, 117)
CRIMSON = (148, 0, 0)
VIOLET = (186, 4, 138)
# Game dimensions
gridwidth = 50
gridheight = 50
margin = 3
# Fonts
FONT = 'Calibri'
TEXTSIZE = 70

# Converts the user's key-input to a rotation or translation
key_to_function = {
    pygame.K_LEFT: (lambda x: x.translateall('x', -10)),
    pygame.K_RIGHT: (lambda x: x.translateall('x', 10)),
    pygame.K_DOWN: (lambda x: x.translateall('y', 10)),
    pygame.K_UP: (lambda x: x.translateall('y', -10)),
    # pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    # pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q: (lambda x: x.rotateall('x', 0.1)),
    pygame.K_w: (lambda x: x.rotateall('x', -0.1)),
    pygame.K_a: (lambda x: x.rotateall('y', 0.1)),
    pygame.K_s: (lambda x: x.rotateall('y', -0.1)),
    pygame.K_z: (lambda x: x.rotateall('z', 0.1)),
    pygame.K_x: (lambda x: x.rotateall('z', -0.1))}


class ProjectionViewer:
    """
    Displays 3D objects on a Pygame screen
    """

    def __init__(self, width, height):
        """
        :param width: Width of the screen that 'run' creates
        :param height: Height of the screen that 'run' creates
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (0, 0, 0)

        self.wireframes = {}
        self.displayvertices = True
        self.displayedges = True
        self.displayfaces = True
        self.vertexcolour = (255, 255, 255)
        self.edgecolour = (200, 200, 200)
        self.vertexRadius = 4
        self.facecolour = (150, 150, 150)

    def addwireframe(self, name, frame):
        """
        Adds a named Wireframe object
        :param name: The name of the object
        :param frame: The object itself
        """
        self.wireframes[name] = frame

    def run(self):
        """
        Create a pygame screen until it is closed by the user.
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)

            self.display()
            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        print(len(self.wireframes))
        for frame in self.wireframes.values():
            if self.displayfaces:
                for face in frame.faces:
                    pygame.draw.polygon(self.screen,
                                        GREEN,
                                        [(vertex.x, vertex.y) for vertex in face.vertices],
                                        0)


            if self.displayedges:
                for edge in frame.edges:
                    pygame.draw.aaline(self.screen, self.edgecolour, (edge.start.x, edge.start.y),
                                       (edge.stop.x, edge.stop.y), 1)

            if self.displayvertices:
                for vertex in range(len(frame.vertices)):
                    font = pygame.font.SysFont(FONT, 50, True, False)
                    text = font.render(str(vertex), True, RED)
                    self.screen.blit(text, (int(frame.vertices[vertex].x),
                                            int(frame.vertices[vertex].y)))
                    pygame.draw.circle(self.screen,
                                       self.vertexcolour,
                                       (int(frame.vertices[vertex].x),
                                        int(frame.vertices[vertex].y)),
                                       self.vertexRadius, 0)


    def translateall(self, axis, d):
        """
        Translate all wireframes along a given axis by d units.
        :param axis: The axis on which the wireframes are translated
        :param d: By how many units they are translated
        """
        for frame in self.wireframes:
            self.wireframes[frame].translate(axis, d)

    def rotateall(self, axis, theta):
        """
        Rotate all wireframe about their centre, along a given axis by a given angle.
        :param axis: The axis on which the wireframes are rotated
        :param theta: By what angle they are rotated
        """
        for frame in self.wireframes:
            # centre = self.wireframes[frame].findcentre()
            centre = (300, 300, 300)
            getattr(self.wireframes[frame], 'rotate' + axis)(centre, theta)


board = []
clock = pygame.time.Clock()
pygame.init()
display = ProjectionViewer(600, 600)
for y in range(10):
    row = []
    for x in range(10):
        aisle = []
        for z in range(10):
            [i, j, k] = [(int(x) + 1 )* 100 for x in [y, x, z]]
            if [100, 200, 100] == [i, j, k] or [100, 100, 100] == [i, j, k]:
                print('hi')
                aisle.append(
                    wireframe.Wireframe(
                        [[i, j, k],
                         [i + 100, j, k],
                         [i, j - 100, k],
                         [i + 100, j - 100, k],
                         [i, j, k + 100],
                         [i + 100, j, k + 100],
                         [i, j - 100, k + 100],
                         [i + 100, j - 100, k + 100]
                         ],
                        [(n, n + 4)
                         for n in range(0, 4)] + [(n, n + 1)
                                                  for n in range(0, 8, 2)] + [(n, n + 2)
                                                                              for n in (0, 1, 4, 5)],
                        # [[[i, j, k], [i, j - 100, k], [i + 100, j - 100, k], [i + 100, j, k]],
                        # [[i, j, k], [i + 100, j, k], [i + 100, j, k + 100], [i, j, k + 100]],
                        # [[i, j, k], [i, j - 100, k], [i, j - 100, k + 100], [i, j, k + 100]],
                        # [[i + 100, j - 100, k + 100], [i, j - 100, k + 100], [i, j, k + 100], [i, j, k + 100]],
                        # [[i + 100, j - 100, k + 100], [i + 100, j - 100, k], [i + 100, j, k], [i + 100, j, k + 100]],
                        # [[i + 100, j - 100, k + 100], [i + 100, j - 100, k], [i, j - 100, k], [i, j, k + 100]],]
                    ))
                aisle[-1].addfaces(
                    [
                        [aisle[-1].vertices[0], aisle[-1].vertices[1], aisle[-1].vertices[3], aisle[-1].vertices[2]],
                        [aisle[-1].vertices[0], aisle[-1].vertices[4], aisle[-1].vertices[6], aisle[-1].vertices[2]],
                        [aisle[-1].vertices[0], aisle[-1].vertices[1], aisle[-1].vertices[5], aisle[-1].vertices[4]],
                        [aisle[-1].vertices[5], aisle[-1].vertices[7], aisle[-1].vertices[3], aisle[-1].vertices[1]],
                        [aisle[-1].vertices[5], aisle[-1].vertices[7], aisle[-1].vertices[6], aisle[-1].vertices[4]],
                        [aisle[-1].vertices[5], aisle[-1].vertices[1], aisle[-1].vertices[0], aisle[-1].vertices[4]]
                    ])
                # aisle[-1].scale(1, (300, 300))
                display.addwireframe((i, j, k), aisle[-1])
        row.append(aisle)
    board.append(row)



display.run()
