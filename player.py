import pygame

size = width , height = (600,600)
road_width = int(width/1.5)
roadmark_width=int(width/90)


#Load Lamborghini
lambo = pygame.image.load("./Car images/Lambo img updated.png")
lambo_loc = lambo.get_rect()
lambo_loc.center = width/2 - road_width/6 -50, height*0.85

#Load Mclaren
mclaren = pygame.image.load("./Car images/Mclaren img.png")
mclaren_loc = mclaren.get_rect()
mclaren_loc.center = width/2 , height*0.85
print(mclaren_loc.x)

#Load Corvette
corvette = pygame.image.load("./Car images/Corvette img.png")
corvette_loc = corvette.get_rect()
corvette_loc.center = width/2 +road_width/6 +50 , height*0.85

class Player():
    def __init__(self, x, y, width, height, color,carName):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.carName = carName

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        
    def draw_car(self,win):
        if(self.carName == "lambo"):
            win.blit(lambo,(self.x,self.y,self.width,self.height))
        elif(self.carName == "mclaren"):
            win.blit(mclaren,(self.x,self.y,self.width,self.height))
        else:
            win.blit(corvette,(self.x,self.y,self.width,self.height))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x > (width/2 - road_width/2 + roadmark_width*2 -6):
                self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if self.x < (width/2 + road_width/2 - roadmark_width*2 -25):
                self.x += self.vel

        if keys[pygame.K_UP]:
            if self.y > 0:
                self.y -= self.vel

        if keys[pygame.K_DOWN]:
            if self.y < height-45:
                self.y += self.vel

        self.update()
        

    def update(self):
        self.x=self.x
        self.y=self.y
        self.rect = (self.x, self.y, self.width, self.height)