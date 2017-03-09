import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
sys.path.append("..")
from modelo.neurona import Neurona

class Window(QtGui.QMainWindow):

    def __init__(self):                                     #inicio clase
        super(Window, self).__init__()
        self.setGeometry(50,50,300,200)
        self.setWindowTitle("Ventana")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.home()

    def home(self):
                                                            #declaraciones
        global textboxAlpha
        global textboxDelta
        btnExit=QtGui.QPushButton("Salir",self)             
        btnGraphics=QtGui.QPushButton("Graficar",self)      
        labelAlpha=QtGui.QLabel("Alpha",self)                   
        labelDelta=QtGui.QLabel("Delta",self)
        textboxAlpha=QtGui.QLineEdit(self)
        textboxDelta=QtGui.QLineEdit(self)
                                                            #eventos
        btnExit.clicked.connect(self.close_application)
        btnGraphics.clicked.connect(self.graphics)
                                                            #posiciones
        textboxAlpha.move(150,50)
        textboxDelta.move(150,100)
        labelAlpha.move(50,50)
        labelDelta.move(50,90)
        btnGraphics.resize(50,30)
        btnGraphics.move(190,160)
        btnExit.resize(40,30)
        btnExit.move(250,160)
        self.show()

    def close_application(self):                            #funcion salir
        opcE = QtGui.QMessageBox.question(self,'Salir',"Estas seguro de salir?",
                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if opcE==QtGui.QMessageBox.Yes:
            self.setWindowTitle("Adios")
            sys.exit(0)
        else:
            pass

    def graphics(self):                                     #funcion graficar                                 
        opcG = QtGui.QMessageBox.question(self,'Graficar',"Estas seguro de graficar?",
                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if opcG==QtGui.QMessageBox.Yes:
            self.neuron=Neurona()
            alpha = textboxAlpha.text()
            delta = textboxDelta.text()
            alpha1=float(alpha)                             #convertir QLineEdit
            delta1=float(delta)
            global mu
            global initValX
            global initValY
            global cycles
            mu=0.001
            initValX=0
            initValY=-3
            cycles=2000
            neu = Neurona()
            neu.getDinamicaSimple().configurarYCalcular(mu,alpha1,delta1,initValX,initValY,cycles)
            self.setWindowTitle("Graficando")
            plt.plot(neu.getDinamicaSimple().getN(), neu.getDinamicaSimple().getX())
            plt.ylabel('X_n')
            plt.xlabel('n')
            plt.show()
        else:
            pass
       
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
