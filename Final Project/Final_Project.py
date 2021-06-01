# Final Project of CS1: Intro to Game Programming F20 Fall 2020
# Name: Daeshaun Morrison
# Import sys library
import sys
import time as t
# Import pygame library
import pygame
import random
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
defaultFont = r"assets\\fonts\\NerkoOne-Regular.ttf"
BOMB_SpeedX = 7
BOMB_SpeedY = 25
BOMB_AMOUNT = 5
SPEEDBOOST = 5
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
        self.loadImage()
        
        self.frame = 0
        self.delay = 3
        self.pause = 0

        self.image = self.imgList[0]
        self.rect = self.image.get_rect()
        self.rect.center = (300, 400)
        # Allows ship to move
        self.toggle = True
        # Set a var that allows ship to shoot multi-missiles
        self.multiShot = False
        self.speedBoost = False
        # Set timer for multiShot
        self.multiShotTimer = 0
        # Set timer for speedBoost
        self.speedBoostTimer = 0

    def loadImage(self):
        self.imgList = []
        for i in range(1, 5) :
            self.image = pygame.image.load(f"assets\sprites\spaceship_blue_animation/{i}.png")
            self.image = self.image.convert()
            self.transColor = self.image.get_at((1,1))
            self.image.set_colorkey(self.transColor)
            self.image = pygame.transform.scale( self.image, (80, 80))
            self.imgList.append(self.image)   
    
    def update(self):
        # This updates the frame of each sprite to simulate animation 
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0            
            self.image = self.imgList[self.frame]
        # If the player collides with a power, set a timer that only counts up when game is unpaused.
        # When timer reaches a __ seconds, turn it off
        if self.multiShot and self.toggle == True :
            self.multiShotTimer += 1
            if self.multiShotTimer > CLOCK_TICK * 5:
                self.multiShotTimer = 0
                self.multiShot = False

        if self.speedBoost and self.toggle == True:
            self.speedBoostTimer += 1
            if self.speedBoostTimer > CLOCK_TICK * 5:
                self.speedBoostTimer = 0
                self.speedBoost = False

        # Allow the user to move using the arrow keys or awsd keys.
        # pygame.key.get_pressed() returns a
        # list of booleans, one for each key.
        # More than one key can be pressed.
        keys = pygame.key.get_pressed()     
        # Arrow keys
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d] ) and self.rect.right < WIDTH and self.toggle == True: 
            # If player collect speed boost(powerUp), increase their speed by ___
            if self.speedBoost == True :
                self.rect.centerx += (SHIPSPEED + SPEEDBOOST)
            else : 
                self.rect.centerx += SHIPSPEED         
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0 and self.toggle == True: 
            if self.speedBoost == True :
                self.rect.centerx -= (SHIPSPEED + SPEEDBOOST)        
            else :
                self.rect.centerx -= SHIPSPEED      
        if (keys[pygame.K_UP] or keys[pygame.K_w])and self.rect.top > 0 and self.toggle == True:   
            if self.speedBoost == True :
                self.rect.centery -= (SHIPSPEED + SPEEDBOOST) 
            else :  
                self.rect.centery -= SHIPSPEED      
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT and self.toggle == True:
            if self.speedBoost == True :
                self.rect.centery += (SHIPSPEED + SPEEDBOOST)
            else :    
                self.rect.centery += SHIPSPEED

    def get_pos(self):
        return self.rect.center

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Get image of the whole spritesheet
        self.imgMaster = pygame.image.load("assets\sprites\Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
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
        self.dx = 0
        self.dy = 0
        # Allows it to move
        self.toggle = True
        
    def fire(self, player_pos):
            self.rect.center = player_pos  # Move Bomb to player.
            self.dy = -BOMB_SpeedY              # Set its velocity.

    def fireRight(self, player_pos):
            self.rect.center = player_pos
            # Rotate it to make it look like it's going to the right
            self.image = pygame.transform.rotate(self.image, 345)
            self.dy = -BOMB_SpeedY 
            self.dx = BOMB_SpeedX

    def fireLeft(self, player_pos):
            self.rect.center = player_pos
            # Rotate it to make it look like it's going to the left
            self.image = pygame.transform.rotate(self.image, 15)
            self.dy = -BOMB_SpeedY 
            self.dx = -BOMB_SpeedX

    def update(self):
        if self.toggle:
            self.rect.centerx += self.dx 
            self.rect.centery += self.dy           
            # Remove sprite when it's off-screen to save memory
            if self.rect.bottom < 0:
                self.reset()
        else: 
            self.rect.centerx -= 0
            self.rect.centery -= 0

    def get_pos(self):
        return self.rect.center 

    def reset(self):
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        # Load img in folder
        self.loadImage()
        
        self.frame = 0
        self.delay = 3
        self.pause = 0

        self.image = self.imgList[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
        (self.speedX, self.speedY) = speed
        # Allows ship to move
        self.toggle = True

    def loadImage(self):
        self.imgList = []

        for i in range(1, 9) :
            self.image = pygame.image.load(f"assets\sprites\Enemy_animation\{i}.png")
            self.image = self.image.convert()
            self.transColor = self.image.get_at((1,1))
            self.image.set_colorkey(self.transColor)
            self.image = pygame.transform.scale( self.image, (80, 80))
            self.image = pygame.transform.rotate(self.image, 180)
            self.imgList.append(self.image) 

    def update(self):
        # This updates the frame of each sprite to simulate animation 
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0  
            self.image = self.imgList[self.frame]

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
        self.kill()
  
    def get_pos(self):
        return self.rect.center

class Boss(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        # Get image of the whole spritesheet
        pygame.sprite.Sprite.__init__(self)
        self.imgMaster = pygame.image.load("assets\sprites\Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png") 
        self.imgMaster.convert()
        misImgSize = (237, 230)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (216, 880) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (100, 100))
        (self.speedX, self.speedY) = speed
        # Get rect of sprite
        self.rect = self.image.get_rect()
        self.rect.center = position
        # Count hits recieved
        self.hit = 0
        # delay on shots
        self.shoot_delay = 0
        # Allows ship to move
        self.toggle = True

    def update(self):
        if self.toggle:
            # Set a shoot delay. Count to X(30 tick), then reset the timer.
            # The timer is used to tell the program to shoot a enemyMissile from
            # Boss shoots a missile every X amount of seconds.
            # CLOCK_TICK = 1 second
            self.shoot_delay += 1
            if self.shoot_delay > (CLOCK_TICK * 3):
                self.shoot_delay = 0
            # Move it each time update runs. Ex. If CLOCK_TICK = 30,
            # the update runs 30x per second(30FPS)
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
        self.kill()

    def get_pos(self):
        return self.rect.center

class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Get image of the whole spritesheet
        self.imgMaster = pygame.image.load("assets\sprites\Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
        self.imgMaster.convert()
        misImgSize = (45, 77)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (163, 1956) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (15, 35) )
        self.image = pygame.transform.rotate(self.image, 180)
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = (-100, 100)
        self.dx = 0
        self.dy = 0
        # Allows it to move
        self.toggle = True
        
    def fire(self, enemy_pos):
            # Move Bomb to an enemy
            self.rect.center = enemy_pos  
            # Set its velocity to shot it
            self.dy = 10             

    def fireRight(self, enemy_pos):
            self.rect.center = enemy_pos
            # Rotate it to make it look like it's going to the right
            self.image = pygame.transform.rotate(self.image, 15)
            self.dy = 10 
            self.dx = 5

    def fireLeft(self, enemy_pos):
            self.rect.center = enemy_pos
            # Rotate it to make it look like it's going to the left
            self.image = pygame.transform.rotate(self.image, 345)
            self.dy = 10 
            self.dx = -5

    def update(self):
        if self.toggle:
            self.rect.centerx += self.dx 
            self.rect.centery += self.dy
            # Remove sprite when it's off-screen to save memory
            if self.rect.top > HEIGHT:
                self.reset()
        else: 
            self.rect.centerx += 0
            self.rect.centery += 0

    def get_pos(self):
        return self.rect.center 

    def reset(self):
        self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.imgMaster = pygame.image.load("assets\sprites\Royalty-Free-Game-art-Spaceships-from-Unlucky-Studio.png")
        self.imgMaster.convert()
        misImgSize = (105, 111)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (416, 2530) ,(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (50, 50))
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = position
        self.delay = 0

    def update(self):
        self.delay += 1
        if self.delay == CLOCK_TICK:
            self.kill()

class MultiShotPowerUp(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        # Get image of the whole spritesheet
        self.imgMaster = pygame.image.load("assets\sprites\powerUpSpriteSheet.png")
        self.imgMaster.convert()
        misImgSize = (135, 100)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (656, 37),(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (40, 40) )
        self.image = pygame.transform.rotate(self.image, 237)
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = position
        (self.dx, self.dy) = speed
        # Allows it to move
        self.toggle = True
        # Set what type of powerUp it is
        self.powerUpType = "multiShot"

    def update(self):
        if self.toggle:
            # Move it each time update runs. Ex. If CLOCK_TICK = 30,
            # the update runs 30x per second(30FPS)
            self.rect.center = (self.rect.centerx + self.dx, self.rect.centery + self.dy)
            if self.rect.left < 0:
                self.dx = abs(self.dx)
            if self.rect.right > WIDTH :
                self.dx = -1 * abs(self.dx)
            if self.rect.top < 0:
                self.dy = abs(self.dy)
            # Remove sprite when it's off-screen to save memory
            if self.rect.top > HEIGHT:
                self.reset()
        else: 
            self.rect.centerx += 0
            self.rect.centery += 0

    def get_pos(self):
        return self.rect.center 

    def reset(self):
        self.kill()

class SpeedPowerUp(pygame.sprite.Sprite):
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        # Get image of the whole spritesheet
        self.imgMaster = pygame.image.load("assets\sprites\powerUpSpriteSheet.png")
        self.imgMaster.convert()
        misImgSize = (131, 125)
        # Create a surface to draw a section of the spritesheet
        self.image = pygame.Surface(misImgSize)
        self.image.blit(self.imgMaster, (0,0), ( (0, 37),(misImgSize)) )
        self.image.set_colorkey( self.image.get_at((1,1)))
        self.image = pygame.transform.scale( self.image, (40, 40) ) 
        # Get rect of sprite
        self.rect = self.image.get_rect()
        # Place missile off-screen at first
        self.rect.center = position
        (self.dx, self.dy) = speed
        # Allows it to move
        self.toggle = True
        # Set what type of powerUp it is
        self.powerUpType = "speedBoost"

    def update(self):
        if self.toggle:
            # Move it each time update runs. Ex. If CLOCK_TICK = 30,
            # the update runs 30x per second(30FPS)
            self.rect.center = (self.rect.centerx + self.dx, self.rect.centery + self.dy)
            if self.rect.left < 0:
                self.dx = abs(self.dx)
            if self.rect.right > WIDTH :
                self.dx = -1 * abs(self.dx)
            if self.rect.top < 0:
                self.dy = abs(self.dy)
            # Remove sprite when it's off-screen to save memory
            if self.rect.top > HEIGHT:
                self.reset()
        else: 
            self.rect.centerx += 0
            self.rect.centery += 0

    def get_pos(self):
        return self.rect.center 

    def reset(self):
        self.kill()
    
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
    background = pygame.image.load("assets\\background\Space_Parallax.png")
    # Convert for better preformance
    background = background.convert()
    background = pygame.transform.scale(background, screen.get_size())
    # screen.blit(background, (0, 0))
    moveY = 0
    # Construct labels for title, objective and controls. 
    # It stays until user proceeds or quits game.
    # Adding them to a group is one step needs to update any changes made to them and collision detection
    title = Label("Space Defenders!", ( (WIDTH//2), (HEIGHT//2) ), defaultFont, 25, WHITE)
    goal = Label("Fight off alien ships as long as possible to gain the highest score!", ( (WIDTH//2), ((HEIGHT//2) + 30) ), defaultFont, 23, WHITE)
    instr = Label("Move using arrow keys and use spacebar to shoot", ( (WIDTH//2), (HEIGHT//2) + 60), defaultFont, 25, WHITE)
    startGametxt = Label("Click to start!", ( (WIDTH//2), (HEIGHT//2) + 90), defaultFont, 25, WHITE)
    labelGroup = pygame.sprite.Group(title, goal, instr, startGametxt) 
    # Set FPS of the game
    clock = pygame.time.Clock()
    # Set a loop that keeps running until user quits or proceeds
    keepGoing = True
    while keepGoing:
        # Set FPS of the game - 30 frames per second/tick
        clock.tick(CLOCK_TICK)
        # Create Scrolling background
        rel_moveY = moveY % background.get_rect().height
        screen.blit(background, (0, rel_moveY - background.get_rect().height))
        if rel_moveY < HEIGHT:
            screen.blit(background, (0, rel_moveY))
        moveY += 1
        # Handle any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
        # Update the display
        labelGroup.update()
        # Draw the display
        labelGroup.draw(screen)
        # Put it to the screen
        pygame.display.flip()
            
def game():
    # Construct a background
    background = pygame.image.load("assets\\background\Space_Parallax.png")
    # Convert for better preformance
    background = background.convert()
    background = pygame.transform.scale(background, screen.get_size())
    # screen.blit(background, (0, 0))
    moveY = 0
    # Play music when game starts
    pygame.mixer.music.load("assets\sounds\POL-galactic-trek-short.wav")
    pygame.mixer.music.play(-1) # play continuously
    # Set volume, scaled from 0 to 1
    pygame.mixer.music.set_volume(0.1)
    # Create a necessary objects
    player = Player()
    explodeSound = pygame.mixer.Sound("assets\sounds\\16-bit-explosion_120bpm_C_major.wav")
    tickCount = 0
    highScore = 0
    level = 0
    highScoreLabel = Label(f"Highscore: {highScore}", (100, 50), defaultFont, 25, WHITE)
    levelLabel = Label(f"Level: {level}", ((WIDTH - 100), 50), defaultFont, 25, WHITE)
    pausedLabel = Label(f"", ((WIDTH//2), (HEIGHT//2)), defaultFont, 65, WHITE)
    # Add them to groups
    playerGroup = pygame.sprite.Group(player)
    missileGroup = pygame.sprite.Group()
    powerUpGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    enemyMissileGroup = pygame.sprite.Group()
    bossGroup = pygame.sprite.Group()
    allEnemyGroup = pygame.sprite.Group(enemyGroup, bossGroup)
    labelGroup = pygame.sprite.Group(highScoreLabel, levelLabel, pausedLabel)
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
        # Set a var that will be a rand interger from X to X
        powerUpChance = randint(1, 100)
        # If it "powerUpChance" is X, spawn it. This will it a X% spawn rate
        if powerUpChance == 1 and pause == False :
            positionX = randint( 0, WIDTH)
            positionY = randint( 0, 50 )
            speedX = randint(3, 5)
            speedY = randint(3, 5)
            multiShotPowerUp = MultiShotPowerUp((positionX, positionY), (speedX, speedY))
            powerUpGroup.add(multiShotPowerUp)

        if powerUpChance == 1 and pause == False :
            positionX = randint( 0, WIDTH)
            positionY = randint( 0, 50 )
            speedX = randint(3, 5)
            speedY = randint(3, 5)
            speedPowerUp = SpeedPowerUp((positionX, positionY), (speedX, speedY))
            powerUpGroup.add(speedPowerUp)

        # Create New list of enemy for each level
        if len(enemyGroup) == 0 and len(bossGroup) == 0:
            level += 1
            levelLabel.text = f"Level: {level}"
            # Every 15 lvls, spawn 2 bosses
            if level % 15 == 0:
                for i in range(2):
                    positionX = randint( 0, WIDTH)
                    positionY = randint( 20, 50 )
                    speedX = random.choice([-10, 10])
                    speedY = 0
                    boss = Boss((positionX, positionY), (speedX, speedY))
                    bossGroup.add(boss)
            elif level % 5 == 0:
                positionX = randint( 0, WIDTH)
                positionY = randint( 20, 50 )
                speedX = random.choice([-10, 10])
                speedY = 0
                boss = Boss((positionX, positionY), (speedX, speedY))
                bossGroup.add(boss)
            else :
                for i in range(ENEMYAMOUNT):
                    positionX = randint( 0, WIDTH)
                    positionY = randint( -20, 0 )
                    speedX = randint(-ENEMYSPEED, ENEMYSPEED)
                    speedY = randint(3, ENEMYSPEED)
                    eachEnemy = Enemy((positionX, positionY), (speedX, speedY))
                    enemyGroup.add(eachEnemy)
        # Pause everything in the game. Game is paused if "paused == True", otherwise run.
        # Also put "paused" text in the middle of screen when "paused == True"
        if pause == True:
            pausedLabel.text = f"Paused"
            player.toggle = False
            for eachPowerUp in powerUpGroup:
                eachPowerUp.toggle = False
            for eachEnemy in enemyGroup:
                eachEnemy.toggle = False
            for eachBoss in bossGroup:
                eachBoss.toggle = False
            for missile in missileGroup:
                missile.toggle = False
            for enemyMissile in enemyMissileGroup:
                enemyMissile.toggle = False 
        else:
            pausedLabel.text = f""
            player.toggle = True
            for eachPowerUp in powerUpGroup:
                eachPowerUp.toggle = True
            for eachEnemy in enemyGroup:
                eachEnemy.toggle = True
            for eachBoss in bossGroup:
                eachBoss.toggle = True
            for missile in missileGroup:
                missile.toggle = True
            for enemyMissile in enemyMissileGroup:
                enemyMissile.toggle = True
        # Handle any events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False 
            if event.type == pygame.KEYDOWN:
                # Space-bar shoots missile
                # If player gets power up, shoot 3 missiles!
                if event.key == pygame.K_SPACE and pause == False and player.multiShot == True:
                    # 1st missile
                    missile = Missile()
                    missileGroup.add(missile)
                    missile.fire(player.get_pos())
                    # 2nd missile
                    missile2 = Missile()
                    missileGroup.add(missile2)
                    missile2.fireRight(player.get_pos())
                    # 3rd missile
                    missile3 = Missile()
                    missileGroup.add(missile3)
                    missile3.fireLeft(player.get_pos())
                elif event.key == pygame.K_SPACE and pause == False:
                    missile = Missile()
                    missileGroup.add(missile)
                    missile.fire(player.get_pos())
                # "P" pauses the game
                if event.key == pygame.K_p and pause == False:
                    pause = True
                elif event.key == pygame.K_p and pause == True:
                    pause = False
        #### Check collisions or any other actions
        # Make a list of enemies, adding them into it when they collide with a missile
        deadEnemy = []
        resetMisList = []

        for eachEnemy in enemyGroup: 
            tickCounts = randint(1, 100)
            if tickCounts == 1 and eachEnemy.toggle == True:
                enemyMissile = EnemyMissile()
                enemyMissileGroup.add(enemyMissile)
                enemyMissile.fire(eachEnemy.get_pos())

            if pygame.sprite.spritecollide(eachEnemy, missileGroup, False):
                highScore += 25 
                highScoreLabel.text = f"Highscore: {highScore}"
                explodeSound.play()
                explosion = Explosion(eachEnemy.get_pos())
                labelGroup.add(explosion)
                deadEnemy.append(eachEnemy)

        for eachBoss in bossGroup: 
            if eachBoss.shoot_delay == 30 and eachEnemy.toggle == True:
                enemyMissile = EnemyMissile()
                enemyMissileGroup.add(enemyMissile)
                enemyMissile.fire(eachBoss.get_pos())
                # Second missile that shoots at an angle
                enemyMissile2 = EnemyMissile()
                enemyMissileGroup.add(enemyMissile2)
                enemyMissile2.fireRight(eachBoss.get_pos())
                # Third missile that shoots at an angle
                enemyMissile3 = EnemyMissile()
                enemyMissileGroup.add(enemyMissile3)
                enemyMissile3.fireLeft(eachBoss.get_pos())

            if pygame.sprite.spritecollide(eachBoss, missileGroup, False):
                eachBoss.hit += 1
                explodeSound.play()
                # If hit X amount of times... add it to add deadEnemy so it can be deleted
                if eachBoss.hit == 20:
                    highScore += 750
                    highScoreLabel.text = f"Highscore: {highScore}"
                    explodeSound.play()
                    explosion = Explosion(eachBoss.get_pos())
                    labelGroup.add(explosion)
                    deadEnemy.append(eachBoss)
        
        for missile in missileGroup:
            if pygame.sprite.spritecollide(missile, enemyGroup, False) :
                explodeSound.play()
                resetMisList.append(missile)

        for eachPowerUp in powerUpGroup: 
            if pygame.sprite.spritecollide(eachPowerUp, playerGroup, False) :
                if eachPowerUp.powerUpType == "multiShot" :
                    # Player hits a power up, allow it to shoot multiple missiles
                    # Set the multishot timer to 0 if the player gets a power up while already
                    # powered up
                    player.multiShot = True
                    player.multiShotTimer = 0
                    eachPowerUp.reset()

                elif eachPowerUp.powerUpType == "speedBoost" :
                    # Player hits this power up, get speed boost
                    # Set the multishot timer to 0 if the player gets a power up while already
                    # powered up
                    player.speedBoost = True
                    player.speedBoostTimer = 0
                    eachPowerUp.reset()
        # Then remove enemy from group
        # If enemy was removed too soon. The the loop above wouldn't detech any collisions
        for eachEnemy in deadEnemy:   
            eachEnemy.reset()
        # Then remove missile from group
        for eachMis in resetMisList:
            eachMis.reset()
        # End game if player collides with an enemy   
        if pygame.sprite.spritecollide(player, enemyGroup, True) :
            keepGoing = False
        # End game if player collides with an enemy's missile   
        if pygame.sprite.spritecollide(player, enemyMissileGroup, True) :
            keepGoing = False
        # Player wins if they get to lvl X 
        if level == 50:
            keepGoing = False
            win = True
        # Update and draw/render all the groups
        playerGroup.update()
        missileGroup.update()
        powerUpGroup.update()
        enemyGroup.update()
        enemyMissileGroup.update()
        bossGroup.update()
        allEnemyGroup.update()
        labelGroup.update()

        playerGroup.draw(screen)
        missileGroup.draw(screen)
        powerUpGroup.draw(screen)
        enemyGroup.draw(screen)
        enemyMissileGroup.draw(screen)
        bossGroup.draw(screen)
        allEnemyGroup.draw(screen)
        labelGroup.draw(screen)

        pygame.display.flip()
    
    return (win, highScore)

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
    winOrLose = winLose[0]
    highScore = winLose[1]

    if winOrLose == True :
        gameResult = Label("You Won!", ( (WIDTH//2), (HEIGHT//2)), defaultFont, 25, BLUE)
        highScoreTxt = Label(f"Highscore: {highScore}", ( (WIDTH//2), (HEIGHT//2) + 30), defaultFont, 25, BLUE)
        playAgainTxt = Label("Play again(Y/N)", ( (WIDTH//2), (HEIGHT//2) + 60), defaultFont, 25, BLUE)
    else: 
        gameResult = Label("You Lost!", ( (WIDTH//2), (HEIGHT//2)), defaultFont, 25, RED)
        highScoreTxt= Label(f"Highscore: {highScore}", ( (WIDTH//2), (HEIGHT//2) + 30), defaultFont, 25, RED)
        playAgainTxt= Label("Play again(Y/N)", ( (WIDTH//2), (HEIGHT//2) + 60), defaultFont, 25, RED)
    
    labelGroup = pygame.sprite.Group(gameResult, playAgainTxt, highScoreTxt)

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
                if event.key == pygame.K_q:
                    keepGoing = False
                    replay = False
                    sys.exit()  


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
