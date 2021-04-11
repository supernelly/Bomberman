import pygame, character, config, bomb


class Player(character.Character):
    currentBomb = 1
    maxBombs = 1
    power = 1
    lives = 3

    def __init(self, name, imageName, id, point):
        character.Character.__init__(self, name, "players/"+imageName, point)
        self.c = config.Config()
        self.id = id
        self.instance_of = 'player'

    #reset stats if death is true
    def reset(self,death):
        character.Character.reset(self,True)
        if death:
            self.currentBomb = self.maxBombs = 1
            self.power = 1
            self.speed = 1
            
    def dropBomb(self):
        if self.currentBomb > 0:
            self.currentBomb -= 1
            b = bomb.Bomb(self)
            return b
        return None

    def gainPower(self,power):
        if power == self.c.BOMB_UP:
            self.currentBomb += 1
            self.maxBombs += 1
        elif power == self.c.POWER_UP:
            self.power += 1

    def die(self):
        sys.exit(0)
        
