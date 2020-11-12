#################################
# snake.py
#
# Name: Daeshaun Morrison
# Date: 11/10/2020
#
# The classic arcade game "Snake"
#
#################################

import pygame
from random import randint

pygame.init()

# Constants:
WIDTH  = 900
HEIGHT = 600
CENTER = (WIDTH//2, HEIGHT//2)

INIT_TICK  = 5                      # Clock ticks per second (5 is slow)

STEP_SIZE  = 20                     # Size of a (square) snake segment
SEG_MARGIN = 3                      # Blank space in between segments
SEG_SIZE   = STEP_SIZE - SEG_MARGIN # Spacing of segments

INIT_SNAKE_LEN = 3                  # Number of segments in a baby snake
WIN_SNAKE_LEN  = 25                 # What does it take to win?

# Some basic color names
BLACK     = (0,0,0)
RED       = (255,0,0)
GREEN     = (0,255,0)
BLUE      = (0,0,255)
YELLOW    = (255,255,0)
MAGENTA   = (255,0,255)
CYAN      = (0,255,255)
WHITE     = (255,255,255)

# Background fill colors for the various screens
TITLE_BG  = (110,255,100)
REPLAY_BG = (0,0,127)
GAME_BG   = BLACK
END_BG    = CYAN
MIDSCREEN = (WIDTH // 2)

fontFile = "Roboto-Black.ttf"


screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Daeshaun Morrison")  #### Don't forget this!

#####################################################################################################
# A snake is made up of a series of Segment sprites
class Segment(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        #### Put code here to create a sprite that is a surface of size SEG_SIZE,
        #### centered at "location".  This will be one segment of a snake.
        #### Note: The variable "location" contains an (x,y) pair.
        #### The segment could be a square, or you could make it a circle or
        ####    even load an image onto it.
        self.image = pygame.Surface((SEG_SIZE, SEG_SIZE))
        self.image = self.image.convert()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = location
        

#####################################################################################################
# An Apple sprite is a target that the snake wants to eat
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("red-apple.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (SEG_SIZE, SEG_SIZE))
        self.transColor = self.image.get_at((1,1))

        self.appleSurface = pygame.Surface((SEG_SIZE, SEG_SIZE))
        self.appleSurface.blit(self.image, (0,0), ( (1,1), (920, 920) ) )

        self.image.set_colorkey( self.transColor )
        # self.appleSurface.set_colorkey( self.image.get_at((1,1)) )
        self.rect = self.image.get_rect()

        #### Put code here to create a sprite that is a filled green circle on a transparent surface
        #### of size SEG_SIZE.  (Optional: load an image on the surface instead of drawing a circle)

    # When the apple has been eaten, it needs to reappear somewhere else in the game.
    #   This code will pick a random location that does NOT collide with the snake and is NOT too close
    #     to the edge of the screen.
    #   Using STEP_SIZE ensures that segments and apples only appear at regular spacing on a grid.
    def reposition(self, segGroup):
        self.rect.centerx = randint(3, (screen.get_width()//STEP_SIZE)  - 3) * STEP_SIZE
        self.rect.centery = randint(3, (screen.get_height()//STEP_SIZE) - 3) * STEP_SIZE
        # If the apple has chosen a spot occupied by any of the snake segments, 
        #    try a different random location.  Keep trying until there is no collision.
        while( pygame.sprite.spritecollide(self, segGroup, False) ) :
            self.rect.centerx = randint(3, (screen.get_width()//STEP_SIZE)  - 3) * STEP_SIZE
            self.rect.centery = randint(3, (screen.get_height()//STEP_SIZE) - 3) * STEP_SIZE

#####################################################################################################
# Label sprites are used for the scoreboard, the title screen, etc.
#   Creating a Label sprite requires 5 parameters:
#       msg       - a string
#       center    - an (x,y) pair of the center point of the Label object
#       fontFile  - name of a .ttf font file in the current folder (or "None")
#       textSize  - height of the text, in pixels
#       textColor - an (r,g,b) triple of the color of the text
class Label(pygame.sprite.Sprite):
    def __init__(self, msg, center, fontFile, textSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.font     = pygame.font.Font(fontFile, textSize)
        self.text     = msg
        self.center   = center
        self.txtColor = textColor

    def update(self):
        self.image       = self.font.render(self.text, 1, self.txtColor)
        self.rect        = self.image.get_rect()  # get a new rect after any text change
        self.rect.center = self.center

#####################################################################################################
# TitleScreen puts up an inital welcome screen and waits for the user to click the mouse
def titleScreen():
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    background.fill( TITLE_BG )     # Fill the background
    screen.blit(background, (0,0))  # Blit background to screen
    
    # background = pygame.image.load("sand_background.png")
    # background = background.convert()
    # transColor = background.set_colorkey( background.get_at(0,0) )
    # screen.blit(background, (0,0))  # Blit background to screen
    

    #### Fill in here to construct labels for a title and game instructions.
    #### Use multiple Label sprites to do this.
    #### Add your Label sprites to labelGroup.

    gameTitle = Label("Snake!", (MIDSCREEN, ((HEIGHT // 2) - 100) ), fontFile, 15, RED)

    goalTxt = Label("As a snake, try to eat the apples without running into yourself!", 
                    (MIDSCREEN, ((HEIGHT // 2) - 80) ), fontFile, 15, RED)
    instrTxt = Label("Press UP/Down/Left/Right arrows to move snake(Ex. Up-arrow = Moves snake up)", 
                    (MIDSCREEN, ((HEIGHT // 2) - 60) ), fontFile, 15, RED)
    labelGroup = pygame.sprite.Group(gameTitle, goalTxt, instrTxt)

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:  
        clock.tick(30) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False
                                                       
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)
        
        pygame.display.flip()
                
#####################################################################################################
# The game() function performs the actual gameplay.  Returns a boolean
def game():
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill( GAME_BG )      # Fill the background
    screen.blit(background, (0,0))  # Blit background to screen

    # Create sprites and sprite groups
    scoreboard = Label("Snake Length = " + str(INIT_SNAKE_LEN),
                       (screen.get_width()//2, 50), None, 30, WHITE)

    # A snake is a group of Segment sprites, evenly spaced, 
    #    based on a grid of STEP_SIZE pixels per grid position.
    # The snake's head is the sprite at position [0] in the list,
    #    and the tail is the last sprite in the list.
    # The first segment is placed at grid position (5,5), and each 
    #    subsequent segment is placed one grid position farther to the right.
    snakeSegs = []
    for i in range(INIT_SNAKE_LEN) :
        seg = Segment( (STEP_SIZE*(5+i), (STEP_SIZE*5)) )
        snakeSegs.insert(0, seg)  # insert each new segment to the beginning of the list.
    snakeGroup   = pygame.sprite.Group(snakeSegs)

    # Once the snake has been made, create an Apple sprite, and choose a random position
    #   that does not collide with the snake
    apple = Apple()
    apple.reposition(snakeGroup)

    otherSprites = pygame.sprite.Group(scoreboard, apple)

    # Set initial snake movement
    dx = STEP_SIZE
    dy = 0

    clock = pygame.time.Clock()
    
    # Initial clock speed is pretty slow, but could be increased as game progresses (higher levels?)
    clockSpeed = INIT_TICK  
    
    keepGoing = True
    paused    = False
    win       = False

    # The game loop:
    while (keepGoing) :

        clock.tick(clockSpeed)  # Slow tick speed used (snake moves one segment per clock tick)

        # The event loop:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                keepGoing = False
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q :
                    keepGoing = False
                elif event.key == pygame.K_p :  # Pause
                    paused = not paused
                # Arrow keys dictate where the next snake segment will appear on next clock tick
                elif event.key == pygame.K_LEFT :
                    dx = -STEP_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT :
                    dx = STEP_SIZE
                    dy = 0
                elif event.key == pygame.K_UP :
                    dx = 0
                    dy = -STEP_SIZE
                elif event.key == pygame.K_DOWN :
                    dx = 0
                    dy = STEP_SIZE

        if not paused :
            # Make the snake "move" by adding a new first segment and deleting the last segment
            head = Segment( ((snakeSegs[0].rect.centerx + dx), (snakeSegs[0].rect.centery + dy)) )

            # Check to see if we have lost:
            if  (pygame.sprite.spritecollide(head, snakeGroup, True) ) :
                #  or (snakeSegs[0].rect.left < 0 ) or (snakeSegs[0].rect.right < screen.get_width()) 
                #### Put code here to detect if the new head collides with any segment in the snakeGroup,
                ####  or if the head has gone off-screen.  These all indicate the end of the game.
                win = False
                return False
            elif ((snakeSegs[0].rect.left < 0 ) or (snakeSegs[0].rect.right > WIDTH ) or (snakeSegs[0].rect.top < 0 ) or (snakeSegs[0].rect.bottom > HEIGHT ) ):
                win = False
                return False
                
            else :
                # It's not colliding, so insert the new head segment at the front of the snake (position [0]).
                snakeSegs.insert(0, head)  # snakeSegs is a Python list
                snakeGroup.add(head)       # snakeGroup is a Pygame group

            if (pygame.sprite.spritecollide(apple, snakeGroup, False)) :      # Ate an apple!
                apple.reposition(snakeGroup)                   # Move apple and let snake keep its tail
                scoreboard.text = "Snake Length = " + str(len(snakeSegs))     # Snake is one seg longer
                # You could put a sound here, too...
            else :
                tail = snakeSegs.pop()                         # Regular move; remove the tail segment
                snakeGroup.remove(tail)
                
            if len(snakeSegs) >= WIN_SNAKE_LEN :               # Did we reach the goal?
                keepGoing = False
                win = True
                
            snakeGroup.clear(screen,background)
            otherSprites.clear(screen,background)
            
            snakeGroup.update()
            otherSprites.update()
            
            snakeGroup.draw(screen)
            otherSprites.draw(screen)
            
            pygame.display.flip()
    
    return win
    
#####################################################################################################
# playAgain asks the obvious question.  Returns a boolean.
def playAgain(winLose):
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill( REPLAY_BG )    # Fill the background
    screen.blit(background, (0,0))  # Blit background to screen
    
    #### Add code here to construct Label sprites that:
    ####    Display a message about whether the player won or lost
    ####    Ask the player if they want to play again
    #### Then add your Label sprites to labelGroup
    if winLose == True : 
        replayLabel = Label("You Won! Press \"Y\" to replay or any other key to end the game", (MIDSCREEN, ((HEIGHT // 2) - 100) ), fontFile, 15, RED)
        labelGroup = pygame.sprite.Group(replayLabel)
    else: 
        replayLabel = Label("You lost! Press \"Y\" to replay or any other key to end the game", (MIDSCREEN, ((HEIGHT // 2) - 100) ), fontFile, 15, RED)
        labelGroup = pygame.sprite.Group(replayLabel)
    
    clock = pygame.time.Clock()
    keepGoing = True
    replay = False

    while keepGoing:
    
        clock.tick(30)  

        for event in pygame.event.get():
            #### Add code here to fill in the event loop:
            ####    If the user clicks the mouse or presses any key, keepGoing = False
            ####    If it happens to be the "y" key, the user wants to play again so replay = True
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    keepGoing = False
                    replay = True
                else:
                    keepGoing = False
                
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        pygame.display.flip()
        
    return replay

#####################################################################################################
# endScreen puts up a final thankyou or credits screen for a short time, and then closes.
def endScreen():
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill( END_BG )       # Fill the background
    screen.blit(background, (0,0))  # Blit background to screen

    #### Add code here:
    #### Construct Label sprites to display two messages and add them to the labelGroup:
    ####    1: a "Good bye" or "Thanks for playing" message
    ####    2: your name
    ####    (Use at least two label sprites for the two messages on this screen)
    endMessage = Label("Thanks for playing!", (MIDSCREEN, ((HEIGHT // 2) - 100) ), fontFile, 15, RED)
    endCredits = Label("by Daeshaun Morrison", (MIDSCREEN, ((HEIGHT // 2) - 80) ), fontFile, 15, RED)
    labelGroup = pygame.sprite.Group(endMessage, endCredits)
    
    clock = pygame.time.Clock()
    keepGoing = True
    frames = 0                  

    while keepGoing:
    
        clock.tick(30)          # Frame rate 30 frames per second.

        frames = frames + 1     # Count the number of frames displayed

        if frames == 60:        # After 2 seconds (= 60 frames) end the message display
            keepGoing = False 

        for event in pygame.event.get():
            # Impatient people can quit earlier by clicking the mouse or pressing any key
            if ( event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN ): 
                keepGoing = False
            
        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(screen)

        pygame.display.flip()

#####################################################################################################
# main coordinates everything
def main():
    
    titleScreen()

    replay = True

    #### Add code here:
    #### while replay is True,
    ####    play the game, then
    ####    run playAgain() to determine if the user wants to play again
    while replay : 
        result = game()
        replay = playAgain(result)
    endScreen()

# Kick it off!
main()

# Clean it up
pygame.quit()
