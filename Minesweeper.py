def createboard(x, y, mines):
    board = []
    for i in range(0, x):
        column = []
        for j in range(0, y):
            print([i,j],mines[-1])
            if [i, j] in mines:
                column.append('x')
            else:
                column.append('_')
        board.append(column)
    return board


def choose(board):
    x = ''
    for i in board:
        for j in i:
            x += '_ '
        x += '\n'
    print(x)
    selection = [int(input('X axis coord '))]
    selection.append(int(input('X axis coord ')))
    count = bombsnear(selection[0], selection[1], board)
    print(count)

def bombsnear(x, y, board):
    count = 0
    xs = [x - 1, x, x + 1]
    ys = [y - 1, y, y + 1]
    for i in xs:
        for j in ys:
            if board[i][j] == 'x':
                count += 1
    return count

def main():
    board = createboard(5, 5, [[0, 0],[1, 1], [2, 2]])
    print(board)
    choose(board)

print('Jacob')
main()
