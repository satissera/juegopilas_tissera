#! /usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
import pilas
from pilas.comportamientos import Comportamiento
import zombiediana

#----------------------------------------------------------------------
pilas.iniciar()
#----------------------------------------------------------------------
#Definimos las teclas a usar
teclas={pilas.simbolos.a:'izquierda', pilas.simbolos.d:'derecha', pilas.simbolos.ESPACIO:'boton'}
#----------------------------------------------------------------------
#creamos el control personalizado
mandos=pilas.control.Control(pilas.escena_actual(),teclas)
#----------------------------------------------------------------------
tiempo=6
velocidad=6
#----------------------------------------------------------------------
#variables del juego

fin_de_juego=False
tiempo=6
balassimples = pilas.actores.Bala
#----------------------------------------------------------------------

#la clase del actor
class Tirador(pilas.actores.Actor):

	def __init__(self,x=0, y=0):
		pilas.actores.Actor.__init__(self,x=0,y=-200)
		self.imagen=pilas.imagenes.cargar_grilla("cuchillopistola.png",15)
		self.definir_cuadro(9)
		self.hacer(Esperando2())
		self.aprender(pilas.habilidades.MoverseConElTeclado)
		self.aprender(pilas.habilidades.SeMantieneEnPantalla)
		self.aprender(pilas.habilidades.MoverseConElTeclado,control=mandos)
		self.aprender(pilas.habilidades.Disparar,municion=balassimples,offset_disparo=(29,29),escala=0.7)
		self.balas=0

	def definir_cuadro(self,indice):
		self.imagen.definir_cuadro(indice)

		self.radio_de_colision=30

	def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
		self.cuando_elimina_enemigo = cuando_elimina_enemigo
		self.habilidades.Disparar.definir_colision(grupo, self.hacer_explotar_al_enemigo)
	def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
		mi_disparo.eliminar()
		el_enemigo.eliminar()
		if self.cuando_elimina_enemigo:
			self.cuando_elimina_enemigo()	

		


#----------------------------------------------------------------------
	#esta clase es cuando el personaje no hace nada excepto moverse con la pistola
class Esperando2(Comportamiento):
	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.receptor2.definir_cuadro(9)

	def actualizar(self):

		if mandos.izquierda:
#modificacion de la velocidad porque si no el actor se mueve muy lentamente (la velocidad es de 6)
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
		else:
			self.receptor2.hacer(Esperando2())

#si toca el boton para disparar 10 veces carga la pistola
		if pilas.escena_actual().control.boton:
			self.receptor2.hacer(Disparando())
			self.receptor2.balas+=1
			if self.receptor2.balas==10:

				self.receptor2.hacer(cargar())
				self.receptor2.balas=0

#----------------------------------------------------------------------

#clase de cuando el tirador dispara con la pistola
class Disparando(Comportamiento):

	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.cuadros=[6,7,7,8,8,9,10,10,10,11,11,11,12,12,13,13,14,14]
		self.paso=9

	def actualizar(self):
		self.avanzar_animacion()		
		if mandos.izquierda:
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
#ponemos aca y no en tirador que aprenda a disparar para que cuando apriete boton dispare un solo tiro



		if not mandos.boton:

			self.receptor2.hacer(Esperando2())

#avabza la animacion


	def avanzar_animacion(self):
		self.paso+=1
		if self.paso>=len(self.cuadros):
			self.paso=9
		self.receptor2.definir_cuadro(self.cuadros[self.paso])	
#----------------------------------------------------------------------
#cuando llegue a 10 balas cargue las balas
class cargar(Comportamiento):
	def iniciar(self,receptor2):

		self.receptor2=receptor2
		self.cuadros=[8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7]
		self.paso=4

	def actualizar(self):
		self.avanzar_animacion()

		if mandos.izquierda:
#hacemos que valla hacia la izquierda con la velocidad que ya pusimos
			self.receptor2.x-=velocidad
#hacemos que valla hacia la izquierda con la velocidad que ya pusimos
		elif mandos.derecha:
			self.receptor2.x+=velocidad
#si no se aprieta el boton hace esperando			
		if not mandos.boton:
			self.cuadro=8
			self.receptor2.hacer(Esperando2())

	def avanzar_animacion(self):
		self.paso+=1
		if self.paso>=len(self.cuadros):
			self.paso=8
		self.receptor2.definir_cuadro(self.cuadros[self.paso])

#----------------------------------------------------------------------
juan=Tirador()
pilas.ejecutar()


















