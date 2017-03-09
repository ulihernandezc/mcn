from neurona import Neurona
import matplotlib.pyplot as plt
import random as rnd
import math

class Simulacion():
	def __init__(self, N, R, gc):
		self.N = N
		self.L_MAX = 50
		self.neuronas = []
		self.mu = 0.001
		self.R = R
		self.F = 0.01
		self.gc = gc
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)
	
	def crearNeuronas(self):
		for i in range(self.N):
			n = Neurona(i)
			self.neuronas.append(n)
	
	def calcularVecinos(self, neurona):
		vecindad = []
		for n in self.neuronas:
			if n.id != neurona.id:
				if self.distancia(neurona, n) <= self.R:
					vecindad.append(n)
		return vecindad
		
	def inicializarNeuronas(self):
		self.crearNeuronas()
		for neurona in self.neuronas:
			neurona.setAlpha(rnd.uniform(3,6))
			neurona.setSigma(rnd.uniform(-0.5, 0.6))
			neurona.setPosX(rnd.uniform(0,self.L_MAX))
			neurona.setPosY(rnd.uniform(0,self.L_MAX))
			neurona.setX0(rnd.uniform(-2, 2))
			neurona.setY0(rnd.uniform(-4, -3))
			neurona.setBetaI(rnd.uniform(-2, 2))
		for neurona in self.neuronas:
			neurona.setVecindad(self.calcularVecinos(neurona))
			neurona.calcularSigmaI(self.N, 0)
			neurona.calcularEstadosIniciales()
		for neurona in self.neuronas:
			neurona.reposicionar(1, self.F, self.L_MAX)
		for neurona in self.neuronas:
			neurona.calcularBetaI(self.gc, self.N, 1)
			neurona.calcularSigmaI(self.N, 1)
		for neurona in self.neuronas:
			neurona.setVecindad(self.calcularVecinos(neurona))
		for neurona in self.neuronas:
			neurona.calcularEstadosIniciales1()
	
	def distancia(self, n1, n2):
		d = math.sqrt(pow(n2.getPosX() - n1.getPosX(), 2) + pow(n2.getPosY() - n1.getPosY(), 2))
		return d
		
			
	def simular(self):
		self.inicializarNeuronas()
		n = 2
		total_n = 10000
		while n < total_n:
			for neurona in self.neuronas:
				neurona.calcularSigmaI(self.N, n)
				neurona.calcularBetaI(self.gc, self.N, n)
				x = 0
				y = 0
				if neurona.getX()[n-1] <= 0:
					x = neurona.getAlpha()/(1 - neurona.getX()[n-1]) + (neurona.getY()[n-1] + neurona.getBetaI())
				elif (((neurona.getX()[n-1] > 0) and (neurona.getX()[n-1] < (neurona.getAlpha() + (neurona.getY()[n-1] + neurona.getBetaI())))) and (neurona.getX()[n-2] <= 0)):
					x = neurona.getAlpha() + (neurona.getY()[n-1] + neurona.getBetaI())
				elif ((neurona.getX()[n-1] >= (neurona.getAlpha() + (neurona.getY()[n-1] + neurona.getBetaI()))) or neurona.getX()[n-2] > 0):
					x = -1
		
				y = neurona.getY()[n-1] - (self.mu * (neurona.getX()[n-1]+1)) + (self.mu * neurona.getSigma()) + (self.mu * neurona.getSigmaI())
				neurona.getX().append(x)
				neurona.getY().append(y)
				neurona.reposicionar(n-1, self.F, self.L_MAX)
			for neurona in self.neuronas:
				neurona.setVecindad(self.calcularVecinos(neurona))
			self.graficar()
			n += 1
	
	def graficar(self):
		for neurona in self.neuronas:
			self.ax.plot(neurona.getPosX(), neurona.getPosY(), 'bo')
		plt.pause(1)
		plt.cla()
		
