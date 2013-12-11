# -*- coding: utf-8 -*-

import pilas

MENSAJE_AYUDA="""
Debes mover a tu tirador de izquierda
a derecha usando el teclado, (a) (d) y (ESPACIO)
para disparar. El objetivo del juego
es destruir la mayor cantidad
de dianas de zombie en el menor tiempo posible
(debes entrenarte antes de salir a la calle)
"""

class Ayuda(pilas.escena.Base):
	def __init__(self):
		pilas.escena.Base.__init__(self)


	def iniciar(self):
		pilas.fondos.Fondo("fondo_menú.jpg")
		self.crear_texto_ayuda()
		self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

	def crear_texto_ayuda(self):
		pilas.actores.Texto("Ayuda", y=200)
		pilas.actores.Texto(MENSAJE_AYUDA, y=0,x=10)
		pilas.avisar("Pulsa ESC para regresar")


	def cuando_pulsa_tecla(self, *k, **kw):
		import escena_menu
		pilas.cambiar_escena(escena_menu.EscenaMenu())

