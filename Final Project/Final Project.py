# Final Project of CS1: Intro to Game Programming F20 Fall 2020
# Name: Daeshaun Morrison
# Import sys library
import sys
import time as t
# Import pygame library
import pygame
from random import randint

# Init it for use
pygame.init()
pygame.mixer.init()

# Set constants 
WIDTH=640
HEIGHT=480
CLOCK_TICK = 30
SHIPSPEED = 10
ENEMYSPEED = 5
ENEMYAMOUNT = 5
defaultFont = "NerkoOne-Regular.ttf"
BOMB_SpeedY = 25
BOMB_AMOUNT = 5
# Some basic colors
BLACK     = (0,0,0)
RED       = (255,0,0)
GREEN     = (0,255,0)
BLUE      = (0,0,255)
YELLOW    = (255,255,0)
MAGENTA   = (255,0,255)
CYAN      = (0,255,255)
WHITE     = (255,255,255)


# Set window size and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender - Daeshaun Morrison")

class Player(pygame.sprite.Sprite):
    # Initialize the sprite.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load img in folder
        self.image = pygame.image.load("spaceship.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale( self.image, (50, 50))
        self.image.set_colorkey( self.image.get_at( (1,1) ) )
        self.rect = self.image.get_rect() 
        self.rect.center = (300, 400)
        # Allows ship to move
        self.toggle = True
    
    def update(self):
        # Allow the user to move using the arrow keys.
        # pygame.key.get_pressed() returns a
        # list of booleans, one for each key.
        # More than one key can be pressed.
        keys = pygame.key.get_pressed()     
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH and self.toggle == True:            
            self.rect.centerx += SHIPSPEED         
        if keys[pygame.K_LEFT] and self.rect.left > 0 and self.toggle == True:         
            self.rect.centerx -= SHIPSPEED      
        if keys[pygame.K_UP] and self.rect.top > 0 and self.toggle == True:             
            self.rect.centery -= SHIPSPEED      
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT and self.toggle == True:
            self.rect.centery += SHIPSPEED

    def get_pos(self):
        return self.rect.center

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy-spaceship-sprite.png")
        self.image = self.image.convert()
        self.image = pygame.transform.scale( self.image, (50, 50))
        self.image.set_colorkey( self.image.get_at( (1,1) ) )
        self.rect = self.image.get_rect() 
        self.rect.center = position
        (self.speedX, self.speedY) = speed
        # Allows ship to move
        self.toggle = True
        self.timer = 30

    def update(self):
        if self.toggle:
            self.rect.center = (self.rect.centerx + self.speedX, self.rect.centery + self.speedY)
            if self.rect.left < 0:
                self.speedX = abs(self.speedX)
            if self.rect.right > WIDTH :
                self.speedX = -1 * abs(self.speedX)
            if self.rect.top < 0:
                self.speedY = abs(self.speedY)
            if self.rect.top > HEIGHT:
                self.rect.bottom = 0
        else :
            self.rect.center = (self.rect.centerx + (self.speedX - self.speedX), self.rect.centery + (self.speedY - self.speedY))

    def reset(self):
        # timer = 0
        # for i in range(900):
        #     tickCount += 1
        #     if tickCount == 900:
        #         print("yes")
        #         tickCount = 0
        #         self.kill()
        self.kill()


    def explode(self):
        self.imgMaster = pygame.image.load("Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
        self.imgMaster.convert()
        self.image = pygame.transform.scale( self.image, (50, 50))
        misImgSize = (100, 120)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (421, 2530) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (50, 70) )

    def get_pos(self):
        return self.rect.center

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Get image of the whole spritesheet
        self.imgMaster = pygame.image.load("Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
        self.imgMaster.convert()
        misImgSize = (45, 77)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (71, 1956) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (15, 35) )
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = (-100, 100)
        self.dy = 0
        # Allows it to move
        self.toggle = True
        
    def fire(self, player_pos):
            self.rect.center = player_pos  # Move Bomb to player.
            self.dy = BOMB_SpeedY              # Set its velocity.

    def update(self):
        if self.toggle:
            self.rect.centery -= self.dy
            # Remove sprite when it's off-screen to save memory
            if self.rect.bottom < 0:
                self.reset()
        else: 
            self.rect.centery -= 0

    def get_pos(self):
        return self.rect.center 

    def reset(self):
        self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imgMaster = pygame.image.load("Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
        self.imgMaster.convert()
        # self.image = pygame.transform.scale( self.image, (50, 50))
        misImgSize = (105, 111)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (416, 2530) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (15, 35) )
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = (-100, 100)

    # def update(self):
    #     self.rect.center = (-100, 100)
    def blowUp(self, position):
        self.rect.center = position
    
class Label(pygame.sprite.Sprite):
    def __init__(self, textStr, center, fontName, fontSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.text = textStr
        self.center = center
        self.font = pygame.font.Font(fontName, fontSize)
        self.textColor = textColor
    # self.update() - Render the text on the label and any changes to it.
    def update(self):
        self.image = self.font.render(self.text, 1, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

def titleScreen():
    # Construct a background
    background = pygame.Surface(screen.get_size())
    # Convert for better preformance
    background = background.convert()
    # Set background color
    background.fill( (0, 0, 0) )
    screen.blit(background, (0, 0))
    # Ask professor about this - screen.fill((0, 0, 0))

    # Construct labels for title, objective and controls. 
    # It stays until user proceeds or quits game.
    # Adding them to a group is one step needs to update any changes made to them and collision detection
    title = Label("Space Defenders!", ( (WIDTH//2), (HEIGHT//2) ), defaultFont, 25, WHITE)
    goal = Label("Fight off alien ships as long as possible to gain the highest score!", ( (WIDTH//2), ((HEIGHT//2) + 30) ), defaultFont, 23, WHITE)
    instr = Label("Move using arrow keys and use spacebar to shoot", ( (WIDTH//2), (HEIGHT//2) + 60), defaultFont, 25, WHITE)
    startGametxt = Label("Click to start!", ( (WIDTH//2), (HEIGHT//2) + 90), defaultFont, 25, WHITE)
    labelGroup = pygame.sprite.Group(title, goal, instr, startGametxt, )
    
    # Set FPS of the game
    clock = pygame.time.Clock()
    # Set a loop that keeps running until user quits or proceeds
    keepGoing = True
    while keepGoing:
        # Set FPS of the game - 30 frames per second/tick
        clock.tick(CLOCK_TICK)
        # Handle any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
        # Update the display
        labelGroup.clear(screen, background)

        labelGroup.update()

        labelGroup.draw(screen)

        pygame.display.flip()
            
def game():
    # Construct a background
    background = pygame.image.load('Space_Parallax.png')
    # Convert for better preformance
    background = background.convert()
    background = pygame.transform.scale(background, screen.get_size())
    # screen.blit(background, (0, 0))
    moveY = 0

    # Play music when game starts
    pygame.mixer.music.load("POL-galactic-trek-short.wav")
    pygame.mixer.music.play(-1) # play continuously
    # Set volume, scaled from 0 to 1
    pygame.mixer.music.set_volume(0.1)

    # Create a necessary objects
    player = Player()
    explosion = Explosion()
    explodeSound = pygame.mixer.Sound("16-bit-explosion_120bpm_C_major.wav")
    # enemyList = []
    tickCount = 0
    highScore = 0
    level = 0
    highScoreLabel = Label(f"Highscore: {highScore}", (100, 50), defaultFont, 25, WHITE)
    levelLabel = Label(f"Level: {level}", ((WIDTH - 100), 50), defaultFont, 25, WHITE)

    # Add them to groups
    playerGroup = pygame.sprite.Group(player)
    missileGroup = pygame.sprite.Group()
    # enemyGroup = pygame.sprite.Group(enemyList)
    enemyGroup = pygame.sprite.Group()
    labelGroup = pygame.sprite.Group(highScoreLabel, levelLabel, explosion)

    # - a variable that tells if the user won
    win = False
    # Pause 
    pause = False
    # - Set FPS of the game
    clock = pygame.time.Clock()
    #  - Set a loop that keeps running until user quits or proceeds
    keepGoing = True
    while keepGoing:
        # Set FPS of the game - 30 frames per second/tick
        clock.tick(CLOCK_TICK)
        # Every 30 ticks is a second
        tickCount += 1
        # Create Scrolling background
        rel_moveY = moveY % background.get_rect().height
        screen.blit(background, (0, rel_moveY - background.get_rect().height))
        if rel_moveY < HEIGHT:
            screen.blit(background, (0, rel_moveY))
        moveY += 1

        # Create New list of enemy for each level
        if len(enemyGroup) == 0:
            level += 1
            levelLabel.text = f"Level: {level}"
            for i in range(ENEMYAMOUNT):
                positionX = randint( 0, WIDTH)
                positionY = randint( -20, 0 )
                speedX = randint(-ENEMYSPEED, ENEMYSPEED)
                speedY = randint(3, ENEMYSPEED)
                eachEnemy = Enemy((positionX, positionY), (speedX, speedY))
                enemyGroup.add(eachEnemy)

        # Pause everything in the game. Game is paused if "paused = True", otherwise run.
        if pause == True:
            for eachEnemy in enemyGroup:
                eachEnemy.toggle = False
            for missile in missileGroup:
                missile.toggle = False
            player.toggle = False
        else:
            for eachEnemy in enemyGroup:
                eachEnemy.toggle = True
            for missile in missileGroup:
                missile.toggle = True
            player.toggle = True

        # Handle any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False 
            if event.type == pygame.KEYDOWN:
                # Space-bar shoots missile
                if event.key == pygame.K_SPACE and pause == False:
                    missile = Missile()
                    missileGroup.add(missile)
                    missile.fire(player.get_pos())
                # "P" pauses the game
                if event.key == pygame.K_p and pause == False:
                    pause = True
                elif event.key == pygame.K_p and pause == True:
                    pause = False
                if event.key == pygame.K_q:
                    sys.exit()  
        #### Check collisions or any other actions
        # Make a list of enemies, adding them into it when they collide with a missile
        deadEnemy = []
        for eachEnemy in enemyGroup: 
            if pygame.sprite.spritecollide(eachEnemy, missileGroup, False):
                # eachEnemy.explode()
                highScore += 25 
                highScoreLabel.text = f"Highscore: {highScore}"
                explodeSound.play()
                deadEnemy.append(eachEnemy)
        
        for missile in missileGroup:
            if pygame.sprite.spritecollide(missile, enemyGroup, False) :
                missile.reset()
                explodeSound.play()
        # Then remove enemy from group
        # If enemy was removed too soon. The the loop above wouldn't detech any collisions
        for eachEnemy in deadEnemy: 
            eachEnemy.explode()  
            eachEnemy.reset()
        
                
        if pygame.sprite.spritecollide(player, enemyGroup, True) :
            keepGoing = False
        
        if level == 10:
            keepGoing = False
            win = True

        labelGroup.clear(screen, background)
        missileGroup.clear(screen, background)

        playerGroup.update()
        enemyGroup.update()
        missileGroup.update()
        labelGroup.update()

        playerGroup.draw(screen)
        enemyGroup.draw(screen)
        labelGroup.draw(screen)
        missileGroup.draw(screen)

        pygame.display.flip()
    
    return win

def playAgain(winLose):
    # Construct a background
    background = pygame.Surface(screen.get_size())
    # Convert for better preformance
    background = background.convert()
    # Set background color
    background.fill( (0, 0, 0) )
    screen.blit(background, (0, 0))

    # Get from variable "game()" and check if it's true or false.
    # winLose = True, user won.  winLose = False, user lost.
    winOrLose = winLose

    if winOrLose == True :
        gameResult = Label("You Won!", ( (WIDTH//2), (HEIGHT//2)), defaultFont, 25, BLUE)
        playAgainTxt = Label("Play again(Y/N)", ( (WIDTH//2), (HEIGHT//2) + 30), defaultFont, 25, BLUE)
    else: 
        gameResult = Label("You Lost!", ( (WIDTH//2), (HEIGHT//2)), defaultFont, 25, RED)
        playAgainTxt= Label("Play again(Y/N)", ( (WIDTH//2), (HEIGHT//2) + 30), defaultFont, 25, RED)
    
    labelGroup = pygame.sprite.Group(gameResult, playAgainTxt)

    replay = False
    # Set FPS of the game
    clock = pygame.time.Clock()
    # Set a loop that keeps running until user quits or proceeds
    keepGoing = True
    while keepGoing:
        # Set FPS of the game - 30 frames per second/tick
        clock.tick(CLOCK_TICK)
        # Handle any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    keepGoing = False
                    replay = True
                if event.key == pygame.K_n:
                    keepGoing = False
                    replay = False


        labelGroup.clear(screen, background)

        labelGroup.update()

        labelGroup.draw(screen)

        pygame.display.flip()

    return replay

def endCredits():
    # Construct a background
    background = pygame.Surface(screen.get_size())
    # Convert for better preformance
    background = background.convert()
    # Set background color
    background.fill( (0, 0, 0) )
    screen.blit(background, (0, 0))

    endCreditsTxt1 = Label("I hope you enjoyed playing!", ( (WIDTH//2), (HEIGHT//2)), defaultFont, 25, WHITE)
    endCreditsTxt2 = Label("By Daeshaun Morrison", ( (WIDTH//2), (HEIGHT//2) + 30), defaultFont, 25, WHITE)

    labelGroup = pygame.sprite.Group(endCreditsTxt1, endCreditsTxt2)


    # Set FPS of the game
    clock = pygame.time.Clock()
    # Set a loop that runs for a set amount of secounds, 5 in this case.
    keepGoing = True
    frames = 0

    while keepGoing == True:
        clock.tick(CLOCK_TICK)

        frames = frames + 1
        if frames == 150:
            keepGoing = False

        labelGroup.clear(screen, background)

        labelGroup.update()

        labelGroup.draw(screen)

        pygame.display.flip()


def main():
    #####
    titleScreen()
    
    replay = True
    while replay == True:
      result = game()
      replay = playAgain(result)
 
    endCredits()

main()
pygame.quit()