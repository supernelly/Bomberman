import sys, pygame, config, game, highscore

#titlescreen class
class Titlescreen():

	def __init__(self):
		self.c = config.Config()
		exitMain = False

		while not exitMain:
			pygame.init()
			self.screen = pygame.display.set_mode((1024,768))
			pygame.display.set_caption("Bomberman")

                        #titlescreen image
			imagePath = self.c.IMAGE_PATH + "titlescreen.png"
			img = pygame.image.load(imagePath).convert()
			self.screen.blit(img,(0,0))

                        #load music
			pygame.mixer.music.load(self.c.AUDIO_PATH + "title.mid")
			pygame.mixer.music.play()

			clock = pygame.time.Clock()
			pygame.mouse.set_visible(True)
			pygame.display.flip()
			userInteracted = False

			while not userInteracted:
				clock.tick(self.c.FPS)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						userInteracted = True
						exitMain = True
						pygame.quit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							userInteracted = True
							exitMain = True
							pygame.quit()
					#start and exit button
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if self.withinBoundary(99, 240, 348, 386):
							userInteracted = True
							self.startGame() #Start button clicked
						elif self.withinBoundary(790, 900, 348, 386):
							userInteracted = True
							exitMain = True
							pygame.quit() #Exit clicked
						elif self.withinBoundary(340, 665, 700, 740):
							userInteracted = True
							self.highScore() #Highscore clicked

        #button boundary
	def withinBoundary(self, x1, x2, y1, y2):
		if pygame.mouse.get_pos()[0] >= x1 and pygame.mouse.get_pos()[0] <= x2 and pygame.mouse.get_pos()[1] >= y1 and pygame.mouse.get_pos()[1] <= y2:
                        return True
		return False

	def startGame(self):
		g = game.Game(self.c.START)

	def highScore(self):
		h = highscore.Highscore()
		h.displayScore()

if __name__ == "__main__":
    t = Titlescreen()
