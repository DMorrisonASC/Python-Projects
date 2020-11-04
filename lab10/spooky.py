# spooky.py
#
# Name: Daeshaun Morrison
# Date: 10/27/2020

# Import and initialize
import pygame
pygame.init()

from random import randint

WIDTH = 800
HEIGHT = 600

BG_COLOR = (randint(0, 255),randint(0, 255), randint(0, 255))

SPRITE_COUNT = 3  # How many sprites of each type?
MAX_SPEED = 15

# Display configuration
screen = pygame.display.set_mode( (WIDTH,HEIGHT) ) 
pygame.display.set_caption("Daeshaun Morrison")

class Pumpkin(pygame.sprite.Sprite):

    # The constructor method for a Pumpkin object.
    # Accepts four input arguments for location and motion of the object.
    def __init__(self, xPos, yPos, speedX, speedY):
        pygame.sprite.Sprite.__init__(self)         # Initialize the sprite.
        #### Add code here that will:
        ####     - Load and convert the image file
        self.image = pygame.image.load("pumpkin.png")
        self.image = self.image.convert()
        ####     - make the background pixels transparent
        self.image.set_colorkey(self.image.get_at((1, 1)))
        ####     - use get_rect() to get the object's coordinates
        self.rect = self.image.get_rect()
        ####     - set self.rect.centerx and self.rect.centery to the xPos and yPos 
        self.rect.centerx = xPos
        self.rect.centery = yPos
        ####     - set self.dx and self.dy to be the values in the speedX and speedY
        self.dx = speedX
        self.dy = speedY

    # The updater method; requires no arguments
    def update(self):
        #### Add code here that will:
        ####     - move the object based on the self.dx and self.dy values
        ####     - check to see if the object has reached the screen boundaries; if
        ####     - so, bounce it off the screen edge
        self.rect.centerx += self.dx
        self.rect.centery += self.dy 
        # Set boundaries to left and right
        if self.rect.centerx > WIDTH - self.image.get_size()[0] // 2:
            self.dx = -1 * abs(self.dx)
        if self.rect.centerx < 0 + self.image.get_size()[0] // 2:
            self.dx = abs(self.dx)
        # Set boundaries to up and bottom
        if self.rect.centery > HEIGHT - self.image.get_size()[1] // 2:
            self.dy = -1 * abs(self.dy)
        if self.rect.centery < 0 + self.image.get_size()[1] // 2 :
            self.dy = abs(self.dy)

    def reset(self) :
        self.dx = 0
        self.dy = 0
class Ghost(pygame.sprite.Sprite):

    # The constructor method for a Ghost object.
    # Accepts four input arguments for location and motion of the object.
    def __init__(self, xPos, yPos, speedX, speedY):
        pygame.sprite.Sprite.__init__(self)         # Initialize the sprite.

        #### Add code here for the Ghost class constructor.
        #### Add code here that will:
        ####     - Load and convert the image file
        self.image = pygame.image.load("ghost.png")
        self.image = self.image.convert()
        ####     - make the background pixels transparent
        self.image.set_colorkey(self.image.get_at((1, 1)))
        ####     - use get_rect() to get the object's coordinates
        self.rect = self.image.get_rect()
        ####     - set self.rect.centerx and self.rect.centery to the xPos and yPos 
        self.rect.centerx = xPos
        self.rect.centery = yPos
        ####     - set self.dx and self.dy to be the values in the speedX and speedY
        self.dx = speedX
        self.dy = speedY

    # The updater method; requires no arguments
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy 

        if self.rect.centerx - self.image.get_size()[0] // 2 > WIDTH :
            self.rect.centerx = 0 + self.image.get_size()[0] // 2

        if self.rect.centerx < 0 + self.image.get_size()[0] // 2:
            self.rect.centerx = WIDTH + self.image.get_size()[0] // 2

        # Set boundaries to up and bottom
        if self.rect.centery - self.image.get_size()[1] // 2 > HEIGHT :
            self.rect.centery = 0 + self.image.get_size()[1] // 2

        if self.rect.centery < 0 + self.image.get_size()[1] // 2:
            self.rect.centery = HEIGHT + self.image.get_size()[1] // 2



def main():

    # Create some entities:
    # First, the background Surface
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR) #### Replace black with a random RGB color here

    # Draw the background on the screen before the loop to start with a fresh view
    screen.blit(background, (0,0))

    #Next, construct some Pumpkin and Ghost objects
    
    #### Add code here that will:  (use SPRITE_COUNT)
    ####     construct a list of Pumpkin and Ghost objects, each with randomly chosen values
    ####          for xPos, yPos, speedX, and speedY (This is where you will use randint!)
    spookyList = []
    for i in range(SPRITE_COUNT) :
        # Create random pumpkin
        pumpkinSpeedX = randint(-MAX_SPEED, MAX_SPEED)
        pumpkinSpeedY = randint(-MAX_SPEED, MAX_SPEED)
        pumpkinXPos = randint(0, WIDTH)
        pumpkinYPos = randint(0, HEIGHT)
        spookyList.append(Pumpkin(pumpkinXPos, pumpkinYPos, pumpkinSpeedX, pumpkinSpeedY))
        # Create random Ghost
        ghostSpeedX = randint(-MAX_SPEED, MAX_SPEED)
        ghostSpeedY = randint(-MAX_SPEED, MAX_SPEED)
        ghostXPos = randint(0, WIDTH)
        ghostYPos = randint(0, HEIGHT)
        spookyList.append(Ghost(ghostXPos, ghostYPos, ghostSpeedX, ghostSpeedY))

    
    
    # Put the objects into a sprite group    
    allSprites = pygame.sprite.Group(spookyList) #### Fill this in with your list of objects

    # Action: Assign key variables
    clock = pygame.time.Clock()
    keepGoing = True

    # The Game Loop
    while keepGoing:

        # Set the timer to tick 30 times per second
        clock.tick(30)

        # The Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.KEYDOWN:
                holdX = 0
                holdY = 0
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False

                elif event.key == pygame.K_SPACE:
                    background.fill((randint(0, 255), randint(0, 255), randint(0, 255)))  #### Replace black with a random RGB color here 
                    screen.blit(background, (0,0))

                elif event.key == pygame.K_r:
                    for sprite in spookyList:
                        sprite.rect.centerx = WIDTH // 2
                        sprite.rect.centery = HEIGHT // 2 
                elif event.key == pygame.K_p:
                    for sprite in spookyList:
                        # spite.holdX = sprite.dx
                        # spite.holdY = sprite.dy
                        # sprite.dx = 0
                        sprite.dy = 0
            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_p:
                    for sprite in spookyList:
                        # sprite.dx = sprite.holdX
                        # sprite.dy = sprite.holdY
                        print(holdX)


        # Refresh the display                
        allSprites.clear(screen, background)  # Clear the sprites from the previous frame
        allSprites.update()                   # Call update() on each sprite to determine new positions
        allSprites.draw(screen)               # Draw all sprites on the screen at their new positions
        
        pygame.display.flip()                 # Flip the screen to make the changes visible.

# Call main() to kick things off
main()

# Clean up
pygame.quit()
