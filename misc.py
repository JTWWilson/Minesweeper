# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

# Updated by Jacob Wilson 22/5/16 into python 3.5 and adapted for my own purpose

import pygame


def get_key():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key
            elif event.type == pygame.QUIT:
                quit()
            else:
                pass


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    screen.fill((0, 0, 0))
    fontobject = pygame.font.Font(None, 18)
    fontwidth = pygame.font.Font.size(fontobject, message)[0]
    fontheight = pygame.font.Font.size(fontobject, message)[1]
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2 )- fontwidth / 2 - 4,
                      (screen.get_height() / 2 )- fontheight - 4,
                      fontwidth + 15,
                      fontheight + 5),
                     0)
    pygame.draw.rect(screen,
                    (255, 255, 255),
                        (((screen.get_width() / 2 )- fontwidth / 2 - 4),
                        ((screen.get_height() / 2 )- fontheight) - 4,
                        fontwidth + 15,
                        fontheight + 5),
                     1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - fontwidth / 2,
                     (screen.get_height() / 2) - fontheight))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": ")
    while 1:
        inkey = get_key()
        if inkey == 8:
            current_string = current_string[0:-1]
        elif inkey == 13:
            break
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + ''.join(current_string))
    return ''.join(current_string)


# def main():
#    screen = pygame.display.set_mode((320, 240))
#    print(ask(screen, "Name") + " was entered")


# while True:
#    main()
