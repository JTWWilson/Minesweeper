import random
import pygame
import misc

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)
CYAN = (26, 184, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 16, 117)
CRIMSON = (148, 0, 0)
VIOLET = (186, 4, 138)
gridwidth = 50
gridheight = 50
margin = 3
FONT = 'Calibri'
TEXTSIZE = 70


def createboard(x, y, mines):
    board = []
    for i in range(0, y):
        row = []
        for j in range(0, x):
            if [j, i] in mines:
                row.append(['x'])
            else:
                row.append(['_'])
        board.append(row)
    return board


def choose(board, y, x):
    # print(board)
    field = ''
    for i in board:
        for j in i:
            if j[0] == 'x' or j[0] == '_':
                field += '_ '
            else:
                field += str(j[0]) + ' '
        field += '\n'
    # print(field)
    count = findadjacent(x, y, 'x', board)
    if count == 'x':
        return 'x'
    board[y][x][0] = count
    if count == 0:
        board = spread(x, y, board)
    return board


def spread(x, y, board):
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0 or (i == x and j == y):
                continue
            count = findadjacent(i, j, 'x', board)
            if count == 0 and board[j][i][0] != count:
                board[j][i][0] = count
                board = spread(i, j, board)
            board[j][i][0] = count
    return board


def findadjacent(x, y, char, board):
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    if board[y][x][0] == 'x':
        return 'x'
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0:
                continue
            elif board[j][i][0] == char:
                count += 1
    return count


def checkinput(screen, question, typecheck, startrange=float('-inf'), endrange=float('inf')):
    """
    It takes in a question to ask the user, asks it, checks if it is a valid input
    (if not they must re-enter it) and returns their final answer
    :parameter question: the question that is posed to the user
    :parameter typecheck: the data type that the user is required to enter
    :keyword startrange: the lower end of the range within which, if a float or integer is required, the user's input
    must be
    :keyword endrange: the upper end of the range within which, if a float or integer is required, the user's input must
    conform to
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


def main():
    # boardsize = int(input('How big would you like the board to be? '))
    # mineno = int(input('How many mines would you like there to be? '))
    pygame.init()
    screen = pygame.display.set_mode((600, 250))
    boardx = checkinput(screen, 'How wide would you like the board to be? ', int, startrange=0, endrange=40)
    boardy = checkinput(screen, 'How long would you like the board to be? ', int, startrange=0, endrange=15)
    mineno = checkinput(screen, 'How many mines would you like there to be? ', int, startrange=0, endrange=(boardx * boardy))
    window_size = [(gridwidth * boardx) + (margin * boardx + 4),
                   (gridheight * boardy) + (margin * boardy + 4)]
    screen = pygame.display.set_mode(window_size)
    # Set title of screen
    pygame.display.set_caption("Minesweeper")
    running = True
    clock = pygame.time.Clock()
    colours = [WHITE, BLUE, GREEN, RED, DARKBLUE, CRIMSON, CYAN, VIOLET, GREY]
    mines = []
    coords = []
    for i in range(mineno):
        coords = [random.randrange(0, boardx), random.randrange(0, boardy)]
        while coords in mines:
            coords = [random.randrange(0, boardx), random.randrange(0, boardy)]
        mines.append(coords)
    board = createboard(boardx, boardy, mines)
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            board[i][j].append(findadjacent(j, i, 'x', board))
    #for i in board:
    #    print(i)
    # solution = [[[findadjacent(x, y, 'x', board)] for x in range(0, len(board[y]))] for y in range(0, len(board))]
    while running:
        temp = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates#
                column = abs(pos[0] - margin) // (gridwidth + margin)
                row = abs(pos[1] - margin) // (gridheight + margin)
                temp = choose(board, row, column)
                if temp != 'x':
                    board = temp
        screen.fill(WHITE)
 #           board = createboard(boardx, boardy, mines)
#    solution = [[findadjacent(x, y, 'x', board) for x in range(0, len(board[y]))] for y in range(0, len(board))]
       # print([[j[0] for j in i] for i in board])
        #test = []
        #for i in board:
        #    for j in i:
        #        test.append(j[0])
        #test = [[j[0] for j in i] for i in board]
        #print(test)
        #boardcheck = []
        #for i in board:
        #    for j in i:
        #        boardcheck.append(j[0])
        #print(boardcheck)
        if temp == 'x' or [[j[0] for j in i] for i in board] == [[j[1] for j in i] for i in board]:
            mine = pygame.image.load('Images/Mine.bmp')
            mine = mine.convert()
            for row in range(0, boardy):
                for column in range(0, boardx):
                    #print(str(boardx) + '\n' + str(boardy) + 'test')
                    #print(str(row) + '\n' + str(column) + 'test')
                    #print('square : ' + '_'.join(str(board[row][column])))
                    if board[row][column][0] == 'x':
                        screen.blit(mine, [(margin + gridwidth) * column + margin * 2,
                                           (margin + gridheight) * row + margin * 3,
                                           gridwidth,
                                           gridheight])
                    else:
                        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
                        text = font.render(str(board[row][column][1]), True, tuple(
                                i + 100 if i < 155 else i - 50 if i > 50 else i for i in
                                colours[board[row][column][1]]))
                        screen.blit(text, [(margin + gridwidth) * column + gridwidth / 3,
                                           (margin + gridheight) * row,
                                           gridwidth,
                                           gridheight])
            pygame.display.flip()
            #print(board)
            if temp == 'x':
                message = 'GAME OVER!'
            elif [[j[0] for j in i] for i in board] == [[j[1] for j in i] for i in board]:
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
        for row in range(boardy):
            for column in range(boardx):
                for i in range(0, 8):
                    if board[row][column][0] == i:
                        font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
                        text = font.render(str(i), True, colours[i])
                        screen.blit(text, [(margin + gridwidth) * column + gridwidth / 3,
                                           (margin + gridheight) * row,
                                           gridwidth,
                                           gridheight])
                if board[row][column][0] == '_' or board[row][column][0] == 'x':
                    pygame.draw.rect(screen,
                                     GREY,
                                     [(margin + gridwidth) * column + margin,
                                      (margin + gridheight) * row + margin,
                                      gridwidth,
                                      gridheight])
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


main()
