"""
Nelson Su and Louis Jiazhi
ICS4U
BOMBERMAN GAME


Notes:
    CHECK Line 102
    CHECK LINE 218
    CHECK LINE 208
    CHECK LINE 228+
"""
import pygame, math, copy, random, time
import player, enemy, board, bomb, music
import os, sys
from pygame.locals import *
from bomb import Bomb
sys.path.append(os.path.split(sys.path[0])[0])

#player intialization
player = pygame.image.load('player.png')
playerPosition = [0,0] #player position [x,y]
playerNextR = [0,0] #spot right to player
playerNextL = [0,0] #spot left to player
playerNextU = [0,0] #spot up to player
playerNextD = [0,0] #spot down to player
playerNextRRU = [0,0] #spot right to player
playerNextLLD = [0,0] #spot left to player
playerNextUUR = [0,0] #spot up to player
playerNextDDL = [0,0] #spot down to player

#Music
mp = music.Music()
mp.playMusic(self.mode)

#Empty Corners
currentTile = tileMap[playerPosition[1]][playerPosition[0]]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [1,0]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [0,1]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [29,0]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [28,0]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [29,1]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [29,19]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [29,18]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [28,19]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [0,19]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [0,18]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [1,19]
tileMap[playerPosition[1]][playerPosition[0]] = GROUND
playerPosition = [0,0]

#Start Game
g = Game(self)

