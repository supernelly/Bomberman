import pygame, character, config, bomb

class Player(character.Character):
	lives = 5 #lives
	currentBomb = 1
	maxBombs = 1
	power = 1 #bomb power
	score = 0

	def __init__(self, name, imageName, id, point):
		character.Character.__init__(self, name, "player/"+imageName, point)
		self.c = config.Config()
		self.id = id
		self.instance_of = 'player'
	
	# reset all stats if death is true
	def reset(self,death):
		character.Character.reset(self,True)
		if death:
			self.currentBomb = self.maxBombs = 1
			self.power = 1
			self.speed = 1

	def deployBomb(self):
		if self.currentBomb > 0:
			self.currentBomb -= 1
			b = bomb.Bomb(self)
			return b
		return None

	def gainPower(self,power):
		if power == self.c.POWER_UP:
			self.power += 1
	
	def setScore(self,score):
		self.score += score
		if self.score < 0:
			self.score = 0

	def loseLifeAndGameOver(self):
		self.lives -= 1
		return self.lives <= 0
