def createBoard(x, y, mines):
    board = []
    for i in range(0, x):
        column = []
        for j in range(0, y):
            print([i,j],mines[-1])
            if [i, j] in mines:
                column.append('x')
            else:
                column.append('0')
        board.append(column)
    return board

print(createBoard(5, 5, [[0, 0],[1, 1], [2, 2]]))