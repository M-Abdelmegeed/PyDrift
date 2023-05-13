import pygame
import socket

pygame.init()

# set up the window
size = width, height = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Input Field")

background_image = pygame.image.load("3555572.jpg").convert()

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set up the font
font = pygame.font.Font(None, 32)

# set up the input field
input_box = pygame.Rect(width / 2 - 50, height / 2 + 50, 200, 45)
input_text = ""

# set up the submit button
submit_button = pygame.Rect(input_box.x + 10, input_box.y + 70, 100, 50)

# set up the label for the input field
label_font = pygame.font.Font(None, 24)
label_surface = label_font.render("Player Name", True, WHITE)
label_rect = label_surface.get_rect()
label_rect.topleft = (input_box.x - 110, input_box.y + 15)

# set up the label for the submit button
submit_font = pygame.font.Font(None, 24)
submit_surface = submit_font.render("Submit", True, WHITE, (8, 92, 209))
submit_rect = submit_surface.get_rect()
submit_rect.topleft = (submit_button.x + 15, submit_button.y + 15)

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # save the text when user hits "return"
                input_text = input_text.strip()  # remove whitespace from input_text
                print(input_text)
                input_text = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if submit_button.collidepoint(event.pos):
                # save the text when user clicks submit button
                input_text = input_text.strip()  # remove whitespace from input_text
                print(input_text)
                input_text = ""
                running = False
                break

                # create a new window and display the player name
                player_screen = pygame.display.set_mode((400, 300))
                player_screen.fill(WHITE)
                player_name_font = pygame.font.Font(None, 48)
                player_name_surface = player_name_font.render(input_text, True, BLACK)
                player_name_rect = player_name_surface.get_rect()
                player_name_rect.center = (200, 150)
                player_screen.blit(player_name_surface, player_name_rect)
                pygame.display.flip()

        # update the input_text variable
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalnum():
                input_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

    # clear the screen
    screen.fill(WHITE)

    # Background
    screen.blit(background_image, (0, 0))

    # draw the input field, label, and submit button
    pygame.draw.rect(screen, WHITE, input_box)
    screen.blit(label_surface, label_rect)
    pygame.draw.rect(screen, (8, 92, 209), submit_button)
    screen.blit(submit_surface, submit_rect)

    # render the text
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

    # display title
    title_font = pygame.font.Font(None, 64)
    title_surface = title_font.render("PyDrift", True, BLACK)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (width / 2, 50)
    screen.blit(title_surface, title_rect)

    # update the display
    pygame.display.flip()

# quit the game
pygame.quit()
