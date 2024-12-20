from pygame.time import get_ticks

# timer sind dazu da, um nach einer bestimmten zeit, dinge auszuloesen
# z.b. das zufaellige aendern der bewegung von den skelleten

class Timer:
	def __init__(self, duration, repeat = False, autostart = False, func = None):
		self.duration = duration
		self.start_time = 0
		self.active = False
		self.repeat = repeat
		self.func = func
		if autostart:
			self.activate()

	def activate(self):
		self.active = True
		self.start_time = get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()

	def update(self):
		if self.active:
			#print(self.duration)
			current_time = get_ticks()
			#print(current_time)
			if current_time - self.start_time >= self.duration:
				if self.func:
					self.func()	
				self.deactivate()

#timer code from "clear code"