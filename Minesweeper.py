import random
import pygame
import misc
import wireframe

pygame.init()
pygame.display.set_mode((600, 600))

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

# Images
#mine = pygame.image.load('Images/Mine.bmp').convert()
#tile = pygame.image.load('Images/Tile.bmp').convert()
#flag = pygame.image.load('Images/Flag.bmp').convert()
#wronglyflagged = pygame.image.load('Images/WronglyFlagged.bmp').convert


def createboard(x, y, z, mines):
    """
    Creates the board on which the game is based
    :param x: How wide the board must be
    :param y: How long the board must be
    :param z: How deep the board must be
    :param mines: The list of all of the mines to be placed into the board
    :return: Returns the created board
    """
    board = []
    for i in range(0, y):
        column = []
        for j in range(0, x):
            aisle = []
            for k in range(0, z):
                if [j, i, k] in mines:
                    aisle.append({'display': '_', 'solution': 'x', 'flagged': False, 'pressed': False,
                                  'coordinates': [str(j), str(i), str(k)]})
                else:
                    aisle.append({'display': '_', 'solution': '', 'flagged': False, 'pressed': False,
                                  'coordinates': [str(j), str(i), str(k)]})
            column.append(aisle)
        board.append(column)
    return board


def choose(board, y, x, z):
    """
    Takes the given coordinates that the user has chosen and returns the board state after they have selected it
    :param board: The board that is edited
    :param y: The y coordinate of the user's selection
    :param x: The x coordinate of the user's selection
    :param z: The z coordinate of the user's selection
    :return: The board state after their selection or just 'x' if the user hit a bomb
    """
    count = findadjacent(board, x, y, z, 'x')
    # Works out how many bombs are adjacent to the square
    if board[y][x][z]['solution'] == 'x':
        return 'x'
    board[y][x][z]['display'] = count
    if count == 0:
        board = spread(board, x, y, z)
        # Runs the zero recursion function if they select a 0
    return board


def spread(board, x, y, z):
    """
    Checks each adjacent square to see if it is a zero, if it is, then the program repeats this function, recurring
    until a square is not zero
    :param board: The board that is edited
    :param y: The y coordinate of the zero
    :param x: The x coordinate of the zero
    :param z: The z coordinate of the user's selection
    :return: The board's new state
    """
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    zs = [z - 1, z, z + 1]
    # ToDo: Possible item based dimension system?!?
    # How to represent 4 dimensions?!?
    for i in xs:
        for j in ys:
            for k in zs:
                if i >= len(board[0]) or j >= len(board) or k >= len(board[0][0]) or -1 in [i, j, k] or \
                        (i == x and j == y and k == z):
                    continue
                count = findadjacent(board, i, j, k, 'x')
                if count == 0 and board[j][i][k]['display'] != count:
                    board[j][i][k]['display'] = count
                    board = spread(board, i, j, k)
                board[j][i][k]['display'] = count
    return board


def findadjacent(board, x, y, z, char):
    """
    Counts the number of occurrences of a specific phrase in any of the squares adjacent to that given by x and y
    :param board: The board that is edited
    :param y: The y coordinate of the point
    :param x: The x coordinate of the point
    :param z: The z coordinate of the point
    :param char: The character that is counted
    :return: The board's new state
    """
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    zs = [z - 1, z, z + 1]
    if board[y][x][z]['solution'] == 'x':
        return 'x'
    for i in xs:
        for j in ys:
            for k in zs:
                if i >= len(board[0]) or j >= len(board) or k >= len(board[0][0]) or -1 in [i, j, k] or \
                        (i == x and j == y and k == z):
                    continue
                elif board[j][i][k]['solution'] == char:
                    count += 1
    return count


def flagsquare(board, x, y, z):
    """
    Toggles whether a square is flagged or not
    :param board: The board that is edited
    :param y: The y coordinate of the zero
    :param x: The x coordinate of the zero
    :param z: The z coordinate of the zero
    :return: The board's new state
    """
    if board[x][y][z]['display'] == '_':
        if board[x][y][z]['flagged'] is True:
            board[x][y][z]['flagged'] = False
        else:
            board[x][y][z]['flagged'] = True
    return board


