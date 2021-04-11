import sys, pygame, config, bomb, board
import player, enemy, random, music, time, highscore
from pygame.locals import *
import os
sys.path.append(os.path.split(sys.path[0])[0])

#game class
class Game:
	firstRun = True
	exitGame = False
	resetTiles = []
	stage = 1
	level = 1
	players = []
	enemies = []
	bombs = []

	def __init__(self, mode):
		self.c = config.Config() #take a variable from config.py
		self.forceQuit = False
		self.mode = mode
		self.highscores = highscore.Highscore()

                #screen
		pygame.init()
		self.screen = pygame.display.set_mode((self.c.WIDTH,self.c.HEIGHT),pygame.DOUBLEBUF)
		pygame.display.set_caption("Bomberman")
				
		#repeat for multiple levels
		while not self.exitGame: 
			self.resetGame()
			self.initGame()

		#launch highscores
		if not self.forceQuit:
			self.highscores.reloadScoreData()
			self.highscores.displayScore()
			
	def resetGame(self):
		self.field = None
		self.enemies = []
		self.bombs = []
		self.resetTiles = []

		#clearing background
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.blit(bg,(0,0))

	def initGame(self):
		if self.mode == self.c.START:
			self.printText("Level %d-%d" % (self.stage,self.level),(40,15))
			self.field = board.Board(self.stage, self.level)
			self.timer = 3*60+1

		self.drawBoard()
		self.drawInterface()
		self.updateTimer()

		#player doesn't have to be reinitialized after the first time
		if self.firstRun:
			self.firstRun = False
			self.initPlayers()
		else:
			self.resetPlayerPosition(self.user,False)
		
		if self.mode == self.c.START:
			self.initEnemies()
		
		#music player
		mp = music.Music()
		mp.playMusic(self.mode)

		self.runGame()

	#draws the board onto the screen
	def drawBoard(self):
		for row in range(1,len(self.field.board)-1):
			for col in range(1,len(self.field.board[row])-1):
				image = self.field.board[row][col].image
				# RFCT - fix the mess
				position = self.field.board[row][col].image.get_rect().move((col*self.c.TILE_SIZE,row*self.c.TILE_SIZE))
				self.blit(image, position)

	def updateDisplayInfo(self):
		self.printText(self.user.score,(600,15))
		self.printText(self.user.lives,(770,653))
		self.printText(self.user.power,(630,653))

	def drawInterface(self):
		life = pygame.image.load(self.c.IMAGE_PATH + "life.png").convert()
		power = pygame.image.load(self.c.IMAGE_PATH + "power.png").convert()

                self.blit(life,(720,652))
		self.blit(power,(580,650))
	
	def initPlayers(self):
		if self.mode == self.c.START:
			self.user = player.Player("Player 1","p_1_",0,(40,40))
			self.players.append(self.user)
			self.blit(self.user.image, self.user.position)

	def initEnemies(self):
		#generates 5 enemies
		for i in range(0,5):
			while True:
				x = random.randint(6,self.field.width-2)*40	# randint(1,X) changed to 6 so enemies do not start near player
				y = random.randint(6,self.field.height-2)*40

				if self.field.getTile((x,y)).canPass() == True:
					break

			e = enemy.Enemy("Enemy", "e_%d_" % (random.randint(1,self.c.MAX_ENEMY_SPRITES)), (x,y))
			self.enemies.append(e)
			self.blit(e.image, e.position)

        #game core
	def runGame(self):
		clock = pygame.time.Clock()
		pygame.time.set_timer(pygame.USEREVENT,1000)
		pygame.time.set_timer(pygame.USEREVENT+1,500)
		cyclicCounter = 0
		self.gameActive = True

		while self.gameActive:
			clock.tick(self.c.FPS)
			
			self.checkPlayerEnemyCollision()
			self.checkWinConditions()

			#FPS is set to 30, 30 ticks = 1 second
			cyclicCounter += 1
			if cyclicCounter == self.c.FPS:
				cyclicCounter = 0
				self.updateTimer()

			if cyclicCounter%5 == 1:
				self.clearExplosion()
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.KEYDOWN:
					# deploy bomb
					k = event.key

					if k == pygame.K_SPACE:
						self.deployBomb(self.user)
					elif k == pygame.K_ESCAPE:
						self.fQuit()
					elif k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT:
						point = self.user.movement(k) #next point
						self.movementHelper(self.user, point)
					elif k == pygame.K_g: # god mode, cheat ;)
						self.user.gainPower(self.c.POWER_UP)
                                        elif k ==pygame.K_l: #auto victory
                                                self.victory()

				elif event.type == pygame.USEREVENT:
					self.updateBombs()
				elif event.type == pygame.USEREVENT+1:
					for e in self.enemies:
						self.movementHelper(e,e.nextMove())

				self.updateDisplayInfo()
				pygame.display.update()
	
	def deployBomb(self,player):
                b = player.deployBomb() #returns a bomb if available
		if b != None:
                        tile = self.field.getTile(player.position)
                        tile.bomb = b
                        self.bombs.append(b)
		
	def blit(self,obj,pos):
		self.screen.blit(obj,pos)
	
	def movementHelper(self, char, point):
		nPoint = char.position.move(point)

		tile = self.field.getTile(nPoint)

		#also check for bomb / special power ups here
		if tile.canPass():
			if char.instance_of == 'player' and tile.isPowerUp():
				char.setScore(100) #score when you get powerup
				char.gainPower(tile.type)
				tile.destroy()
				self.blit(tile.getBackground(),nPoint)
			char.move(point)
			
			self.blit(char.image, char.position)

			t = self.field.getTile(char.old)
			if t.bomb != None:
				self.blit(t.getBackground(),char.old)
			self.blit(t.getImage(), char.old)

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

                        mp = music.Music()
                        mp.playSound("bomb")

			explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_a.png").convert()
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
	
	def bombHelper(self, bomb, direction):
		if direction == 'right':
			point = (40,0)
		elif direction == 'left':
			point = (-40,0)
		elif direction == 'up':
			point = (0,-40)
		elif direction == 'down':
			point = (0,40)

		x = y = 0
		while True:
			x += point[0]
			y += point[1]

			nPoint = bomb.position.move((x,y))
			t = self.field.getTile(nPoint)

			#hit a block or indestructible object
			if not t.canBombPass():
				#trigger new bomb explosion
				if t.bomb != None:
					self.activateBomb(t.bomb)
				elif t.destroyable == True:
					#if brick or powerup or player
					t.destroy()
					self.blit(t.getImage(),nPoint)
					self.user.setScore(20) #score when are destory something
				break
			else:
				#path which explosion can travel on
				self.checkPlayerEnemyBombCollision(nPoint)

				explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_a.png").convert()
				self.blit(explosion,nPoint)
				self.resetTiles.append(nPoint)
			
			#check bomb's power
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
		#check if player was hit by bomb
		for player in self.players:
			if player.position == position:
				if player.loseLifeAndGameOver():
					self.gameover(player)
				else:
					#if the player gets hit by a blast, reset it's position to the starting position
					self.resetPlayerPosition(player,True)
		
		#check if enemy was hit by bomb
		for enemy in self.enemies:
			if enemy.position == position:
				self.enemies.remove(enemy)
				self.user.setScore(200) #score when you kill someone

	def checkPlayerEnemyCollision(self):
		for enemy in self.enemies:
			if enemy.position == self.user.position:
				if self.user.loseLifeAndGameOver():
					self.gameover(self.user)
				self.user.setScore(-300) #score when enemy dies
				self.resetPlayerPosition(self.user,True)
	
	def checkWinConditions(self):
		if self.mode == self.c.START:
			if len(self.enemies) == 0:
				self.victory()

	def gameover(self, player):
		if self.mode == self.c.START:
			print 'GAMEOVER'
			print 'LOST ALL LIVES OR TIME RAN OUT'
			self.highscores.addScore(player.score)
			self.gameActive = False
			self.exitGame = True
	
	def fQuit(self):
		self.gameActive = False
		self.exitGame = True
		self.forceQuit = True

	def printText(self,text,point):
		font = pygame.font.Font("Pokemon GB.ttf",20)
		label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
		textRect = label.get_rect()
		textRect.x = point[0] 
		textRect.y = point[1]
		self.blit(label, textRect)
	
	def victory(self):
		self.gameActive = False
		self.user.setScore(1000) #score when level is won
		self.level += 1
		if self.level > 6:
			self.stage += 1
			self.level = 1
		mp = music.Music()
		mp.playSound("victory")
		print 'victory fanfare'
		time.sleep(5) #time for victory fanfare to finish

	def updateTimer(self):
		self.timer -= 1

		#user lost
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
