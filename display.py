import pygame

size = width, height = (600, 600)

# Load crash
crash = pygame.image.load("Car images/crash.png")
crash_rect = crash.get_rect()

# Load motorcycle
motorcycle = pygame.image.load("./Car images/motorcycle).png")
motorcycle_rect = motorcycle.get_rect()


def playerEliminated(opponent, win, offset, color):
    font = pygame.font.Font(None, 24)
    surface = font.render(opponent + " " + "has been eliminated", True, color)
    rect = surface.get_rect()
    rect.topright = (width, offset)
    win.blit(surface, rect)


def gameOver(win, x, y, score, player):
    crash_rect.center = (x, y)
    motorcycle_rect.center = (x, y - 25)
    player.draw_car(win)
    win.blit(crash, crash_rect)
    win.blit(motorcycle, motorcycle_rect)
    game_over_font = pygame.font.Font(None, 64)
    game_over_surface = game_over_font.render("Game Over", True, (255, 10, 10))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = (width / 2, height / 2)
    win.blit(game_over_surface, game_over_rect)
    game_time_font = pygame.font.Font(None, 44)
    score_surface = game_time_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.center = (width / 2, height / 2 + 55)
    win.blit(score_surface, score_rect)


def loadingScreen(win, missing_players):
    loading_font = pygame.font.Font(None, 58)
    if missing_players == 1:
        loading_string = "Waiting for 1 player to join..."
    else:
        loading_string = "Waiting for 2 players to join..."
    loading_surface = loading_font.render(loading_string, True, (255, 255, 255))
    loading_rect = loading_surface.get_rect()
    loading_rect.center = (width / 2, height / 2)
    win.blit(loading_surface, loading_rect)
    pygame.display.update()


def displayScore(win, score):
    game_time_font = pygame.font.Font(None, 18)
    score_surface = game_time_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.topleft = (5, 50)
    win.blit(score_surface, score_rect)


def displayGameTime(win, time):
    game_time_display = "Game-time: " + str(time)
    game_time_font = pygame.font.Font(None, 18)
    game_time_surface = game_time_font.render(game_time_display, True, (255, 255, 255))
    game_time_rect = game_time_surface.get_rect()
    game_time_rect.topleft = (5, 30)
    win.blit(game_time_surface, game_time_rect)


def displayWon(win, score):
    won_font = pygame.font.Font(None, 64)
    won_surface = won_font.render("Congratulations, you won!", True, (15, 255, 15))
    won_rect = won_surface.get_rect()
    won_rect.center = (width / 2, height / 2)
    win.blit(won_surface, won_rect)
    score_font = pygame.font.Font(None, 44)
    score_surface = score_font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.center = (width / 2, height / 2 + 55)
    win.blit(score_surface, score_rect)