def checkinput(screen, question, typecheck, startrange=float('-inf'), endrange=float('inf')):
    """
    It takes in a question to ask the user, asks it, checks if it is a valid input
    (if not they must re-enter it) and returns their final answer
    :parameter screen: The screen upon which the question is asked
    :parameter question: the question that is posed to the user
    :parameter typecheck: The data type that the user is required to enter
    :parameter startrange: The lower end of the range to which, if a float or integer is required, the user's input must
     conform
    :parameter endrange: The upper end of the range to which, if a float or integer is required, the user's input must
    conform
    :returns answer: the first value that the user has inputted that conforms to all of the requirements
    """
    # set valid to false so that the while loop actually runs
    valid = False
    # repeat the checking process until the answer is acceptable
    answer = ''
    while valid is False:
        # try the following code, if there is an exception go to that except statement
        try:
            if typecheck == 'yesno':
                answer = {'y': True, 'yes': True, 'n': False, 'no': False}[misc.ask(screen, question).lower()]
                valid = True
            else:
                # ask the user the question then try to force the answer into the required data type
                answer = typecheck(misc.ask(screen, question))
                # check if the user's input is within the required bounds if it is a float or integer
                if (typecheck == int or typecheck == float) and (answer < startrange or answer > endrange):
                    # ask the user the question again, explaining what range it should be in
                    print('Input out of required range (%s to %s)' % (startrange, endrange))
                # if the user's input has passed all of the hurdles
                else:
                    # let the input through
                    valid = True
        # if a value error occurs, explain that it occurred and tell them to try again
        except ValueError:
            print('ValueError, try again')
        # explain that they must input yes or no
        except KeyError:
            print('Input is not Yes or No')
            # Restart because of the exception
    return answer


"""
def main():

    The main function with the game loop

    mines = []
    coords = []
    # print(mines)
    while running:
        temp = ''
        for event in pygame.event.get():
        # print(face)

        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
        text = font.render(face, True, BLACK)
        pygame.draw.rect(screen, GREY,
                         (0, window_size[1] - extra, window_size[0],
                          window_size[1] - pygame.font.Font.size(font, face)[1],
                          # pygame.font.Font.size(font, face)[0],
                          ))
        screen.blit(text, [window_size[0] / 2 - pygame.font.Font.size(font, face)[0] / 2,
                           (gridheight + margin) * boardy])
        pygame.display.flip()
        flagged = 0
"""

# Converts the user's key-input to a rotation or translation
key_to_function = {
    pygame.K_LEFT: (lambda n: n.translateall('x', -10)),
    pygame.K_RIGHT: (lambda n: n.translateall('x', 10)),
    pygame.K_DOWN: (lambda n: n.translateall('y', 10)),
    pygame.K_UP: (lambda n: n.translateall('y', -10)),
    # pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    # pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q: (lambda n: n.rotateall('x', 0.1)),
    pygame.K_w: (lambda n: n.rotateall('x', -0.1)),
    pygame.K_a: (lambda n: n.rotateall('y', 0.1)),
    pygame.K_s: (lambda n: n.rotateall('y', -0.1)),
    pygame.K_z: (lambda n: n.rotateall('z', 0.1)),
    pygame.K_x: (lambda n: n.rotateall('z', -0.1))}


