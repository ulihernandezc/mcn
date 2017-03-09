from lecturaComportamiento import LecturaComportamiento

class DinamicaSimple():
	def __init__(self):
		self.x = []		#arreglo de los valores de x
		self.y = []		#arreglo de los valores de y
		self.mu = 0.001   #constante mu
		self.alpha = 0		#variable que representa el parametro externo alfa
		self.sigma = 0		#variable que representa el parametro externo sigma
		self.x0 = 0    #valor inicial del arreglo x, antes de iniciar el ciclo para calcular
		self.y0 = 0		#valor inicial del arreglo y, antes de iniciar el ciclo para calcular
		self.ciclos = 0		#numero de ciclos que dara, para calcular los valores de x, y
		self.n = []			#arreglo de los valores de n
		self.comportamiento = LecturaComportamiento()
	
	def setMu(self, mu): self.mu = mu					#sets y gets
	def setAlpha(self, alpha): self.alpha = alpha
	def setSigma(self, sigma): self.sigma = sigma
	def setX0(self, x0): self.x0 = x0
	def setY0(self, y0): self.y0 = y0
	def setCiclos(self, ciclos): self.ciclos = ciclos
	def getMu(self): return self.mu
	def getAlpha(self): return self.alpha
	def getSigma(self): return self.sigma
	def getX0(self): return self.x0
	def getY0(self): return self.y0
	def getCiclos(self): return self.ciclos
	def getN(self): return self.n
	def getX(self): return self.x
	
	def configurarYCalcular(self, mu, alpha, sigma, x0, y0, ciclos):  #funcion para configurar y calcular dinamica simple en tiempo establecido
		self.mu = mu
		self.alpha = alpha
		self.sigma = sigma
		self.x0 = x0
		self.y0 = y0
		self.ciclos = ciclos
		self.calcular()
	
	def calcular(self):		#funcion para calcular la dinamica simple de la neurona
		self.x.append(self.x0)	#agrega al arreglo de valores de x, el primer valor especificado, n(0)
		self.y.append(self.y0)	#agrega al arreglo de valores de y, el primero valor especificado, n(0)
		self.n.append(0)		#agrega al arreglo de valores de n, el valor 0
		n = 1	#inicializa la variable n en 1, ya que n(0) ya se definio
		while n < self.ciclos:
			x = 0
			y = 0
			if n == 1:  #como en la funcion se necesita el tiempo discreto n-1, en la primer vuelta del ciclo,
						#no se cuenta con este valor, se define la funcion sin ese tiempo, y apartir de n=2 se corre
						#el ciclo normalmente
				if self.x[n-1] <= 0:
					x = self.alpha/(1 - self.x[n-1]) + self.y[n-1]
				elif ((self.x[n-1] > 0) and (self.x[n-1] < (self.alpha + self.y[n-1]))):
					x = self.alpha + self.y[n-1]
				elif self.x[n-1] >= (self.alpha + self.y[n-1]):
					x = -1
				
			else:		#en el tiempo n=2, la funcion se puede evaluar de manera normal
				
				if self.x[n-1] <= 0:
					x = self.alpha/(1 - self.x[n-1]) + self.y[n-1]
				elif ((self.x[n-1] > 0 and (self.x[n-1] < (self.alpha + self.y[n-1]))) and (self.x[n-2] <= 0)):
					x = self.alpha + self.y[n-1]
				elif ((self.x[n-1] >= (self.alpha + self.y[n-1])) or self.x[n-2] > 0):
					x = -1
				
			y = self.y[n-1] - (self.mu * (self.x[n-1]+1)) + (self.mu * self.sigma)	
			self.x.append(x)
			self.y.append(y)
			self.n.append(n)
			self.comportamiento.leer(x) 		#lee el valor de X_n para calcular su comportamiento
			n += 1
		self.comportamiento.calcularTipoComportamiento() 		#al terminar el ciclo, se calcula el tipo de comportamiento que tuvo
		
		
	