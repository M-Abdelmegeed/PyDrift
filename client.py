import pygame
from network import Network
from player import Player
import random
from _thread import *


size = width, height = (600, 600)
road_width = int(width / 1.5)
roadmark_width = int(width / 90)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Car Game")

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
):
    win.fill((11, 52, 163))
    # print("No of players: "+ str(reply_object["Connections"]))
    if int(reply_object["Connections"]) < 3:
        loading_font = pygame.font.Font(None, 64)
        loading_surface = loading_font.render(
            "Waiting for others to join...", True, (255, 255, 255)
        )
        loading_rect = loading_surface.get_rect()
        loading_rect.center = (width / 2, height / 2)
        win.blit(loading_surface, loading_rect)
        pygame.display.update()
    else:
        player_rect = pygame.Rect(
            player.x, player.y, player.width - 15, player.height - 10
        )
        pygame.draw.rect(
            win, (33, 33, 33), (width / 2 - road_width / 2, 0, road_width, height)
        )
        # pygame.draw.rect(win,(255,240,60),(width/2 - roadmark_width/2, 0, roadmark_width,height)) //That's the center line
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
            crash_rect.center = (player_rect.x, player_rect.y)
            win.blit(crash, crash_rect)
            game_over_font = pygame.font.Font(None, 64)
            game_over_surface = game_over_font.render("Game Over", True, (255, 10, 10))
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.center = (width / 2, height / 2)
            win.blit(game_over_surface, game_over_rect)
            game_time_font = pygame.font.Font(None, 44)
            score_surface = game_time_font.render(
                "Score: " + str(score), True, (255, 255, 255)
            )
            score_rect = score_surface.get_rect()
            score_rect.center = (width / 2, height / 2 + 55)
            win.blit(score_surface, score_rect)
        elif reply_object["won"] == True:
            won_font = pygame.font.Font(None, 64)
            won_surface = won_font.render(
                "Congratulations, you won!", True, (15, 255, 15)
            )
            won_rect = won_surface.get_rect()
            won_rect.center = (width / 2, height / 2)
            win.blit(won_surface, won_rect)
            score_font = pygame.font.Font(None, 44)
            score_surface = score_font.render(
                "Score: " + str(score), True, (255, 255, 255)
            )
            score_rect = score_surface.get_rect()
            score_rect.center = (width / 2, height / 2 + 55)
            win.blit(score_surface, score_rect)
        else:
            # Display score
            game_time_font = pygame.font.Font(None, 18)
            score_surface = game_time_font.render(
                "Score: " + str(score), True, (255, 255, 255)
            )
            score_rect = score_surface.get_rect()
            score_rect.topleft = (5, 50)
            win.blit(score_surface, score_rect)
            # Display total game time
            print(reply_object["Game Time"])
            game_time_display = "Game-time: " + str(reply_object["Game Time"])
            game_time_font = pygame.font.Font(None, 18)
            game_time_surface = game_time_font.render(
                game_time_display, True, (255, 255, 255)
            )
            game_time_rect = game_time_surface.get_rect()
            game_time_rect.topleft = (5, 30)
            win.blit(game_time_surface, game_time_rect)
            win.blit(label_surface, label_rect)
            player.draw_car(win)
            if reply_object["Opponent 1"] != "":
                reply_object["Opponent 1"].draw_car(win)
            if reply_object["Opponent 2"] != "":
                reply_object["Opponent 2"].draw_car(win)
            win.blit(motorcycle, motorcycle_loc)
            win.blit(ferrari, ferrari_loc)
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


def main(playerName):
    pygame.init()
    run = True
    gameOver = False
    lane_marker_move_y = 0
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()
    score = 0
    speed = 3

    reply_object = n.send({"loc": p, "crashed": False})
    while run:
        player_rect = pygame.Rect(p.x - 5, p.y - 5, p.width - 15, p.height - 10)
        while reply_object["Connections"] < 3:
            reply_object = n.send({"loc": p, "crashed": False})
            print("Waiting for other players...")
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
            )
        while reply_object["won"]:
            reply_object = n.send({"loc": p, "crashed": False})
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
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        if player_rect.colliderect(motorcycle_loc):
            lane_marker_move_y = 1
            gameOver = True
            print("Game Over")
            # clock.tick(60)
            reply_object = n.send({"loc": p, "crashed": True})
            # redrawWindow(win, p, reply_object,lane_marker_move_y,motorcycle,motorcycle_loc,ferrari,ferrari_loc,label_rect,label_surface,score,gameOver)
        else:
            motorcycle_loc[1] += speed
            if motorcycle_loc[1] > height:
                score += 1
                motorcycle_loc[1] = -600
                motorcycle_loc.center = (
                    random.randint(
                        width / 2 - road_width / 2 + roadmark_width * 2 - 6,
                        width / 2 + road_width / 2 - roadmark_width * 2 - 25,
                    ),
                    0,
                )
                if score > 0 and score % 5 == 0:
                    speed += 1  # Increase game speed
            ferrari_loc[1] += speed
            if ferrari_loc[1] > height:
                ferrari_loc[1] = -600
                ferrari_loc.center = (
                    random.randint(
                        width / 2 - road_width / 2 + roadmark_width * 2 - 6,
                        width / 2 + road_width / 2 - roadmark_width * 2 - 25,
                    ),
                    0,
                )
            clock.tick(60)
            reply_object = n.send({"loc": p, "crashed": False})
            print(reply_object["won"])

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


# homeScreen()
main("Test")
