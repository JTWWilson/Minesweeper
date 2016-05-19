import random

def createboard(x, y, mines):
    board = []
    for i in range(0, y):
        row = []
        for j in range(0, x):
            if [j, i] in mines:
                row.append('x')
            else:
                row.append('_')
        board.append(row)
    return board


def choose(board, solution):
    print(board)
    print(solution)
    if board == solution:
        print('You have solved the mine-field!\nWell done!')
        main()
    field = ''
    for i in board:
        for j in i:
            if j == 'x' or j == '_':
                field += '_ '
            else:
                field += str(j) + ' '
        field += '\n'
    print(field)
    x = int(input('X axis coord '))
    y = int(input('Y axis coord '))
    count = findadjacent(x, y, 'x', board)
    if count == 'x':
        print('You hit a mine, game over!')
        for i in solution:
            print(i)
        main()
    board[y][x] = count
    if count == 0:
        board = spread(x, y, board, solution)
    return board




def spread(x, y, board, solution):
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0 or (i == x and j == y):
                continue
            count = findadjacent(i, j, 'x', board)
            if count == 0 and board[j][i] != count:
                board[j][i] = count
                board = spread(i, j, board, solution)
            board[j][i] = count
    return board


def findadjacent(x, y, char, board):
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    if board[y][x] == 'x':
        return 'x'
    for i in xs:
        for j in ys:
            if i > len(board[0]) - 1 or j > len(board) - 1 or i < 0 or j < 0:
                continue
            elif board[j][i] == char:
                count += 1
    return count


def main():
    boardsize = int(input('How big would you like the board to be? '))
    mineno = int(input('How many mines would you like there to be? '))
    board = createboard(boardsize, boardsize, [[random.randrange(0, boardsize), random.randrange(0, boardsize)] for i in range(0, mineno)])
    solution = [[findadjacent(x, y, 'x', board) for x in range(0, len(board[y]))] for y in range(0, len(board))]
    while True:
        board = choose(board, solution)


main()
