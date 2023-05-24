import pygame
from network import Network
from player import Player
import random
from _thread import *
from display import *
from chat import GUI
import threading

size = width, height = (600, 600)
road_width = int(width / 1.5)
roadmark_width = int(width / 90)
win = pygame.display.set_mode(size)
pygame.display.set_caption("PyDrift")

marker_width = 10
marker_height = 50
speed = 3

left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

left_lane = 150
center_lane = 250


def redrawWindow(
    win,
    player,
    reply_object,
    lane_marker_move_y,
    motorcycle,
    motorcycle_loc,
    ferrari,
    ferrari_loc,
    label_rect,
    label_surface,
    score,
    game_over,
    gameID,
):
    win.fill((11, 52, 163))
    if int(reply_object[gameID]["Connections"]) < 3:
        missing_players = 3 - reply_object[gameID]["Connections"]
        loadingScreen(win, missing_players)
    else:
        player_rect = pygame.Rect(
            player.x, player.y, player.width - 15, player.height - 10
        )
        pygame.draw.rect(
            win, (33, 33, 33), (width / 2 - road_width / 2, 0, road_width, height)
        )
        pygame.draw.rect(
            win,
            (255, 255, 255),
            (
                width / 2 - road_width / 2 + roadmark_width * 2 - 6,
                0,
                roadmark_width,
                height,
            ),
        )  # Left white line
        pygame.draw.rect(
            win,
            (255, 255, 255),
            (
                width / 2 + road_width / 2 - roadmark_width * 2,
                0,
                roadmark_width,
                height,
            ),
        )  # Right white line
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(
                win,
                (255, 255, 255),
                (
                    width / 2 - road_width / 6 + roadmark_width * 2,
                    y + lane_marker_move_y,
                    roadmark_width,
                    marker_height,
                ),
            )  # Left center line
            pygame.draw.rect(
                win,
                (255, 255, 255),
                (
                    width / 2 + road_width / 6 - roadmark_width * 2,
                    y + lane_marker_move_y,
                    roadmark_width,
                    marker_height,
                ),
            )  # Right center line
            pygame.draw.rect(
                win,
                (255, 0, 0),
                (
                    width / 2 - road_width / 2 + roadmark_width * 2 - 6,
                    y + lane_marker_move_y,
                    roadmark_width,
                    marker_height,
                ),
            )
            pygame.draw.rect(
                win,
                (255, 0, 0),
                (
                    width / 2 + road_width / 2 - roadmark_width * 2,
                    y + lane_marker_move_y,
                    roadmark_width,
                    marker_height,
                ),
            )
        if game_over == True:
            gameOver(
                win, player_rect.x, player_rect.y, score, player
            )  # Display game-over screen
        elif reply_object[gameID]["won"] == True:
            displayWon(win, score)  # Display winning screen
        else:
            displayScore(win, score)  # Display score
            # displayGameTime(
            #     win, reply_object[gameID]["Game Time"]
            # )  # Display total game time
            win.blit(label_surface, label_rect)
            player.draw_car(win)
            if reply_object[gameID]["Opponent 1"] != "":
                reply_object[gameID]["Opponent 1"].draw_car(win)
            else:
                playerEliminated("Opponent 1", win, 25, (255, 10, 10))
            if reply_object[gameID]["Opponent 2"] != "":
                reply_object[gameID]["Opponent 2"].draw_car(win)
            else:
                playerEliminated("Opponent 2", win, 45, (255, 10, 10))
            win.blit(motorcycle, motorcycle_loc)
            # win.blit(ferrari, ferrari_loc)
        pygame.display.update()


# Load motorcycle and Ferrari
motorcycle = pygame.image.load("./Car images/motorcycle).png")
motorcycle_loc = motorcycle.get_rect()
motorcycle_loc.center = (
    random.randint(
        width / 2 - road_width / 2 + roadmark_width * 2 - 6,
        width / 2 + road_width / 2 - roadmark_width * 2 - 25,
    ),
    0,
)
ferrari = pygame.image.load("./Car images/Ferrari img.png")
ferrari_loc = ferrari.get_rect()
ferrari_loc.center = (
    random.randint(
        width / 2 - road_width / 2 + roadmark_width * 2 - 6,
        width / 2 + road_width / 2 - roadmark_width * 2 - 25,
    ),
    0,
)
# Load crash
crash = pygame.image.load("Car images/crash.png")
crash_rect = crash.get_rect()

rand_num = random.randint(
    width / 2 - road_width / 2 + roadmark_width * 2 - 6,
    width / 2 + road_width / 2 - roadmark_width * 2 - 25,
)


