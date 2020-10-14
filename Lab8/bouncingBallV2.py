# bouncingBall.py
#
# Modified by:
# Date:
#
# A simple ball-in-a-box game. 

# Initialize pygame
import pygame
pygame.init()

# Constants
WIDTH  = 800
HEIGHT = 600
BOX_SIZE = 100

# Construct a screen - WIDTH x HEIGHT pixels (origin at upper-left)
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
# Set program's process name
pygame.display.set_caption("Daeshaun Morrison")

def main():

    # Construct a yellow background surface the same size as the screen.
    background = pygame.Surface(screen.get_size())  # Construct background
    background = background.convert()               # Convert graphics format.
    background.fill( (0,0,255) )                  # Fill with color. (255,255,0) is yellow.

    # Now construct a box to move on the screen.
    box = pygame.Surface( (BOX_SIZE,BOX_SIZE) )     # Construct a square surface.
    box = box.convert()                             # Convert graphics format.
    box.fill( (255,255,0) )                         # Fill with color. (Same color as background)
    box.set_colorkey((255,255,0))

    # Now construct a box for 2nd cirle to move on the screen. 
    boxSecond = pygame.Surface( (BOX_SIZE,BOX_SIZE) )     # Construct a square surface.
    boxSecond = boxSecond.convert()                       # Convert graphics format.
    boxSecond.fill( (255,255,0) )                           # Fill with color. (Same color as background)
    boxSecond.set_colorkey((255,255,0))

    # Draw a circle on the box object.
    halfBox = BOX_SIZE // 2  # Integer division, so no fractional answers
    pygame.draw.circle(box, (255,0,0), (halfBox,halfBox), halfBox, 0)
    #                   ^       ^              ^             ^     ^
    #              object     color    center of circle   radius   0="filled"
    # Draw a circle on the box object for 2nd cirle.
    halfBoxSecond = BOX_SIZE // 2  # Integer division, so no fractional answers
    pygame.draw.circle(boxSecond, (0,50,0), (halfBoxSecond,halfBoxSecond), halfBoxSecond, 0)


    # set up some box variables:
    
    # The initial location of the upper left corner of the box.
    boxLeft = 0       # The initial x-coordinate.
    boxTop  = 0       # The initial y-coordinate.
    # The initial location of the upper left corner of the 2nd box.
    # The bottom, far right of screen.
    boxLeftSecond = screen.get_width()      # The initial x-coordinate.
    boxTopSecond  = screen.get_height()       # The initial y-coordinate.


    # Move this many pixels for each clock tick.
    dx = 10
    dy = 12
    # For 2nd circle.
    dxSecond = 10
    dySecond = 12

    clock = pygame.time.Clock()  # A clock to control the frame rate.
    keepGoing = True             # Signals when the program ends.


    # GAME LOOP:
    while keepGoing:
        clock.tick(30)  # Frame rate 30 ticks (frames) per second.

        # EVENT LOOP: Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                background.fill( (0,255,0) )          # (0, 255, 0) is "green"
                box.fill( (255,255,0) )                 # Fill with color. (Same color as background)
                box.set_colorkey((255,255,0))
                pygame.draw.circle(box, (255,0,0), (halfBox,halfBox), halfBox, 0)
                # 2nd Box
                boxSecond.fill( (0,255,0) )                 # Fill with color. (Same color as background)
                boxSecond.set_colorkey((0,255,0))
                pygame.draw.circle(boxSecond, (0,50,0), (halfBoxSecond, halfBoxSecond), halfBoxSecond, 0)
                print("Ouch!")
            elif event.type == pygame.MOUSEBUTTONUP:
                background.fill( (0,0,255) )      # (0, 0, 255) is "blue"
                box.fill( (255,255,0) )             # Fill with color. (Same color as background)
                box.set_colorkey((255,255,0))
                pygame.draw.circle(box, (255,0,0), (halfBox,halfBox), halfBox, 0)
                dx = -1 * dx 
                dy = -1 * dy
                # Draw 2nd Box
                boxSecond.fill( (255,255,0) )             # Fill with color. (Same color as background)
                boxSecond.set_colorkey((255,255,0))
                pygame.draw.circle(boxSecond, (0,50,0), (halfBoxSecond,halfBoxSecond), halfBoxSecond, 0)
                dx = -1 * dx 
                dy = -1 * dy

        # Update the box's location by changing its coordinates.
        boxLeft += dx  # move the box horizontally.
        boxTop  += dy  # move the box vertically.
        
        # 2nd Box
        boxLeftSecond += dxSecond  # move the box horizontally.
        boxTopSecond  += dySecond  # move the box vertically.
    
        # If the box hits the edge of the screen, reverse its direction
        #    by changing the sign of dx or dy.
        if boxLeft > screen.get_width() - (BOX_SIZE):
            dx = -1 * abs(dx)                    # Ensure new direction is negative

        if boxLeft < 0:
            dx = abs(dx)                         # Ensure new direction is positive

        if boxTop > screen.get_height() - (BOX_SIZE):
            dy = -1 * abs(dy)                    # Ensure new direction is negative

        if boxTop < 0:
            dy = abs(dy)                         # Ensure new direction is positive

        # For 2nd Circle
        if boxLeftSecond > screen.get_width() - (BOX_SIZE):
            dxSecond = -1 * abs(dxSecond)                    # Ensure new direction is negative

        if boxLeftSecond < 0:
            dxSecond = abs(dxSecond)                         # Ensure new direction is positive

        if boxTopSecond > screen.get_height() - (BOX_SIZE):
            dySecond = -1 * abs(dySecond)                    # Ensure new direction is negative

        if boxTopSecond < 0:
            dySecond = abs(dySecond)                         # Ensure new direction is positive

        # Blit the background to the screen at position (0,0), erasing 
        #  the old position of the box
        screen.blit(background, (0,0))
        
        # Blit the box to the screen at its new (boxLeft, boxTop) coordinates.
        screen.blit(box, (boxLeft, boxTop))  
        screen.blit(boxSecond, (boxLeftSecond, boxTopSecond))
     
        # Flip the double buffered screen to make the new positions visible.
        pygame.display.flip()  
        
# Call the main() function
main()

# After main() finishes, quit pygame and clean up.  Without this,
#  pygame may never terminate, leaving you sad.
pygame.quit()
