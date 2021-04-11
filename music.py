import pygame, random, config

class Music:
	def __init__(self):
                #grab value from config.py
		self.c = config.Config()

	def playMusic(self, mode):
                #level music
		if mode == self.c.START:
			music = "leveltheme.mid"

		pygame.mixer.music.load(self.c.AUDIO_PATH + music)
		pygame.mixer.music.play(-1)

	#sound triggers
	def playSound(self, type):
		if type == "bomb":
			sound = "blast.wav"
		elif type == "victory":
			sound = "victory_fanfare.mid"

		pygame.mixer.music.load(self.c.AUDIO_PATH + sound)
		pygame.mixer.music.play()