def main(playerName):
    pygame.init()
    run = True
    gameOver = False
    lane_marker_move_y = 0
    n = Network()
    p = n.getP()["player"]
    print("This is p", p)
    gameID = n.getP()["gameID"]
    print("Game id:", gameID)
    clock = pygame.time.Clock()
    score = 0
    speed = 5

    start_new_thread( goAhead, (playerName, ), )


    reply_object = n.send(
        {gameID: {"loc": p, "crashed": False, "playerName": playerName, "score": score}}
    )
    while run:
        player_rect = pygame.Rect(p.x - 5, p.y - 5, p.width - 15, p.height - 10)
        while reply_object[gameID]["Connections"] < 3:
            reply_object = n.send(
                {
                    gameID: {
                        "loc": p,
                        "crashed": False,
                        "playerName": playerName,
                        "score": score,
                    }
                }
            )
            print("Connections in game:", reply_object[gameID]["Connections"])
            label_font = pygame.font.Font(None, 24)
            label_surface = label_font.render(playerName, True, (255, 255, 255))

            redrawWindow(
                win,
                p,
                reply_object,
                lane_marker_move_y,
                motorcycle,
                motorcycle_loc,
                ferrari,
                ferrari_loc,
                pygame.Rect(0, 0, 0, 0),
                label_surface,
                score,
                gameOver,
                gameID,
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        while reply_object[gameID]["won"]:
            reply_object = n.send(
                {
                    gameID: {
                        "loc": p,
                        "crashed": False,
                        "playerName": playerName,
                        "score": score,
                    }
                }
            )
            label_font = pygame.font.Font(None, 24)
            label_surface = label_font.render(playerName, True, (255, 255, 255))
            redrawWindow(
                win,
                p,
                reply_object,
                lane_marker_move_y,
                motorcycle,
                motorcycle_loc,
                ferrari,
                ferrari_loc,
                pygame.Rect(0, 0, 0, 0),
                label_surface,
                score,
                gameOver,
                gameID,
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        if player_rect.colliderect(motorcycle_loc):
            lane_marker_move_y = 1
            gameOver = True
            print("Game Over")
            reply_object = n.send(
                {
                    gameID: {
                        "loc": p,
                        "crashed": True,
                        "playerName": playerName,
                        "score": score,
                    }
                }
            )
        else:
            motorcycle_loc[1] += speed
            if motorcycle_loc[1] > height:
                score += 1
                motorcycle_loc[1] = -600
                # center_point = (
                #     reply_object["Obstacle Center"],
                #     0,
                # )
                motorcycle_loc.center = reply_object[gameID]["Obstacle Center"]
                if score > 0 and score % 3 == 0:
                    speed += 1  # Increase game speed
            # ferrari_loc[1] += speed
            # if ferrari_loc[1] > height:
            #     ferrari_loc[1] = -600
            #     ferrari_loc.center = (
            #         random.randint(
            #             width / 2 - road_width / 2 + roadmark_width * 2 - 6,
            #             width / 2 + road_width / 2 - roadmark_width * 2 - 25,
            #         ),
            #         0,
            #     )
            clock.tick(60)
            reply_object = n.send(
                {
                    gameID: {
                        "loc": p,
                        "crashed": False,
                        "playerName": playerName,
                        "score": score,
                    }
                }
            )
            # print(reply_object[gameID]["won"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()
            lane_marker_move_y += speed * 2
            if lane_marker_move_y >= marker_height * 2:
                lane_marker_move_y = 0
            label_font = pygame.font.Font(None, 24)
            label_surface = label_font.render(playerName, True, (255, 255, 255))
            label_rect = label_surface.get_rect()
            label_rect.center = (p.x + 15, p.y + 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(
            win,
            p,
            reply_object,
            lane_marker_move_y,
            motorcycle,
            motorcycle_loc,
            ferrari,
            ferrari_loc,
            label_rect,
            label_surface,
            score,
            gameOver,
            gameID,
        )


input_text = ""
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyDrift")
background_image = pygame.image.load("3555572.jpg").convert()

def homeScreen():
    pygame.init()
    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # set up the font
    font = pygame.font.Font(None, 32)

    # set up the input field
    input_box = pygame.Rect(width / 2 - 50, height / 2 + 50, 200, 45)
    global input_text

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
    home_running = True

    # Load the music file
    pygame.mixer.music.load("Audio Files/(FIFA 14) Smallpools - Dreaming.mp3")

    # Commented out music during testing
    # Set the volume and play the music on an infinite loop
    # pygame.mixer.music.set_volume(0.7)
    # pygame.mixer.music.play(-1)
    while home_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                home_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # save the text when user hits "return"
                    input_text = input_text.strip()  # remove whitespace from input_text
                    print(input_text)
                    home_running = False
                    main(input_text)
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    # save the text when user clicks submit button
                    input_text = input_text.strip()  # remove whitespace from input_text
                    print(input_text)
                    # input_text = ''
                    home_running = False
                    main(input_text)
                    break
            # update the input_text variable
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum():
                    input_text += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

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

def goAhead(name):
    chatgui = GUI(name)


homeScreen()


#main("Test")
