import pygame, config

class Character(pygame.sprite.Sprite):
    speed = 1
    lives = 1

    def __init__(self, name, imageName, point):
        pygtame.sprite.Sprite.__init__(self)
        self.c = config.Config()
        self.name = name
        self.imageName = imageName
        self.sPosition = point
        self.reset(True)

    def reset(self,bool):
        self.getImage('down')
        self.position = self.image.get_rect()
        self.move(self.sPosition)

    def getImage(self, direction):
        imagePath = self.c.IMAGE_PATH + self,imageName + direction + ",png"
        self.image + pygame.image.load(imagePath).convert()

    def update(self):
        print "=D"

    def movement(self,key):
        c = config.Config()

        if key == pygame.K_UP:
            self.getImage('up')
	    return [0, -1*c.tileSize]
	elif key == pygame.K_DOWN:
            self.getImage('down')
	    return [0, c.tileSize]
	elif key == pygame.K_LEFT:
	    self.getImage('left')
	    return [-1*c.tileSize, 0]
	elif key == pygame.K_RIGHT:
	    self.getImage('right')
	    return [c.tileSize, 0]

    def move(self,point):
	self.old = self.position
	self.position = self.position.move(point)







		    
