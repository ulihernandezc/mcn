class Comportamiento():
	def __init__(self, tipo):
		self.tipo = ''
		self.setTipoComportamiento(tipo)
		self.duracion = 0
		self.picosEnRafaga = 0
		self.duracionPicos = 0
		self.enElTiempo = 0
		self.tiempoInicial = 0
	
	def setDuracion(self, duracion): self.duracion = duracion
	def setPicosEnRafaga(self, picosEnRafaga): self.picosEnRafaga = picosEnRafaga
	def setDuracionPicos(self, duracionPicos): self.duraconPicos = duracionPicos
	def setEnElTiempo(self, enElTiempo): self.enElTiempo = enElTiempo
	def setTiempoInicial(self, tiempoInicial): self.tiempoinicial = tiempoInicial
	def getTipo(self): return self.tipo
	def getDuracion(self): return self.duracion
	def getPicosEnRafaga(self): return self.picosEnRafaga
	def getDuracionPicos(self): return self.duracionPicos
	def getEnElTiempo(self): return self.enElTiempo
	def getTiempoInicial(self): return self.tiempoInicial
	
	def setTipoComportamiento(self, tipo):
		if tipo == 0:
			self.tipo = "Silente"
		elif tipo == 1:
			self.tipo = "Pico"
		elif tipo == 2:
			self.tipo = "Rafagas de picos"
	
	