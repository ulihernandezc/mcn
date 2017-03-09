from dinamicaSimple import DinamicaSimple
import numpy as np

class Neurona():
	def __init__(self, id):
		self.id = id
		self.x = []
		self.y = []
		self.posX = None
		self.posY = None
		self.x0 = 0
		self.y0 = 0
		self.alpha = 0		
		self.sigma = 0
		self.betaI = 0
		self.sigmaI = 0
		self.vecindad = []
		self.mu = 0.001
		self.dinamicaSimple = DinamicaSimple()
	
	def setX(self, x): self.x = x
	def setY(self, y): self.y = y
	def setAlpha(self, alpha): self.alpha = alpha
	def setSigma(self, sigma): self.sigma = sigma
	def setX0(self, x0):
		self.x0 = x0
		self.x.append(x0)
	def setY0(self, y0):
		self.y0 = y0
		self.y.append(y0)
	def setPosX(self, posX): self.posX = posX
	def setPosY(self, posY): self.posY = posY
	def setBetaI(self, betaI): self.betaI = betaI
	def setSigmaI(self, sigmaI): self.sigmaI = sigmaI
	def setVecindad(self, vecindad): self.vecindad = vecindad
	def getX(self): return self.x
	def getY(self): return self.y
	def getPosX(self): return self.posX
	def getPosY(self): return self.posY
	def getAlpha(self): return self.alpha
	def getBetaI(self): return self.betaI
	def getSigma(self): return self.sigma
	def getSigmaI(self): return self.sigmaI
	def getDinamicaSimple(self): return self.dinamicaSimple
	
	def calcularSigmaI(self, N, t):
		sum_v = 0
		if len(self.vecindad) == 0:
			self.sigmaI = 0.0
		else:
			for v in self.vecindad:
				sum_v += 1 * (v.getX()[t] - self.x[t])
			self.sigmaI = (1/len(self.vecindad)) * sum_v
	
	def calcularBetaI(self, gc, N, t):
		sum_v = 0
		if len(self.vecindad) == 0:
			self.betaI = 0.0
		else:
			for v in self.vecindad:
				sum_v += 1 * (v.getX()[t] - self.x[t])
			self.betaI = (gc/len(self.vecindad)) * sum_v

	def calcularEstadosIniciales(self):
		x = 0
		y = 0
		if self.x[0] <= 0:
			x = self.alpha/(1 - self.x[0]) + (self.y[0] + self.betaI)
		elif ((self.x[0] > 0) and (self.x[0] < (self.alpha + (self.y[0] + self.betaI)))):
			x = self.alpha + (self.y[0] + self.betaI)
		elif self.x[0] >= (self.alpha + (self.y[0] + self.betaI)):
			x = -1
		
		y = self.y[0] - (self.mu * (self.x[0]+1)) + (self.mu * self.sigma) + (self.mu * self.sigmaI)
		self.x.append(x)
		self.y.append(y)
	
	def calcularEstadosIniciales1(self):
		x = 0
		y = 0
		if self.x[1] <= 0:
			x = self.alpha/(1 - self.x[1]) + (self.y[1] + self.betaI)
		elif ((self.x[1] > 0) and (self.x[1] < (self.alpha + (self.y[1] + self.betaI)))):
			x = self.alpha + (self.y[1] + self.betaI)
		elif self.x[1] >= (self.alpha + (self.y[1] + self.betaI)):
			x = -1
		
		y = self.y[1] - (self.mu * (self.x[1]+1)) + (self.mu * self.sigma) + (self.mu * self.sigmaI)
		self.x.append(x)
		self.y.append(y)
		
	def reposicionar(self, n, F, L_MAX):
		ri = np.array([self.posX, self.posY])
		sumr_vec = np.array([0.0, 0.0])
		sumx_vec = 0
		for j in self.vecindad:
			sumx_vec += j.getX()[n]
			rj = np.array([j.getPosX(), j.getPosY()])
			norm = np.linalg.norm(rj - ri)
			if norm == 0.0:
				sumr_vec += (rj - ri)
			else:
				sumr_vec += ((rj - ri)/(norm))
		sumx_vec *= self.x[n]
		ri = ri + (F * sumr_vec * sumx_vec)
		x = ri[0]
		y = ri[1]
		if x > L_MAX:
			x -= L_MAX
		if x < 0:
			x += L_MAX
		if y > L_MAX:
			y -= L_MAX
		if y < 0:
			y += L_MAX
		self.posX = x
		self.posY = y
		
		
		