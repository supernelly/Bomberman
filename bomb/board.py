import sys, tile, pygame, config

class Board:
    
    def __init__(self)
    
        self.board = []
        tileMap = [ [GROUND for w in range(WIDTH)] for h in range(HEIGHT) ]

        #setting the map
        for rw in range(HEIGHT): #loop each row
            for cl in range(WIDTH): #loop each column in row
                randomNumber = random.randint(0,15) #random number from 0-15
                if randomNumber <= 12:
                    tile = BRICK
                else:
                    tile = GROUND
                tileMap[rw][cl] = tile
            print ""
            
        self.height = HEIGHT
        self.width = WIDTH

        
    def getTile(self,point):

	c = config.Config()
		
	cl = int(point[0]/c.tileSize)
	rw = int(point[1]/c.tileSize)
	return self.board[rw][cl]        
