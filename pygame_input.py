import pygame
from math import floor
# Import modules used in the program


def get_key():
    """
    Waits until the user presses a key
    :return event.key: The key that was pressed
    """
    # Loop indefinitely
    while True:
        # Listen for any events
        for event in pygame.event.get():
            # If the event was someone pressing a key
            if event.type == pygame.KEYDOWN:
                # Return that key
                return event.unicode
            # If they pressed quit
            elif event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                quit()


def display_box(window, message):
    """
    Prints a message in a box onto the screen
    :parameter window: The screen that the message is shown onto
    :parameter message: The message that is shown
    """
    fontobject = pygame.font.Font(None, 24)
    # Store the width and height of the message so it can be positioned correctly
    fontwidth = pygame.font.Font.size(fontobject, message)[0]
    fontheight = pygame.font.Font.size(fontobject, message)[1]
    # Draw a white box where the message will be
    pygame.draw.rect(window, (255, 255, 255),
                     (0,
                      (window.get_height() / 2) - (floor(4.25 * fontheight) + 5) / 2,
                      window.get_width(),
                      floor(3 * fontheight) + 5),
                     0)
    # Draw an outlining box for the message
    pygame.draw.rect(window,
                     (10, 10, 10),
                     (((window.get_width() / 2) - fontwidth / 2) - 4,
                      ((window.get_height() / 2) - fontheight) - 4,
                      fontwidth + 15,
                      fontheight + 5),
                     1)
    # If there is a message
    if len(message) != 0:
        # Display it onto the screen
        window.blit(fontobject.render(message, 1, (10, 10, 10)),
                    ((window.get_width() / 2) - fontwidth / 2,
                     (window.get_height() / 2) - fontheight))
    # 'Flips' all of the changes ,ade onto the visible screen
    pygame.display.flip()


def ask(screen, question, subtitle=None):
    """
    Takes in a question and returns the answer
    :parameter screen: The window the question is shown onto
    :parameter question: The question itself
    :keyword subtitle: A subtitle that is shown
    :return: The response from the user
    """
    pygame.font.init()
    # The current inputted string (starts empty)
    current_string = []
    # Show the question with a colon to indicate the user's current response
    display_box(screen, question + ": ")
    # If there is a subtitle
    if subtitle is not None:
        # Draw a white box behind were it will be shown to obscure any previous message
        pygame.draw.rect(screen, (255, 255, 255),
                         (30, screen.get_height() - 40, screen.get_width(), 40))
        fontobject = pygame.font.Font(None, 26)
        # Show the subtitle onto the screen
        screen.blit(fontobject.render(subtitle, 1, (0, 0, 0)),
                    ((30, screen.get_height() - 40)))
        pygame.display.flip()
    # Loop indefinitely
    while True:
        # Runs get_key and saves the key pressed into the variable 'key'
        key = get_key()
        # If backspace was pressed
        if key == '\b':
            # Remove the last item of the list
            current_string = current_string[0:-1]
        # If return was pressed
        elif key == '\r':
            # Return the current string
            return ''.join(current_string)
        # Otherwise
        else:
            # Add the key to the end of the user's response
            current_string.append(key)
        # Display the question to the user
        display_box(screen, question + ": " + ''.join(current_string))


# If the program is being run normally - not as a module - run this piece of example code
if __name__ == '__main__':
    # Create a screen
    screen = pygame.display.set_mode((320, 240))
    # Print the user's response to 'Name:'
    print(ask(screen, "Name") + " was entered")
