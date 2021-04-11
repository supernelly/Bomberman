import pygame, config, character

#bomb class
class Bomb(pygame.sprite.Sprite):
    fuse = 3

    def __init(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.c = config.Config()

        self.image = pygame.image.load('bomb1.png')
        self.position = self.image.get_rect()
        self.position = self.position.move((playerPosition[0]*tileSize,playerPosition[1]*tileSize))
        self.range = player.power
        self.player = player
        self.triggered = False

    def tick(self):
        self.fuse -= 1
        return self.fuse
            
    def explode(self):
        
        self.player.currentBomb += 1




