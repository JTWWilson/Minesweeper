from random import randrange
import pygame
import pygame_input

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
background = pygame.image.load('Images/background.png').convert()


def createboard(x, y, mines=()):
    """
    Creates the board on which the game is based
    :param x: How wide the board must be
    :param y: How long the board must be
    :param mines: The list of all of the mines to be placed into the board
    :return: Returns the created board
    """
    board = [[{'display': '_', 'solution': 'x', 'flagged': False, 'pressed': False} if (i, j) in mines
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


def check_input(screen, question, typecheck, startrange=float('-inf'), endrange=float('inf')):
    """
    It takes in a question to ask the user, asks it, checks if it is a valid input
    (if not they must re-enter it) and returns their final answer
    :parameter screen: The screen onto which the question is shown
    :parameter question: the question that is positioned to the user
    :parameter typecheck: the data type that the user is required to enter
    :keyword startrange: the lower end of the range within which, if a float or integer is required, the user's input
    must be
    :keyword endrange: the upper end of the range within which, if a float or integer is required, the user's input must
    conform to
    :returns answer: the first value that the user has inputted that conforms to all of the requirements
    """
    # Set valid to false so that the while loop actually runs
    valid = False
    # Repeat the check_ing process until the answer is acceptable
    answer = ''
    subtitle = ''
    while not valid:
        # Try the following code, if there is an exception go to that except statement
        try:
            if typecheck == 'yesno':
                answer = {'y': True, 'yes': True, 'n': False, 'no': False}[
                    pygame_input.ask(screen, question, subtitle).lower()]
                valid = True
            else:
                # Ask the user the question then try to force the answer into the required data type
                answer = typecheck(pygame_input.ask(screen, question, subtitle))
                # Check if the user's input is within the required bounds if it is a float or integer
                if (typecheck == int or typecheck == float) and (answer < startrange or answer > endrange):
                    # Ask the user the question again, explaining what range it should be in
                    subtitle = 'Input out of required range (%s to %s)' % (startrange, endrange)
                    # print('Input out of required range (%s to %s)' % (startrange, endrange))
                # If the user's input has passed all of the hurdles
                else:
                    # Let the input through
                    valid = True
        # If a value error occurs, explain that it occurred and tell them to try again
        except ValueError:
            subtitle = 'Input is of the wrong data type, try again'
            # print('ValueError, try again')
        # If the input was not 'yes' or 'no', explain that they must input yes or no
        except KeyError:
            subtitle = 'Input is not Yes or No'
            # print('Input is not Yes or No')
            # Restart because of the exception
    return answer


def showboard(screen, board, width, height, layer='display'):
    colours = (GREY, BLUE, GREEN, RED, DARKBLUE, CRIMSON, CYAN, VIOLET, WHITE)
    if layer == 'solution':
        colours = tuple(([i + 100 if i < 155 else i - 50 if i > 50 else i for i in colour] for colour in colours))
    for row in range(height):
        for column in range(width):
            if layer == 'display' and board[row][column]['pressed'] is True:
                screen.blit(pressed, [(margin + gridwidth) * column,
                                      (margin + gridheight) * row,
                                      gridwidth,
                                      gridheight])
            elif board[row][column][layer] == 'x':
                if layer == 'solution':
                    screen.blit(mine, [(margin + gridwidth) * column,
                                       (margin + gridheight) * row,
                                       gridwidth,
                                       gridheight])
                elif layer == 'display':
                    screen.blit(tile, [(margin + gridwidth) * column,
                                       (margin + gridheight) * row,
                                       gridwidth,
                                       gridheight])
            elif board[row][column][layer] == '_' and layer == 'display':
                screen.blit(tile, [(margin + gridwidth) * column,
                                   (margin + gridheight) * row,
                                   gridwidth,
                                   gridheight])
            else:
                font = pygame.font.SysFont(FONT, TEXTSIZE, True, False)
                text = font.render(str(board[row][column][layer]), True, colours[board[row][column][layer]])
                screen.blit(text, [(margin + gridwidth) * column + margin * 2,
                                   (margin + gridheight) * row - margin * 2,
                                   gridwidth,
                                   gridheight])
            if board[row][column]['flagged'] is True:
                if layer == 'display' or (layer == 'solution' and board[row][column]['solution'] == 'x'):
                    screen.blit(flag, [(margin + gridwidth) * column,
                                       (margin + gridheight) * row,
                                       gridwidth,
                                       gridheight])
                elif layer == 'solution' and board[row][column]['solution'] != 'x':
                    screen.blit(wronglyflagged, [(margin + gridwidth) * column,
                                                 (margin + gridheight) * row,
                                                 gridwidth,
                                                 gridheight])


def menu():
    """
    The main menu for the program
    """
    # Show the main menu background
    pygame.display.set_mode((530, 560))
    screen.fill(WHITE)
    screen.blit(background,
                [screen.get_width() / 2 - background.get_width() / 2,
                 0])
    # Default options for playing the game
    x, y, mine_no = 10, 10, 10
    # Main program loop
    while True:
        # Listen for any key-presses, mouse-clicks etc. performed by the user
        for event in pygame.event.get():
            # If the user has clicked exit
            if event.type == pygame.QUIT:
                # Exit the game and the program
                pygame.quit()
                quit()
            # If the user has clicked the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Record the position of the press
                position = pygame.mouse.get_pos()
                # Test if they clicked 'Play Game'
                if 161 <= position[0] <= 378 and 109 <= position[1] <= 177:
                    # Run the main game
                    play_game(x, y, mine_no)
                    # Show the background again
                    pygame.display.set_mode((530, 560))
                    screen.fill(WHITE)
                    screen.blit(background,
                                [screen.get_width() / 2 - background.get_width() / 2,
                                 0])
                # If they pressed the 'Settings' button
                elif 161 <= position[0] <= 378 and 226 <= position[1] <= 295:
                    # Enlarge the screen
                    pygame.display.set_mode((530, 560))
                    screen.fill(WHITE)
                    # Set options to the newly-updated settings
                    x, y, mine_no = set_settings()
                    # Shown the background again
                    pygame.display.set_mode((530, 560))
                    screen.fill(WHITE)
                    screen.blit(background,
                                [screen.get_width() / 2 - background.get_width() / 2,
                                 0])
                # If they pressed the 'Quit' button
                elif 161 <= position[0] <= 378 and 347 <= position[1] <= 416:
                    # End the program
                    pygame.quit()
                    quit()
        pygame.display.flip()


def set_settings():
    """
    Change the settings
    :return: The new settings
    """
    # Ask the user for the new value of each of the settings
    x = check_input(screen, 'How wide would you like the board to be? ', int, startrange=2, endrange=40)
    y = check_input(screen, 'How long would you like the board to be? ', int, startrange=2, endrange=15)
    mine_no = check_input(
        screen, 'How many mines would you like there to be? ', int, startrange=0,
        endrange=(x * y) - 1)
    return x, y, mine_no


def play_game(boardx, boardy, mine_no):
    """
    The main function with the game loop
    """
    screen_size = [(gridwidth * boardy) + (margin * boardy + 4),
                   (gridheight * boardx) + (margin * boardx + 4)]
    screen = pygame.display.set_mode(screen_size)
    running = True
    clock = pygame.time.Clock()
    def create_unique_list(number, blacklist=set()):
        """
        Local nested generator function that creates a unique list of coordinates for the bandits/chests
        :parameter number: Length of the list that is being created
        :keyword blacklist: Coordinates that are already filled
        :yield coordinates: Yields the next coordinate pair in the list
        """

        # Repeat the set number of times
        for i in range(number):
            # Generate a random coordinate pair within the bounds of the board
            coordinates = (randrange(0, boardx), randrange(0, boardy))
            # While the coordinates are already filled
            while coordinates in blacklist:
                # Set the coordinates to a new random location
                coordinates = (randrange(0, boardx), randrange(0, boardy))
            # Pass the coordinates out of the generator
            yield coordinates
            # Add the coordinates to the list of occupied tiles
            blacklist.add(coordinates)
    row = None
    board = createboard(boardx, boardy)
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
                column = abs(pos[0] - margin) // (gridwidth + margin)
                row = abs(pos[1] - margin) // (gridheight + margin)
                bombs = 0
                for i in board:
                    for j in i:
                        if j['solution'] == 'x':
                            bombs += 1
                if bombs == 0:
                    mines = set(create_unique_list(mine_no, {(row, column)}))
                    board = createboard(boardx, boardy, mines)
                    for i in range(0, len(board)):
                        for j in range(0, len(board[i])):
                            board[i][j]['solution'] = findadjacent(board, j, i, 'x')
                if event.button == 1 and board[row][column]['flagged'] is False:
                    board[row][column]['pressed'] = True
                    pygame.draw.rect(screen, GREY,
                                     ((margin + gridwidth) * column,
                                      (margin + gridheight) * row,
                                      gridwidth + margin,
                                      gridheight + margin,
                                      ))
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP:
                """# User clicks the mouse. Get the position + Deep copy it into an integer not a variable or it will
                # change as the mouse changes, messing up which square is selected
                pos = tuple((int(i) for i in event.pos))
                # Change the x/y screen coordinates to grid coordinates
                column = abs(pos[0] - margin) // (gridwidth + margin)
                row = abs(pos[1] - margin) // (gridheight + margin)"""
                if row is not None:
                    if event.button == 1:
                        board[row][column]['pressed'] = False
                        if board[row][column]['flagged'] is False:
                            temp = choose(board, row, column)
                            if temp != 'x':
                                board = temp
                    elif event.button == 3:
                        board = flagsquare(board, row, column)
                flagged = 0
                for i in board:
                    for j in i:
                        if j['flagged'] == True and j['solution'] == 'x':
                            flagged += 1
                if temp == 'x' or flagged == mine_no:
                    screen.fill(GREY)
                    showboard(screen, board, boardy, boardx, 'solution')
                    if temp == 'x':
                        message = 'GAME OVER!'
                    elif flagged == mine_no:
                        message = 'YOU WIN!'
                    font = pygame.font.SysFont(FONT, 50, True, False)
                    text = font.render(message, True, BLACK)
                    pygame.draw.rect(screen, GREY,
                                     (screen_size[0] / 2 - pygame.font.Font.size(font, message)[0] / 2,
                                      screen_size[1] / 2 - pygame.font.Font.size(font, message)[1] / 2,
                                      pygame.font.Font.size(font, message)[0],
                                      pygame.font.Font.size(font, message)[1] - 5,
                                      ))
                    screen.blit(text, (screen_size[0] / 2 - pygame.font.Font.size(font, message)[0] / 2,
                                       screen_size[1] / 2 - pygame.font.Font.size(font, message)[1] / 2))
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == 13):
                                return
        screen.fill(GREY)
        showboard(screen, board, boardy, boardx)
        clock.tick(60)
        pygame.display.flip()


menu()
