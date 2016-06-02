import random
import pygame
import misc

pygame.init()
global screen
screen = pygame.display.set_mode((600, 600))


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
mineload = pygame.image.load('Images/Mine.bmp')
tileload = pygame.image.load('Images/Tile.bmp')
flagload = pygame.image.load('Images/Flag.bmp')
wronglyflaggedload = pygame.image.load('Images/WronglyFlagged.bmp')
mine = mineload.convert()
tile = tileload.convert()
flag = flagload.convert()
wronglyflagged = wronglyflaggedload.convert()


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


def checkinput(question, typecheck, startrange=float('-inf'), endrange=float('inf')):
    """
    It takes in a question to ask the user, asks it, checks if it is a valid input
    (if not they must re-enter it) and returns their final answer
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


def showface(board, extra, width, height, depth, face, layer='display'):
    """
    Shows an entire sheet on the screen
    :param board: The board from which the sheet is referenced
    :param width: The width of the board
    :param height: The height of the board
    :param depth: The depth of the board
    :param sheet: Which sheet is being displayed
    :param layer: Which layer of the board is being accessed
    """
  # window_size = [(gridwidth * width) + (margin * width + 4),
   #                (gridheight * height) + (margin * height + 4) + extra]
    #screen = pygame.display.set_mode(window_size)
    pygame.draw.rect(screen, GREY,
                     (0,
                      0,
                      (margin + gridwidth) * width + 4,
                      (margin + gridheight) * height + 4,
                      ))
    orientations = {'front': [width, height, depth],
                    'right': [depth, width, height],
                    'back': [width, height, depth],
                    'left': [depth, height, width],
                    'top': [width, depth, height],
                    'bottom': [width, depth, height]}
   # print(orientations[face][1])
    #try:
    #print(orientations[face])
    for x in range(orientations[face][1]):
        for y in range(orientations[face][0]):
            show = 0
            if board[y][x][show][layer] == 0:
                while show + 1 < orientations[face][2] and board[y][x][show][layer] == 0:
                   #print(str(show) + 'show')
                    show += 1
                showtile(board, y, x, show, layer)
            else:
                showtile(board, y, x, 0, layer)
            font = pygame.font.SysFont(FONT, 10, True, False)
            text = font.render(str(show), True, BLACK)
            screen.blit(text, [(margin + gridwidth) * x,
                               (margin + gridheight) * y,
                               gridwidth,
                               gridheight])
    pygame.display.flip()
    #except IndexError:
     #   print('IndexError')
      #  l = [width, height, depth]
       # for i in range(len(l)):
        #    print(l[i])
         #   print(orientations[face][i])
        #print(board[x][y])
        #print(board[x][y][show])
        #quit()

def showtile(board, x, y, z, layer):
    """
    Shows one tile with the given coordinates on the screen
    :param board: The board from which the point is referenced
    :param y: The y coordinate of the point
    :param x: The x coordinate of the point
    :param z: The z coordinate of the point
    :param layer: Which layer of the board is being accessed
    """
    # ToDo: Resetting colours every time seems to be quite inefficient, look again?
    colours = (GREY, BLUE, GREEN, RED, DARKBLUE, CRIMSON, CYAN, VIOLET, WHITE)
    if layer == 'solution':
        colours = tuple(([i + 100 if i < 155 else i - 50 if i > 50 else i for i in colour] for colour in colours))
    if board[y][x][z][layer] == 'x':
        if layer == 'solution':
            screen.blit(mine, [(margin + gridwidth) * x,
                               (margin + gridheight) * y,
                               gridwidth,
                               gridheight])
        elif layer == 'display':
            screen.blit(tile, [(margin + gridwidth) * x,
                               (margin + gridheight) * y,
                               gridwidth,
                               gridheight])
    elif board[y][x][z][layer] == '_' and layer == 'display':
        screen.blit(tile, [(margin + gridwidth) * x,
                           (margin + gridheight) * y,
                           gridwidth,
                           gridheight])
    else:
        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
        text = font.render(str(board[y][x][z][layer]), True, colours[board[y][x][z][layer]])
        screen.blit(text, [(margin + gridwidth) * x + margin * 2,
                           (margin + gridheight) * y - margin * 2,
                           gridwidth,
                           gridheight])
    if board[y][x][z]['flagged'] is True:
        if layer == 'display' or (layer == 'solution' and board[y][x][z]['solution'] == 'x'):
            screen.blit(flag, [(margin + gridwidth) * x,
                               (margin + gridheight) * y,
                               gridwidth,
                               gridheight])
        elif layer == 'solution' and board[y][x][z]['solution'] != 'x':
            screen.blit(wronglyflagged, [(margin + gridwidth) * x,
                                         (margin + gridheight) * y,
                                         gridwidth,
                                         gridheight])


def main():
    """
    The main function with the game loop
    """

    boardx = checkinput('How wide would you like the board to be? ', int, startrange=0, endrange=40)
    boardy = checkinput('How long would you like the board to be? ', int, startrange=0, endrange=15)
    boardz = checkinput('How deep would you like the board to be? ', int, startrange=0, endrange=5)
    mineno = \
        checkinput('How many mines would you like there to be? ', int, startrange=0, endrange=(boardx * boardy))
    font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
    extra = pygame.font.Font.size(font, 'Front')[1]
    window_size = [(gridwidth * boardx) + (margin * boardx + 4),
                   (gridheight * boardy) + (margin * boardy + 4) + extra]
   # screen = pygame.display.set_mode(window_size)
    # Set title of screen
    pygame.display.set_caption("Minesweeper")
    screen.fill(GREY)
    running = True
    clock = pygame.time.Clock()
    mines = []
    coords = []
    faces = ['front', 'right', 'back', 'left', 'top', 'bottom']
    for i in range(mineno):
        coords = [random.randrange(0, boardx), random.randrange(0, boardy), random.randrange(0, boardz)]
        while coords in mines:
            coords = [random.randrange(0, boardx), random.randrange(0, boardy), random.randrange(0, boardz)]
        mines.append(coords)
   # print(mines)
    board = createboard(boardx, boardy, boardz, mines)
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            for k in range(0, len(board[i][j])):
                board[i][j][k]['solution'] = findadjacent(board, j, i, k, 'x')
    print(board)
    row = 0
    column = 0
    orientations = {'front': [row, column, 0],
                    'right': [0, column, row],
                    'back': [(boardx - 1) - row, column, 0],
                    'left': [0, column, (boardx - 1) - row ],
                    'top': [row, 0, (boardz - 1) - column],
                    'bottom': [row, 0, column]}
    face = 'front'
    while running:
        face = 'front'
        temp = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in range(49, 55):
                    face = faces[int(chr(event.key)) - 1]
                    print(face)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                if pos[1] < (gridheight + margin) * boardy and pos[0] < (gridwidth + margin) * boardx: #ToDo: Change depending on face
                    # Change the x/y screen coordinates to grid coordinates
                    column = abs(pos[0] - margin) // (gridwidth + margin)
                    row = abs(pos[1] - margin) // (gridheight + margin)
                    orientations = {'front': [column, row, 0],
                                    'right': [0, row, column],
                                    'back': [(boardx - 1) - column, row, 0],
                                    'left': [0, row, (boardx - 1) - column],
                                    'top': [column, 0, (boardz - 1) - row],
                                    'bottom': [column, 0, row]}
                    x = orientations[face][0]
                    y = orientations[face][1]
                    z = orientations[face][2]
                    for i in board:
                        field = ''
                        for j in i:
                            field += str(j[0]['solution'])
                        print(field)
                    print([x, y, z])
                    print(board[y][x][z])
                    if event.button == 1:
                        #board[y][x][z]['pressed'] = True
                        pygame.draw.rect(screen, GREY,
                                         ((margin + gridwidth) * column,
                                          (margin + gridheight) * row,
                                          gridwidth + margin,
                                          gridheight + margin,
                                          ))
                        pygame.display.flip()
                        # elif event.type == pygame.MOUSEBUTTONUP:
                        # if event.button == 1:
                        if board[y][x][z]['flagged'] is False:
                            temp = choose(board, y, x, z)
                            if temp != 'x':
                                board = temp
                    elif event.button == 3:
                        print('button 3')
                        board = flagsquare(board, y, x, z)
        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
        text = font.render(face, True, BLACK)
        pygame.draw.rect(screen, GREY,
                         (0, window_size[1] - extra, window_size[0],
                          window_size[1] - pygame.font.Font.size(font, face)[1],
                          #pygame.font.Font.size(font, face)[0],
                          ))
        screen.blit(text, [window_size[0] / 2 - pygame.font.Font.size(font, face)[0] / 2,
                           (gridheight + margin) * boardy])
        pygame.display.flip()
        flagged = 0
        for i in board:
            for j in i:
                for k in j:
                    if k['flagged'] == True and k['solution'] == 'x':
                        flagged += 1
        if temp == 'x' or flagged == mineno:
            screen.fill(GREY)
            showface(board, extra, boardy, boardx, boardz, face, 'solution')
            if temp == 'x':
                message = 'GAME OVER!'
            elif flagged == mineno:
                message = 'YOU WIN!'
            font = pygame.font.SysFont(FONT, 50, True, False)
            text = font.render(message, True, BLACK)
            pygame.draw.rect(screen, GREY,
                             (window_size[0] / 2 - pygame.font.Font.size(font, message)[0] / 2,
                              window_size[1] / 2 - pygame.font.Font.size(font, message)[1] / 2,
                              pygame.font.Font.size(font, message)[0],
                              pygame.font.Font.size(font, message)[1] - 5,
                              ))
            screen.blit(text, (window_size[0] / 2 - pygame.font.Font.size(font, message)[0] / 2,
                               window_size[1] / 2 - pygame.font.Font.size(font, message)[1] / 2))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == 13):
                        main()
        orientations = {'front': [column, row, 0],
                        'right': [0, row, column],
                        'back': [(boardx - 1) - column, row, 0],
                        'left': [0, row, (boardx - 1) - column],
                        'top': [column, 0, (boardz - 1) - row],
                        'bottom': [column, 0, row],
                        'frontface': [boardx, boardy, boardz],
                        'rightface': [boardz, boardx, boardy],
                        'backface': [boardx, boardy, boardz],
                        'leftface': [boardz, boardy, boardx],
                        'topface': [boardx, boardz, boardy],
                        'bottomface': [boardx, boardz, boardy]}
        #l = [boardx, boardy, boardz]
        #for i in range(len(l)):
        #    print(l[i])
        #    print(orientations[face + 'face'][i])
        showface(board, extra,
                 boardx,
                 boardy,
                 boardz, face)
        clock.tick(50)
    pygame.quit()


main()
