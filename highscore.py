import sys, pygame, config

class Highscore:
	def __init__(self):
		self.c = config.Config()
		self.reloadScoreData()
	
	def reloadScoreData(self):
		file = open(self.c.HIGHSCORE,"r").readlines()
		
		self.scores = []
		row = 0
		for line in file:
			self.scores.append(int(line))
	
		#sort scores
		self.scores.sort()
		self.scores.reverse()
	
	def addScore(self,score):
		file = open(self.c.HIGHSCORE,"a")
		file.write(str(score)+"\n")

	#the score screen
	def displayScore(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.c.WIDTH,self.c.HEIGHT))

                #background image
		imagePath = self.c.IMAGE_PATH + "hsb.png"
		img = pygame.image.load(imagePath).convert()
		self.screen.blit(img,(0,0))

		indx = 1
		for score in self.scores:
			self.printText("%d- %d" % (indx,score),(200,75+25*indx))
			indx += 1
		pygame.display.flip()
		
		exit = False
		while not exit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					exit = True

	def clearBackground(self):
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.screen.blit(bg,(0,0))

	def printText(self,text,point):
		font = pygame.font.Font("Pokemon GB.ttf",20)
		label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
		textRect = label.get_rect()
		textRect.x = point[0] 
		textRect.y = point[1]
		self.screen.blit(label, textRect)
				
	def printScores(self):
		indx = 1
		for score in self.scores:
			print "%d- %d" % (indx,score)
			indx += 1

#DEBUG
if __name__ == "__main__":
	h = Highscore()
	h.displayScore()
	raw_input("quit")

