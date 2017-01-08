import random
import pygame
import misc

pygame.init()
screen = pygame.display.set_mode((600, 250))

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
# Set title of screen
pygame.display.set_caption("Minesweeper")
# Images
mine = pygame.image.load('Images/Mine.bmp').convert()
tile = pygame.image.load('Images/Tile.bmp').convert()
pressed = pygame.image.load('Images/Pressed.bmp').convert()
flag = pygame.image.load('Images/Flag.bmp').convert()
wronglyflagged = pygame.image.load('Images/WronglyFlagged.bmp').convert()


def createboard(x, y, mines):
    """
    Creates the board on which the game is based
    :param x: How wide the board must be
    :param y: How long the board must be
    :param mines: The list of all of the mines to be placed into the board
    :return: Returns the created board
    """
    board = [[{'display': '_', 'solution': 'x', 'flagged': False, 'pressed': False} if [i, j] in mines
              else {'display': '_', 'solution': '', 'flagged': False, 'pressed': False}
              for j in range(y)]
             for i in range(x)]
    return board


def choose(board, y, x):
    """
    Takes the given coordinates that the user has chosen and returns the board state after they have selected it
    :param board: The board that is edited
    :param y: The y coordinate of the user's selection
    :param x: The x coordinate of the user's selection
    :return: The board state after their selection or just 'x' if the user hit a bomb
    """
    count = findadjacent(board, x, y, 'x')
    # Works out how many bombs are adjacent to the square
    if board[y][x]['solution'] == 'x':
        return 'x'
    board[y][x]['display'] = count
    if count == 0:
        board = spread(board, x, y)
        # Runs the zero recursion function if they select a 0
    return board


def spread(board, x, y):
    """
    Checks each adjacent square to see if it is a zero, if it is, then the program repeats this function, recurring
    until a square is not zero
    :param board: The board that is edited
    :param y: The y coordinate of the zero
    :param x: The x coordinate of the zero
    :return: The board's new state
    """
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0 or (i == x and j == y):
                continue
            count = findadjacent(board, i, j, 'x')
            if count == 0 and board[j][i]['display'] != count:
                board[j][i]['display'] = count
                board = spread(board, i, j)
            board[j][i]['display'] = count
    return board


def findadjacent(board, x, y, char):
    """
    Counts the number of occurrences of a specific phrase in any of the squares adjacent to that given by x and y
    :param board: The board that is edited
    :param y: The y coordinate of the zero
    :param x: The x coordinate of the zero
    :param char: The character that is counted
    :return: The board's new state
    """
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    if board[y][x]['solution'] == 'x':
        return 'x'
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0 or (i == x and j == y):
                continue
            elif board[j][i]['solution'] == char:
                count += 1
    return count


def flagsquare(board, x, y):
    """
    Toggles whether a square is flagged or not
    :param board: The board that is edited
    :param y: The y coordinate of the zero
    :param x: The x coordinate of the zero
    :return: The board's new state
    """
    if board[x][y]['display'] == '_':
        if board[x][y]['flagged'] is True:
            board[x][y]['flagged'] = False
        else:
            board[x][y]['flagged'] = True
    return board


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


def showboard(screen, board, width, height, layer='display'):
    colours = (GREY, BLUE, GREEN, RED, DARKBLUE, CRIMSON, CYAN, VIOLET, WHITE)
    if layer == 'solution':
        colours = tuple(([i + 100 if i < 155 else i - 50 if i > 50 else i for i in colour] for colour in colours))
    for row in range(height):
        for column in range(width):
            if layer == 'display' and board[row][column]['pressed'] is True:
                screen.blit(pressed, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])
            elif board[row][column][layer] == 'x':
                if layer == 'solution':
                    screen.blit(mine, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])
                elif layer == 'display':
                    screen.blit(tile, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])
            elif board[row][column][layer] == '_' and layer == 'display':
                    screen.blit(tile, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])
            else:
                if board[row][column][layer] == 0: continue
                font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
                text = font.render(str(board[row][column][layer]), True, colours[board[row][column][layer]])
                screen.blit(text, [(margin + gridwidth) * row + margin * 2,
                                   (margin + gridheight) * column - margin * 2,
                                   gridwidth,
                                   gridheight])
            if board[row][column]['flagged'] == True:
                if layer == 'display' or (layer == 'solution' and board[row][column]['solution'] == 'x'):
                    screen.blit(flag, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])
                elif layer == 'solution' and board[row][column]['solution'] != 'x':
                    screen.blit(wronglyflagged, [(margin + gridwidth) * row,
                                       (margin + gridheight) * column,
                                       gridwidth,
                                       gridheight])


def main():
    """
    The main function with the game loop
    """
    running = True
    clock = pygame.time.Clock()
    colours = [GREY, BLUE, GREEN, RED, DARKBLUE, CRIMSON, CYAN, VIOLET, WHITE]
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
            board[i][j]['solution'] = findadjacent(board, j, i, 'x')
    while running:
        temp = ''
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position + Deep copy it into an integer not a variable or it will
                # change as the mouse changes, messing up which square is selected
                pos = tuple((int(i) for i in event.pos))
                # Change the x/y screen coordinates to grid coordinates
                row = abs(pos[0] - margin) // (gridwidth + margin)
                column = abs(pos[1] - margin) // (gridheight + margin)
                if event.button == 1 and board[row][column]['flagged'] is False and board[row][column]['display'] == '_':
                    board[row][column]['pressed'] = True
                    screen.blit(pressed, [(margin + gridwidth) * row,
                                          (margin + gridheight) * column,
                                          gridwidth,
                                          gridheight])
                    pygame.display.update([(margin + gridwidth) * row,
                                           (margin + gridheight) * column,
                                           gridwidth,
                                           gridheight])
                    continue
                    #pygame.draw.rect(screen, GREY,
                    #                 ((margin + gridwidth) * column,
                    #                  (margin + gridheight) * row,
                    #                  gridwidth + margin,
                    #                  gridheight + margin,
                    #                  ))
                    #pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP:
                """# User clicks the mouse. Get the position + Deep copy it into an integer not a variable or it will
                # change as the mouse changes, messing up which square is selected
                pos = tuple((int(i) for i in event.pos))
                # Change the x/y screen coordinates to grid coordinates
                column = abs(pos[0] - margin) // (gridwidth + margin)
                row = abs(pos[1] - margin) // (gridheight + margin)"""
                if event.button == 1:
                    board[row][column]['pressed'] = False
                    if board[row][column]['flagged'] == False:
                        temp = choose(board, row, column)
                        if temp != 'x':
                            board = temp
                elif event.button == 3:
                    board = flagsquare(board, row, column)
                showboard(screen, board, boardy, boardx)
                pygame.display.flip()

        screen.fill(GREY)
        flagged = 0
        for i in board:
            for j in i:
                if j['flagged'] == True and j['solution'] == 'x':
                    flagged += 1
        if temp == 'x' or flagged == mineno:
            screen.fill(GREY)
            showboard(screen, board, boardy, boardx, 'solution')
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

        clock.tick(60)

    pygame.quit()


boardx = checkinput(screen, 'How wide would you like the board to be? ', int, startrange=0, endrange=40)
boardy = checkinput(screen, 'How long would you like the board to be? ', int, startrange=0, endrange=15)
mineno = checkinput(screen, 'How many mines would you like there to be? ', int, startrange=0, endrange=(boardx * boardy))
window_size = [(gridwidth * boardx) + (margin * boardx + 4),
               (gridheight * boardy) + (margin * boardy + 4)]
screen = pygame.display.set_mode(window_size)

main()