#Game events
class Game:

    def __init__(self):

        pygame.init()
        screen = pygame.display.set_mode((WIDTH*tileSize, HEIGHT*tileSize))
        pygame.display.set_caption('Bomber Man')
        
        #self.updateTimer()
        self.runGame()

    def initEnemies(self):
	# generates 5 enemies
	for i in range(0,5):
	    while True:
                x = random.randint(6,self.field.width-2)*40			# randint(1,X) changed to 6 so enemies do not start near player
		y = random.randint(6,self.field.height-2)*40

		if self.field.getTile((x,y)).canPass() == True:
		    break

	    e = enemy.Enemy("Enemy", "e_%d_" % (random.randint(1,self.c.MAX_ENEMY_SPRITES)), (x,y))
	    self.enemies.append(e)
	    self.blit(e.image, e.position)
	    
    def runGame(self):
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT,1000)
        pygame.time.set_timer(pygame.USEREVENT+1,500)
        cyclicCounter = 0
        self.gameIsActive = True

        while self.gameIsActive:
            clock.tick(self.c.FPS)
        
            self.checkPlayerEnemyCollision()
            self.checkWinConditions()

            #FPS is set to 30 ticks = 1 second
            cyclicCounter +=1
            if cyclicCounter == self.c.FPS:
                cyclicCounter = 0
                self.updateTimer()

            if cyclicCounter%5 == 1:
                self.clearExplosion()
        
            for event in pygame.event.get():
                print(event)

                #Quitting
                if event.type == pygame.QUIT:
                    self.forceQuit()    
                #key pressed    
                elif event.type == KEYDOWN:
                    #what resource is the player standing on? 
                    currentTile = tileMap[playerPosition[1]][playerPosition[0]]

                    #determine if right tile is GROUND or not
                    playerNextR[0] = playerPosition[0]  
                    playerNextR[0] += 1

                    playerNextRRU[1] = playerPosition[1]
                    #determine if left tile is GROUND or not
                    playerNextL[0] = playerPosition[0]  
                    playerNextL[0] -= 1

                    playerNextLLD[1] = playerPosition[1]
                    #determine if up tile is GROUND or not
                    playerNextU[1] = playerPosition[1]  
                    playerNextU[1] -= 1

                    playerNextUUR[0] = playerPosition[0]
                    #determine if down tile is GROUND or not
                    playerNextD[1] = playerPosition[1]  
                    playerNextD[1] += 1

                    playerNextDDL[0] = playerPosition[0]
                    #future tile the player MIGHT stand on right
                    futureTileRRU = tileMap[playerNextRRU[1]][playerNextR[0]]
                    if futureTileRRU == GROUND:
                        freeSpotRRU = 1
                    else:
                        freeSpotRRU = 0
                    #future tile the player MIGHT stand on in the left
                    futureTileLLD = tileMap[playerNextLLD[1]][playerNextL[0]]
                    if futureTileLLD == GROUND:
                        freeSpotLLD = 1
                    else:
                        freeSpotLLD = 0
                    #future tile the player MIGHT stand on in the up
                    futureTileUUR = tileMap[playerNextU[1]][playerNextUUR[0]]
                    if futureTileUUR == GROUND:
                        freeSpotUUR = 1
                    else:
                        freeSpotUUR = 0
                    #future tile the player MIGHT stand on in the down                
                    futureTileDDL = tileMap[playerNextD[1]][playerNextDDL[0]]
                    if futureTileDDL == GROUND:
                        freeSpotDDL = 1
                    else:
                        freeSpotDDL = 0

                    #When key is pressed       
                    if event.key == pygame.K_RIGHT and playerPosition[0] < mapWidth - 1:
                        if currentTile == GROUND and freeSpotRRU == 1:
                            playerPosition[0] += 1
                    if event.key == pygame.K_LEFT and playerPosition[0] > 0:
                        if currentTile == GROUND and freeSpotLLD == 1:
                            playerPosition[0] -= 1
                    if event.key == pygame.K_UP and playerPosition[1] > 0 :
                        if currentTile == GROUND and freeSpotUUR == 1:
                            playerPosition[1] -= 1
                    if event.key == pygame.K_DOWN and playerPosition[1] < mapHeight - 1:
                        if currentTile == GROUND and freeSpotDDL == 1:
                            playerPosition[1] += 1
                    if event.key == pygame.K_SPACE:
                        self.deployBomb(self.user)
                    elif event.key == pygame.K_ESCAPE:
                        self.fQuit()
                elif event.type == pygame.USEREVENT:
                    self.updateBombs()
                elif event.type == pygame.USEREVENT+1:
                    for e in self.enemies:
                        #self.movementHelper(e,e.nextMove())

                pygame.display.update()

    def deployBomb(self,player):
        b = player.deployBomb() #returns a bomb if available
        if b != None:
            #tile = self.field.getTile(player.position)
            tile.bomb = b
            self.bombs.append(b)

    def blit(self):
        for row in range(mapHeight):
            for column in range(mapWidth):
                self.screen.blit(textures[tileMap[row][column]], (column*tileSize,row*tileSize))

            #display player at correct position
            self.screen.blit(player,(playerPosition[0]*tileSize,playerPosition[1]*tileSize))
 
    def movementHelper(self, char, point):
	nPoint = char.position.move(point)

	tile = self.field.getTile(nPoint)

	# also check for bomb / special power ups here
			
    def updateBombs(self):
	for bomb in self.bombs:
	    if bomb.tick() == 0:
		    self.activateBomb(bomb)
	
    def activateBomb(self,bomb):
	if not bomb.triggered:
	    bomb.explode()
	    self.triggerBombChain(bomb)
	    self.bombs.remove(bomb)
	    tile = self.field.getTile(bomb.position)
	    tile.bomb = None
	    self.blit(tile.getImage(), bomb.position)
	    self.resetTiles.append(bomb.position)

	    explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
	    self.blit(explosion,bomb.position)

    def triggerBombChain(self, bomb):
	if bomb == None:
	    return
	else:
	    bomb.triggered = True	
	    self.bombHelper(bomb,'left')	
	    self.bombHelper(bomb,'right')
	    self.bombHelper(bomb,'up')
	    self.bombHelper(bomb,'down')
	
    # ALGO NEEDS RFCT!!!
    def bombHelper(self, bomb, direction):
	if direction == 'right':
	    point = [40,0]
	elif direction == 'left':
	    point = [-40,0]
	elif direction == 'up':
	    point = [0,-40]
	elif direction == 'down':
	    point = [0,40]

	x = y = 0
	while True:
	    x += point[0]
	    y += point[1]

	    nPoint = bomb.position.move((x,y))
	    t = self.field.getTile(nPoint)

	    # hit a block or indestructible object
	    if not t.canBombPass():
		# trigger new bomb explosion
		if t.bomb != None:
		    self.activateBomb(t.bomb)
		elif t.destroyable == True:
                    # if brick or powerup or player
		    t.destroy()
		    self.blit(t.getImage(),nPoint)
		    self.user.setScore(10)
		break
	    else:
		# path which explosion can travel on
		self.checkPlayerEnemyBombCollision(nPoint)

		explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
		self.blit(explosion,nPoint)
		self.resetTiles.append(nPoint)
			
	    # check bomb's power, this terminates the recursive loop
	    if int(abs(x)/40) == bomb.range or int(abs(y)/40) == bomb.range:
		break
	
    def clearExplosion(self):
	for point in self.resetTiles:
	    t = self.field.getTile(point)
	    self.blit(t.getImage(),point)
	    self.resetTiles.remove(point)

    def resetPlayerPosition(self, player, death):
	player.reset(death)
	self.blit(player.image,player.position)

    def checkPlayerEnemyBombCollision(self, position):
	# check if player was hit by bomb
	for player in self.players:
	    if player.position == position:
                if player.loseLifeAndGameOver():
		    self.gameover(player)
		else:
		    # if the player gets hit by a blast, reset it's position to the starting position
		    self.resetPlayerPosition(player,True)
		
	# check if enemy was hit by bomb
	for enemy in self.enemies:
	    if enemy.position == position:
		self.enemies.remove(enemy)
		self.user.setScore(100)

    def checkPlayerEnemyCollision(self):
	for enemy in self.enemies:
	    if enemy.position == self.user.position:
		# RFCT - code repetition
		if self.user.loseLifeAndGameOver():
		    self.gameover(self.user)
		self.user.setScore(-250)
		self.resetPlayerPosition(self.user,True)
	
    def checkWinConditions(self):
        if self.mode == self.c.SINGLE:
            if len(self.enemies) == 0:
		self.victory()

    def gameover(self, player):
	if self.mode == self.c.SINGLE:
	    print 'gameover - lost all lives | or time ran out'
	    self.highscores.addScore(player.score)
            self.gameIsActive = False
	    self.exitGame = True
	
    def fQuit(self):
	self.gameIsActive = False
	self.exitGame = True
	self.forceQuit = True

    def printText(self,text,point):
	font = pygame.font.Font("lucida.ttf",20)
	label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
	textRect = label.get_rect()
	textRect.x = point[0] 
	textRect.y = point[1]
	self.blit(label, textRect)
	
    def victory(self):
	self.gameIsActive = False
	self.user.setScore(500)
	self.level += 1
	if self.level > 6:
	    self.stage += 1
	    self.level = 1
	mp = music.Music()
	mp.playSound("victory")
	time.sleep(2)

    def updateTimer(self):
        self.timer -= 1

	# user lost
	if self.timer == 0:
	    self.gameover(self.user)

	mins = str(int(self.timer/60))
	secs = str(int(self.timer%60))

	if len(mins) == 1:
	    mins = "0"+mins
	if len(secs) == 1:
	    secs = "0"+secs
	txt = "%s:%s" % (mins,secs)
	self.printText(txt,(400,653)) 

#set icon
#pygame.display.set_icon(pygame.image.load('icon.png'))

