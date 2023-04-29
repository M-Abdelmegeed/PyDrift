import pygame
from network import Network
from player import Player


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


def redrawWindow(win,player, players,lane_marker_move_y):
    win.fill((11,52,163))
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
    player.draw_car(win)
    players[0].draw_car(win)
    players[1].draw_car(win)
    pygame.display.update()


def main():
    run = True
    lane_marker_move_y = 0
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()
    

    while run:
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
        redrawWindow(win, p, p2,lane_marker_move_y)
        

main()