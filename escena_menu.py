# -*- coding: utf-8 -*-
import pilas
import random
from escena_ayuda import Ayuda
class EscenaMenu(pilas.escena.Base):
	def __init__(self):
		pilas.escena.Base.__init__(self)
	
	def iniciar(self):
		pilas.fondos.Fondo("fondo_menú.jpg")
		pilas.avisar(u"Use el teclado para controlar el menú.")
		self.crear_el_menu_principal()
	
	def crear_el_menu_principal(self):
		opciones = [("Comenzar a jugar", self.comenzar_a_jugar),("Ver ayuda",self.mostrar_ayuda_del_juego),("Salir", self.salir_del_juego)]

		self.menu = pilas.actores.Menu(opciones, y=-50)

	def comenzar_a_jugar(self):
		import escenajuego
		pilas.cambiar_escena(escenajuego.Juego())

	def mostrar_ayuda_del_juego(self):
		import escena_ayuda
		pilas.cambiar_escena(escena_ayuda.Ayuda())
		
	def salir_del_juego(self):
		pilas.terminar()



