import pygame
from network import Network
from player import Player
import random
from _thread import *


size = width , height = (600,600)
road_width = int(width/1.5)
roadmark_width=int(width/90)
win = pygame.display.set_mode(size)
pygame.display.set_caption("Car Game")

marker_width = 10
marker_height = 50
speed=3

left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

left_lane = 150
center_lane = 250


def redrawWindow(win,player, players,lane_marker_move_y,motorcycle,motorcycle_loc,ferrari,ferrari_loc,label_rect,label_surface):
    win.fill((11,52,163))
    print("No of players: "+ str(players[2]))
    if int(players[2]) < 3:
        loading_font = pygame.font.Font(None, 64)
        loading_surface = loading_font.render('Waiting for others to join...', True, (255,255,255))
        loading_rect = loading_surface.get_rect()
        loading_rect.center = (width/2, height/2)
        win.blit(loading_surface, loading_rect)
        pygame.display.update()
    else:
        print(players[3])
        game_time_display = "Game-time: "+str(players[3])
        game_time_font = pygame.font.Font(None, 18)
        game_time_surface = game_time_font.render(game_time_display, True, (255,255,255))
        game_time_rect = game_time_surface.get_rect()
        game_time_rect.topleft = (5, 30)
        win.blit(game_time_surface, game_time_rect)
        
        pygame.draw.rect(win,(33,33,33),(width/2 - road_width/2, 0,road_width,height))
        # pygame.draw.rect(win,(255,240,60),(width/2 - roadmark_width/2, 0, roadmark_width,height)) //That's the center line
        pygame.draw.rect(win,(255,255,255),(width/2 - road_width/2 + roadmark_width*2 -6, 0, roadmark_width,height)) #Left white line
        pygame.draw.rect(win,(255,255,255),(width/2 + road_width/2 - roadmark_width*2, 0, roadmark_width,height)) #Right white line
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(win,(255,255,255),(width/2- road_width/6 + roadmark_width*2, y+lane_marker_move_y, roadmark_width,marker_height)) #Left center line
            pygame.draw.rect(win,(255,255,255),(width/2 + road_width/6 - roadmark_width*2, y+lane_marker_move_y, roadmark_width,marker_height)) #Right center line
            pygame.draw.rect(win,(255,0,0),(width/2 - road_width/2 + roadmark_width*2 -6, y+lane_marker_move_y, roadmark_width,marker_height))
            pygame.draw.rect(win,(255,0,0),(width/2 + road_width/2 - roadmark_width*2, y+lane_marker_move_y, roadmark_width,marker_height))
        # player.draw(win)
        # players[0].draw(win)
        # players[1].draw(win)
        win.blit(label_surface,label_rect)
        player.draw_car(win)
        players[0].draw_car(win)
        players[1].draw_car(win)
        win.blit(motorcycle,motorcycle_loc)
        win.blit(ferrari,ferrari_loc)
        pygame.display.update()


# Load motorcycle and Ferrari
motorcycle = pygame.image.load("./Car images/motorcycle).png")
motorcycle_loc = motorcycle.get_rect()
motorcycle_loc.center = random.randint(width/2 - road_width/2 + roadmark_width*2 -6,width/2 + road_width/2 - roadmark_width*2 -25) , 0
ferrari = pygame.image.load("./Car images/Ferrari img.png")
ferrari_loc = ferrari.get_rect()
ferrari_loc.center = random.randint(width/2 - road_width/2 + roadmark_width*2 -6,width/2 + road_width/2 - roadmark_width*2 -25) , 0


        

def main(playerName):
    pygame.init()
    run = True
    lane_marker_move_y = 0
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()
        

    while run:
        motorcycle_loc[1] += 5
        if motorcycle_loc[1] > height:
            motorcycle_loc[1] =- 600
            motorcycle_loc.center = random.randint(width/2 - road_width/2 + roadmark_width*2 -6,width/2 + road_width/2 - roadmark_width*2 -25) , 0
        ferrari_loc[1] += 5
        if ferrari_loc[1] > height:
            ferrari_loc[1] =- 600
            ferrari_loc.center = random.randint(width/2 - road_width/2 + roadmark_width*2 -6,width/2 + road_width/2 - roadmark_width*2 -25) , 0
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        label_font = pygame.font.Font(None, 24)
        label_surface = label_font.render(playerName, True, (255,255,255))
        label_rect = label_surface.get_rect()
        label_rect.center = (p.x+15, p.y+100)
        redrawWindow(win, p, p2,lane_marker_move_y,motorcycle,motorcycle_loc,ferrari,ferrari_loc,label_rect,label_surface)
 
   
input_text = ''
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PyDrift')
background_image = pygame.image.load("3555572.jpg").convert()


def homeScreen():
    pygame.init()
    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # set up the font
    font = pygame.font.Font(None, 32)

    # set up the input field
    input_box = pygame.Rect(width/2 -50, height/2 +50, 200, 45)
    global input_text

    # set up the submit button
    submit_button = pygame.Rect(input_box.x + 10, input_box.y +70, 100, 50)

    # set up the label for the input field
    label_font = pygame.font.Font(None, 24)
    label_surface = label_font.render('Player Name', True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (input_box.x - 110, input_box.y + 15)

    # set up the label for the submit button
    submit_font = pygame.font.Font(None, 24)
    submit_surface = submit_font.render('Submit', True, WHITE,(8, 92, 209))
    submit_rect = submit_surface.get_rect()
    submit_rect.topleft = (submit_button.x +15, submit_button.y+15)        
    home_running = True
    while home_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                home_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # save the text when user hits "return"
                    input_text = input_text.strip() # remove whitespace from input_text
                    print(input_text)
                    # input_text = ''
                    home_running = False
                    main(input_text)
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    # save the text when user clicks submit button
                    input_text = input_text.strip() # remove whitespace from input_text
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
                    
        #Background
        screen.blit(background_image, (0, 0))

        # draw the input field, label, and submit button
        pygame.draw.rect(screen, WHITE, input_box)
        screen.blit(label_surface, label_rect)
        pygame.draw.rect(screen, (8, 92, 209), submit_button)
        screen.blit(submit_surface, submit_rect)

        # render the text
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
        
        #display title
        title_font = pygame.font.Font(None, 64)
        title_surface = title_font.render('PyDrift', True, BLACK)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (width / 2, 50)
        screen.blit(title_surface, title_rect)

        # update the display
        pygame.display.flip()
    


homeScreen()
# main(input_text)