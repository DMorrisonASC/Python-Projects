# flySwat.py
# A game to swat flies
#
# Name: Daeshaun Morrison
# Date: 11/4/2020

import pygame
from random import randint

# Initialize all that Pygame provides
pygame.init()
pygame.mixer.init() # Enables sound effects

# Global constants:
WIDTH     = 1000
HEIGHT    = 600
FLY_COUNT = 10
DELTA     = 20
BG_COLOR  = (255,255,255)
FONT_COLOR = (0,0,0)
RANDOMIZER = 3
SCORE_POS = (WIDTH//2, 20)

## CLASS DEFINITIONS ##

class Fly(pygame.sprite.Sprite):
    # A member of the Fly class is a sprite that moves around the screen making
    #   random speed changes and bouncing off the edges of the screen.  If it
    #   collides with a swatter, the swat() method is used to change the image
    #   and freeze the location.
        
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("liveFly.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1,1)) ) 
        self.rect = self.image.get_rect()
        self.rect.center = position  # position is an (x, y) pair
        (self.dx, self.dy) = speed   # speed is a (speedX, speedY) pair
        self.alive = True

    def update(self, screen):
        # This method controls movement of the fly object

        if self.alive :     # Only move if it's a living fly
            # Change .dx and .dy to randomize speed each clock tick
            #   so that it looks like a fly buzzing around aimlessly
            self.dx += randint(-RANDOMIZER, RANDOMIZER)
            self.dy += randint(-RANDOMIZER, RANDOMIZER)
            #### Add code here: Move the object.
            self.rect.center = (self.rect.center[0] + self.dx, self.rect.center[1] + self.dy)
            #### Add code here: If the object touches any edge of the screen,
            ####  change the sign (of either dx or dy) so that the object
            ####  bounces back into the field of play.
            if self.rect.right > WIDTH :
                self.dx = -1 * abs(self.dx)

            if self.rect.left < 0 :
                self.dx = 1 * abs(self.dx)

            if self.rect.bottom > HEIGHT : 
                self.dy = -1 * abs(self.dy)

            if self.rect.top < 0 : 
                self.dy = 1 * abs(self.dy)
        
        
    def swat(self):

        #### Add code here: Change the image to be "deadFly.png"
        self.image = pygame.image.load("deadFly.png")
        self.image = self.image.convert()
        self.image.set_colorkey(self.image.get_at((1,1)) ) 
        #### Add code here: Stop the motion of the object, and
        ####  change the "self.alive" Boolean to be False.
        self.alive = False

class Swatter(pygame.sprite.Sprite):
    # A swatter is a sprite that moves around the screen following mouse 
    #   movements.  If it has a collision with a Fly object, the fly is swatted.     
  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("swatter.png")
        self.image = self.image.convert()
        self.image.set_colorkey( self.image.get_at((1, 1)) ) 
        self.rect = self.image.get_rect()
        
    def update(self, screen):
        #### Add code here to have the position of the swatter
        ####    follow the movement of the mouse.
        currentMouseX = pygame.mouse.get_pos()[0]
        currentMouseY = pygame.mouse.get_pos()[1]
        self.rect.center = (currentMouseX, currentMouseY)
        

class Label(pygame.sprite.Sprite):
    # This class puts a message on the screen
    
    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", size)
        self.text = " " # Space (" " not "") This avoids visual artifact on some HW
        self.position = position
        
    def update(self, screen):
        self.image = self.font.render(self.text, 1, FONT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        

## MAIN ##
        
def main():

    screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption("YOUR NAME HERE")
    
    # Create the background Surface object
    background = pygame.Surface(screen.get_size())
    background.fill( BG_COLOR )
    screen.blit(background, (0, 0))
    
    # Create Sound objects
    yay = pygame.mixer.Sound("yay.wav")
    slap = pygame.mixer.Sound("slap.wav")
    
    # Create a Label object (used when the game ends)
    message = Label( (screen.get_width()//2, screen.get_height()//2), 60 )
    
    # Create a scoreboard
    scoreboard = Label( SCORE_POS, 30 )
    
    # Create a Swatter object
    swatter = Swatter()
    
    # Create a list of Fly objects
    flies = []
    
    #### Add code here: Use a for loop to append FLY_COUNT flies to the list.
    ####                Each fly is given a random position and speed:
    ####    position = Pick a random position on the screen (as a pair)
    ####    speed = Pick two random speed numbers between -DELTA and DELTA (as a pair)
    for createFly in range(FLY_COUNT):
        position = (randint(0, WIDTH), randint(0, HEIGHT))
        speed = (randint(-DELTA, DELTA), randint(-DELTA, DELTA))
        eachFly = Fly(position, speed)
        flies.append(eachFly)

            
    # Create sprite groups.
    #  Every sprite must be in a group, but there can be more than one group.
    flyGroup = pygame.sprite.Group(flies)  # All the flies are initially alive
    deadGroup = pygame.sprite.Group()  # Initially empty.  As flies are swatted, they
                                       # are removed from flyGroup and added to deadGroup.
    otherSprites = pygame.sprite.Group(swatter, message, scoreboard)
    
    keepGoing = True
    win = False
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False
                    
        swatList = pygame.sprite.spritecollide(swatter, flyGroup, True)
        # In spriteCollide(), if the third parameter is "True", then each 
        #   colliding sprite is removed from the flyGroup.

        for fly in swatList :   # swatList is all the flies that are currently being swatted
            fly.swat()
            #### Add code here to play a sound and add the fly to the deadGroup
            slap.play()
            deadGroup.add(fly)

        scoreboard.text = "Flies remaining: " +  str(len(flyGroup))

        if (len(flyGroup) == 0) :
            message.text = "You Won!"
            win = True
            keepGoing = False
            
        # All sprite groups must have .clear(), .update(), and .draw() at the end
        #   of the game loop, just before the .flip().  This is true for the group
        #   of live flies, the group of dead flies, and the group of other sprites.
        flyGroup.clear(screen, background)
        deadGroup.clear(screen, background)
        otherSprites.clear(screen, background)
        
        flyGroup.update(screen)
        deadGroup.update(screen)
        otherSprites.update(screen)
        
        flyGroup.draw(screen)
        deadGroup.draw(screen)
        otherSprites.draw(screen)
    
        pygame.display.flip()
        
    # After the game loop is finished
    if win :
        yay.play()
        pygame.time.wait(int(yay.get_length() * 1000)) # pause (in milliseconds)

            
# Start the program running
main()

# Clean up
pygame.quit()
