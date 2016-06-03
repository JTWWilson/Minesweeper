import pygame

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


def convert_to_2d(point=(0, 0, 0)):
    #  * (point[2] * .3)
    return [point[0] * (point[2] * .3) * 10, 600 - point[1] * (point[2] * .3) * 10]

print(convert_to_2d([3, 3, 3]))

board = []
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

for i in range(10):
    row = []
    for j in range(10):
        aisle = []
        for k in range(10):
            aisle.append({'value': '1',
                            '2dpos': convert_to_2d([i, j, k]),
                            'line': pygame.draw.line(screen, RED,
                                                     convert_to_2d([i, j, k]),
                                                     convert_to_2d([i, j, k + 1])),
                            'cube1': pygame.draw.line(screen, BLUE,
                                                      convert_to_2d([i, j, k]),
                                                      convert_to_2d([i, j, k + .25])),
                            'cube2': pygame.draw.line(screen, BLUE,
                                                    convert_to_2d([i + .5, j, k]),
                                                    convert_to_2d([i + .5, j, k + .25])),
                            'cube3': pygame.draw.line(screen, BLUE,
                                                    convert_to_2d([i + .5, j - .5, k]),
                                                    convert_to_2d([i + .5, j - .5, k + .25])),
                            'cube4': pygame.draw.line(screen, BLUE,
                                                    convert_to_2d([i, j, k + .25]),
                                                    convert_to_2d([i + .5, j, k + .25])),
                            'cube5': pygame.draw.line(screen, BLUE,
                                                    convert_to_2d([i + .5, j, k + .25]),
                                                    convert_to_2d([i + .5, j - .5, k + .25]))
            })
        row.append(aisle)
    board.append(row)

pygame.init()

#NEEDS FINISHING
#   _____
#  /    /|
# /____/ |
#|    | /
#|____|/
#
#   _____
#  /    /|
# /    / |
#       /
#      /



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    for i in range(len(board)):
        for j in range(len(board[i])):
            for k in range(len((board[i][j]))):
                #board[i][j][k]['line'].blit
                #font = pygame.font.SysFont(FONT, 1, True, False)
                #text = font.render(str(board[j][i][k]['value']), True, GREY)
                #screen.blit(text, [(margin + gridwidth) * i + margin * 2,
                #                   (margin + gridheight) * j - margin * 2,
                #                   gridwidth,
                #                   gridheight])
                pygame.draw.rect(screen, GREY,
                                 (board[i][j][k]['2dpos'][0],
                                  board[i][j][k]['2dpos'][1],
                                  10,
                                  10,
                                  ), 1)
    clock.tick(60)
    pygame.display.flip()