class ProjectionViewer:
    """
    Displays 3D objects on a Pygame screen
    """

    def __init__(self):
        """
        Runs start up
        """
        self.wireframes = {}
        self.screen = pygame.display.set_mode((600, 600))
        self.boardx = checkinput(self.screen, 'How wide would you like the board to be? ', int, startrange=0,
                                 endrange=40)
        self.boardy = checkinput(self.screen, 'How long would you like the board to be? ', int, startrange=0,
                                 endrange=15)
        self.boardz = checkinput(self.screen, 'How deep would you like the board to be? ', int, startrange=0,
                                 endrange=5)
        self.mineno = checkinput(self.screen, 'How many mines would you like there to be? ', int, startrange=0,
                                 endrange=(self.boardx * self.boardy))
        for y in range(self.boardy):
            for x in range(self.boardx):
                for z in range(self.boardz):
                    [i, j, k] = [(int(n) + 1) * 100 for n in [y, x, z]]
                    n = wireframe.Wireframe(
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
                    )
                    n.addfaces([
                        [n.vertices[0], n.vertices[1], n.vertices[3], n.vertices[2]],
                        [n.vertices[0], n.vertices[4], n.vertices[6], n.vertices[2]],
                        [n.vertices[0], n.vertices[1], n.vertices[5], n.vertices[4]],
                        [n.vertices[5], n.vertices[7], n.vertices[3], n.vertices[1]],
                        [n.vertices[5], n.vertices[7], n.vertices[6], n.vertices[4]],
                        [n.vertices[5], n.vertices[1], n.vertices[0], n.vertices[4]]
                    ])
                    # n.scale(1, (300, 300))
                    self.addwireframe((i, j, k), n)

        mines = []
        for i in range(self.mineno):
            coords = [random.randrange(0, self.boardx),
                      random.randrange(0, self.boardy),
                      random.randrange(0, self.boardz)]
            while coords in mines:
                coords = [random.randrange(0, self.boardx),
                          random.randrange(0, self.boardy),
                          random.randrange(0, self.boardz)]
            mines.append(coords)
        self.board = createboard(self.boardx, self.boardy, self.boardz, mines)
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                for k in range(0, len(self.board[i][j])):
                    self.board[i][j][k]['solution'] = findadjacent(self.board, j, i, k, 'x')

        # self.width = (gridwidth * self.boardx) + (margin * self.boardx + 4)
        # self.height = (gridheight * self.boardy) + (margin * self.boardy + 4)
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('3D Minesweeper')
        self.background = (0, 0, 0)

        self.displayvertices = True
        self.displayedges = True
        self.displayfaces = True
        self.displaynumbers = True
        self.vertexcolour = (255, 255, 255)
        self.edgecolour = (200, 200, 200)
        self.vertexRadius = 4
        facecolour = (150, 150, 150)
        for frame in self.wireframes:
            for face in self.wireframes[frame].faces.values():
                if frame == (100, 100, 100):
                    face.colour = BLUE
                else:
                    face.colour = facecolour

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
        temp = ''
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y, z = [int(i) for i in input('Which tile would you like to select? ').split()]
                    if self.board[y][x][z]['flagged'] is False:
                            temp = choose(self.board, y, x, z)
                            if temp != 'x':
                                self.board = temp
                    for face in self.wireframes[tuple((i + 1) * 100 for i in (x, y, z))].faces:
                        self.wireframes[tuple((i + 1) * 100 for i in (x, y, z))].faces[face].colour = CYAN
                    """
                    # User clicks the mouse. Get the position + Deep copy it into an integer not a variable or it will
                    # change as the mouse changes, messing up which square is selected
                    pos = tuple((int(i) for i in pygame.mouse.get_pos()))
                    # if pos[1] < (gridheight + margin) * self.boardy and pos[0] < (gridwidth + margin) * self.boardx:
                    for frame in self.wireframes.values():
                        for face in frame.faces.keys():
                            # print(pos[0])
                            # print([vertex.x for vertex in face.vertices])
                            if frame.faces[face]['face'].vertices[0].x < pos[0] \
                                    < frame.faces[face]['face'].vertices[1].x and \
                                            frame.faces[face]['face'].vertices[2].x > pos[0] \
                                            > frame.faces[face]['face'].vertices[3].x:
                                if frame.faces[face]['face'].vertices[0].y > pos[1] > frame.faces[face]['face'].vertices[2].y and \
                                            frame.faces[face]['face'].vertices[1].y > pos[1] > frame.faces[face]['face'].vertices[3].y:
                                    frame.faces[face]['colour'] = GREEN
                    # Change the x/y screen coordinates to grid coordinates

                    column = abs(1)
                    row = abs(pos[1] - margin) // (gridheight + margin)
                    # for i in board:
                    #    field = ''
                    #    for j in i:
                    #        field += str(j[0]['solution'])
                    #    print(field)
                    # print([x, y, z])
                    # print(board[y][x][z])

                    #if event.button == 1:
                    #    # board[y][x][z]['pressed'] = True
                    #    # elif event.type == pygame.MOUSEBUTTONUP:
                    #    # if event.button == 1:
                    #    if self.board[y][x][z]['flagged'] is False:
                    #        temp = choose(self.board, y, x, z)
                    #        if temp != 'x':
                    #            self.board = temp
                    #elif event.button == 3:
                        # print('button 3')
                    #    self.board = flagsquare(self.board, y, x, z)
                    """
            flagged = 0
            for i in self.board:
                for j in i:
                    for k in j:
                        if k['flagged'] == True and k['solution'] == 'x':
                            flagged += 1
            self.display()
            clock.tick(30)

            if temp == 'x' or flagged == self.mineno:
                self.screen.fill(GREY)
                if temp == 'x':
                    message = 'GAME OVER!'
                elif flagged == self.mineno:
                    message = 'YOU WIN!'
                font = pygame.font.SysFont(FONT, 50, True, False)
                text = font.render(message, True, BLACK)
                pygame.draw.rect(self.screen, GREY,
                                 (self.width / 2 - pygame.font.Font.size(font, message)[0] / 2,
                                  self.height / 2 - pygame.font.Font.size(font, message)[1] / 2,
                                  pygame.font.Font.size(font, message)[0],
                                  pygame.font.Font.size(font, message)[1] - 5,
                                  ))
                self.screen.blit(text, (self.width / 2 - pygame.font.Font.size(font, message)[0] / 2,
                                        self.height / 2 - pygame.font.Font.size(font, message)[1] / 2))
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif (event.type == pygame.KEYDOWN and event.key == 13) or event.type == pygame.MOUSEBUTTONDOWN:
                            main()

            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        total = 0
        #print(self.wireframes)
        #for i in sorted(self.wireframes,
        #                key=lambda wframe: self.wireframes[wframe].findcentre()[2],
        #                reverse=True):
        #    print(i)
        for frame in sorted(self.wireframes,
                            key=lambda wframe: self.wireframes[wframe].findcentre()[2],
                            reverse=True):
            #if frame[0] == 100 or frame[1] == 100 or frame[2] == 100 or frame[0] == self.boardx * 100 or \
            #                frame[1] == self.boardx * 100 or frame[2] == self.boardx * 100:
            if self.displayfaces:
                for face in sorted(self.wireframes[frame].faces.values(),
                                   key=lambda faces: max([vertex.z for vertex in faces.vertices])):
                    #print(face)
                    total += 1
                    pygame.draw.polygon(self.screen,
                                        face.colour,
                                        [(vertex.x, vertex.y) for vertex in face.vertices],
                                        0)
                    font = pygame.font.SysFont(FONT, 50, True, False)
                    text = font.render(str(self.board[int(frame[1]/100) -1][int(frame[0]/100) -1][int(frame[2]/100) -1]['display']), True, RED)
                    #self.screen.blit(text, (int(sum([(vertex.x) for vertex in face['face'].vertices]) / len(face['face'].vertices)),
                    #                       int(sum([(vertex.y) for vertex in face['face'].vertices]) / len(face['face'].vertices))))
                    self.screen.blit(text, (int(self.wireframes[frame].findcentre()[0]),
                                           int(self.wireframes[frame].findcentre()[1])))

            if self.displayvertices:
                for vertex in range(len(self.wireframes[frame].vertices)):
                    # font = pygame.font.SysFont(FONT, 50, True, False)
                    # text = font.render(str(vertex), True, RED)
                    # self.screen.blit(text, (int(self.wireframes[frame].vertices[vertex].x),
                    #                        int(self.wireframes[frame].vertices[vertex].y)))
                    pygame.draw.circle(self.screen,
                                       self.vertexcolour,
                                       (int(self.wireframes[frame].vertices[vertex].x),
                                        int(self.wireframes[frame].vertices[vertex].y)),
                                       self.vertexRadius, 0)
            if self.displayedges:
                for edge in self.wireframes[frame].edges:
                    pygame.draw.aaline(self.screen, self.edgecolour, (edge.start.x, edge.start.y),
                                       (edge.stop.x, edge.stop.y), 1)
        # print(total)

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


clock = pygame.time.Clock()
pygame.init()

"""
for y in range(5):
    row = []
    for x in range(5):
        aisle = []
        for z in range(5):
            [i, j, k] = [(int(n) + 1) * 100 for n in [y, x, z]]
            # if [100, 100] == [i, j]:
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
    frames.append(row)
"""

def main():
    display = ProjectionViewer()
    display.run()

main()
