import sys, pygame, game, config, highscore

#titlescreen class
class titleScreen():

    def __init__(self):
        self.c = config.Config()
        exitMain = False

        while not exitMain:
            pygame.init()
            self.screen = pygame.display.set_mode((1028,768))
            pygame.display.set_caption("Bomber Man")

            
