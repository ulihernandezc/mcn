from comportamiento import Comportamiento

SILENTE = 0
PICO = 1
RAFAGAS_DE_PICOS = 2

class LecturaComportamiento():
	def __init__(self):       
		self.xMinValEstable = 0	#Minimo valor estable (minimo que se repite mas veces)
		self.vecesRepetidasMVE = 0	#Veces que se repite el minimo valor estable
		self.xMinValor = 0			#Minimo valor que toma X_n
		self.registroValoresMinimos = []	#Registro de valores minimos (se agrega cada que un valor esta decreciendo)
		self.registroComportamientos = []		#Registro de comportamientos SILENTEE = 0, PICO = 1, BURST = 2
		self.xUltimoValor = 0			#ultimo valor que entro
		self.incrementando = False		#Booleano para saber si X_n esta incrementandose
		self.decrementando = False		#Booleano para saber si X_n esta decrementando
		self.comportamientoActual = -1		#Comportamiento actual, -1 = Desconocido, SILENTEE = 0, PICO = 1, BURST = 2
		self.tipo = ""				#Tipo de comportamiento
		self.picosAntesDeRafaga = 0 	#variable para contar los spikes, y en el caso de que haya un silente, se indica un burst
		self.isExcedidoMinValorEstable = False 	#el minimo valor estable ya fue excedido? Variable para indicar un silente
		self.tiempo = -1				#Tiempo, o "n", en la grafica
		self.duracionUltimoComportamiento = 0	#Duracion del ultimo comportamiento (se toma como medida para medir los comportamientos)
		self.duracionUltimosPicos = 0	#Duracion de los ultimos spikes (se toma como medida para medir la duracion de los spikes de una rafaga)
		self.duracionUltimaRafaga = 0 #Duracion de la ultima rafaga (se toma como medida para medir la duracion de las rafagas)
		self.rafagaGuardada = False     #Bandera para saber si ya se guardo una rafaga (despues de agregarla se le incluye el tiempo del silente)
		self.ultimaRafagaGuardada = 0		#Duracion de la ultima rafaga ( se toma como medida para calcular la duracion completa de las rafagas)
	
	def leer(self, valor):	 #funcion para calcular el comportamiento de una neurona a partir de leer los valores de X_n
		self.tiempo += 1		 #cada que se usa la funcion, se aumenta un tiempo, porque en el calculo se llama a esta funcion cada n tiempo
		if valor < self.xMinValor:    
			self.xMinValor = valor		#si el valor que entra es menor que el valor minimo, es el nuevo minimo
			
		if valor < self.xUltimoValor:			#si el valor es menor que el ultimo valor que entro
			if valor in self.registroValoresMinimos:              #si el valor se encuentra en el registro de valores menores
				count = self.registroValoresMinimos.count(valor)	#cuenta cuantas veces se repite el valor
				if count > self.vecesRepetidasMVE:		#si las veces que se repite son mayores a las veces que se repite el minValorEstable
					self.xMinValEstable = valor		#entonces el minimo valor estable es el nuevo que entra
					self.vecesRepetidasMVE = count		#entonces las veces que se repite el MSV es igual a count
			self.registroValoresMinimos.append(valor)  #se agrega el valor al registro de valores menores
			if valor < self.xMinValEstable:    #Si el valor, es menor al Minimo Valor Estable
				if self.isExcedidoMinValorEstable == True:	#Si ya se excedio el valor minimo estable (valor < xMinValEstable) mas de una vez
					ultimo = len(self.registroComportamientos)-1		#calcula el ultimo elemento en el registro de comportamientos
					if not ultimo < 0:	#en el caso de que aun no haya valores en el registro de comportamientos
						if not self.registroComportamientos[ultimo].tipo == "Silent":	#Si el ultimo comportamiento no es un silente
							if self.registroComportamientos[ultimo].tipo == "Burst of spikes":
								self.rafagaGuardada = True
							b = Comportamiento(SILENTE)
							b.setEnElTiempo(self.tiempo)
							self.registroComportamientos.append(b)			#Entonces el comportamiento es un silente (es innecesario poner mas silencios)
							#print "AGREGUE UN SILENTEE Tiempo: ", self.tiempo
						if self.picosAntesDeRafaga > 1:				#Si hay un silente, y varios spikes antes
							#print "PICOS BEFORE: ", self.picosAntesDeRafaga
							b = Comportamiento(RAFAGAS_DE_PICOS)
							b.setPicosEnRafaga(self.picosAntesDeRafaga)
							b.setDuracionPicos(self.tiempo-self.duracionUltimosPicos-1)
							b.setEnElTiempo(self.tiempo)
							self.registroComportamientos.append(b) #entonces hay un comportamiento burst of spikes
							#print "AGREGUE UN BURST Tiempo: ", self.tiempo
							self.picosAntesDeRafaga = 0			#el conteo de spikes se regresa a 0
							self.duracionUltimosPicos += b.getDuracionPicos()
							self.ultimaRafagaGuardada = len(self.registroComportamientos)-1
						else:
							self.picosAntesDeRafaga = 0 			#si hay un silente, y no hay mas de 1 spike, entonces no hay burst, se reinicia el conteo de spikes
				else:
					self.isExcedidoMinValorEstable = True	#Si no se habia excedido el valor, y entra al if, entonces ya va 1 vez que se excede
			if self.incrementando:
				self.isExcedidoMinValorEstable = False	#en el momento que hay un spike, el ya no se excede el valor min estable
				b = Comportamiento(PICO)
				b.setDuracion(self.tiempo-self.duracionUltimoComportamiento+1)
				b.setEnElTiempo(self.tiempo)
				self.registroComportamientos.append(b)		#si se encontraba creciente y ahora decrece, el comportamiento actual es un spike
				#print "AGREGUE UN PICO Tiempo: ", self.tiempo
				self.picosAntesDeRafaga += 1			#si hay un spike, los spikes antes de una rafaga aumentan
				if self.rafagaGuardada:
					self.duracionUltimosPicos += b.getDuracion()-1
					self.registroComportamientos[self.ultimaRafagaGuardada].setDuracion(self.registroComportamientos[self.ultimaRafagaGuardada].getDuracionPicos()+b.getDuracion()-1)
					self.rafagaGuardada = False
				self.duracionUltimoComportamiento += b.getDuracion()
			self.decrementando = True		#el comportamiento es decreciente
			self.incrementando = False
		else:
			self.incrementando = True 		#el comportamiento es creciente
			self.decrementando = False
		
		self.xUltimoValor = valor		#se actualiza el ultimo valor
	
	def countComportamientos(self,comportamiento):
		count = 0
		for b in self.registroComportamientos:
			if b.tipo == comportamiento:
				count +=1
		return count
	
	def calcularTipoComportamiento(self):		#funcion que calcula el tipo de compportamiento general en base al registro de comportamientos
		spikes = self.countComportamientos("Pico")		#Calcula las veces que se repiten los comportamientos
		burst_of_spikes = self.countComportamientos("Rafagas de picos")
		silents = self.countComportamientos("Silente")
		if spikes == 1 and silents == 1:	#en el calculo del comportamiento, siempre se encuentra con un spike al inicio, pero
			self.tipo = "Silente"			#cuando es una grafica silente queda 1 = 1, por eso se hace esta excepcion
		else:						
			if burst_of_spikes > 2:				#de lo contrario se calcula con el que tenga mayor incidencias de comportamientos
				self.tipo = "Rafagas de picos"  #a excepcion de burst, mas de 2 se considera un comportamiento de rafagas
			elif spikes >= silents:
				self.tipo = "Picos periodicos"
			elif silents > spikes:	
				self.tipo = "Silente"
			else:
				self.tipo = "Desconocido"							#Si no hay un comportamiento mayor, es desconocido
