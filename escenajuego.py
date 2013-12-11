#-*-coding:utf-8-*-
import pilas
import random
import zombiediana
from pilas.comportamientos import Comportamiento

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
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#------------------------------------------------------------------------------------------
class Estado:

	def actualizar(self):
		pass #sobrescribir este metodo
#------------------------------------------------------------------------------------------
class Juegando(Estado):

	def __init__(self,juego,nivel):
#usamos el contador de puntaje como contador de tiempo 
		self.tiempo=pilas.actores.Puntaje(x=-230,y=200,color=pilas.colores.blanco)
#esta es la variable que va a tener el VALOR del tiempo
		self.tiempo2=0
		self.nivel=nivel
		self.juego=juego
		self.juego.salezombie(cantidad=nivel+3)
#cuenta los segundos que pasan en la función actualizar
		pilas.mundo.agregar_tarea(1,self.actualizar)
		
	def actualizar(self):
#aumentamos en uno el contador de tiempo
		self.tiempo.aumentar(1)
		self.tiempo2+=1
#cuando llegue a 60 segundos se acabó el juego
		if self.tiempo2==60:
			self.juego.cambiar_estado(SeTermino(self.juego))
		
		if self.juego.ha_eliminado_todos_los_zombies():
			self.juego.cambiar_estado(Iniciando(self.juego,self.nivel+1))
			return False

		return True
#------------------------------------------------------------------------------------------
class Iniciando(Estado):

	def __init__(self,juego,nivel):
		self.texto = pilas.actores.Texto("Empezo %d" %(nivel))
		self.texto.escala = 0.1
		self.texto.escala = [1]
		self.texto.rotacion = [360] 
		self.nivel = nivel
		self.texto.color = pilas.colores.negro
		self.contador_de_segundos = 0
		self.juego = juego
		pilas.mundo.agregar_tarea(1,self.actualizar)

	def actualizar(self):
		self.contador_de_segundos +=1

		if self.contador_de_segundos >2:
			self.juego.cambiar_estado(Juegando(self.juego,self.nivel))
			self.texto.eliminar()
			return False
		return True
#------------------------------------------------------------------------------------------
class SeTermino(Estado):

	def __init__(self,juego,tiempo):
		self.tiempo=tiempo
	#muestra el mensaje de se acabo el tiempo
		pilas.avisar(u"se acabó el tiempo, Conseguiste % de puntos presiona ESC para volver al menú" %(puntos.obtener()))

	def cuando_pulsa_tecla(self,*k,**kw):
		import escena_menu
		pilas.cambiar_escena(escena_menu.EscenaMenu())

	def actualizar():
		pass
#------------------------------------------------------------------------------------------
class Juego(pilas.escena.Base):
	def __init__(self):
		pilas.escena.Base.__init__(self)
	
	def iniciar(self):
		pilas.fondos.Fondo("fondo_juego.png")
		self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)
		self.zombies=[]
		self.crear_tirador()
		self.cambiar_estado(Iniciando(self,1))
		self.puntos=pilas.actores.Puntaje(x=230,y=200,color=pilas.colores.blanco)

	def cambiar_estado(self,estado):
		self.estado=estado

	def crear_tirador(self):
		juan=Tirador()
		juan.definir_enemigos(self.zombies,self.cuando_explota_zombie)

	
	def cuando_explota_zombie(self):
		self.puntos.aumentar(1)

	def cuando_pulsa_tecla_escape(self,*k,**kw):
		import escena_menu
		pilas.cambiar_escena(escena_menu.EscenaMenu())
	
	def salezombie(self,cantidad):
		fuera_de_la_pantalla = [-600,-650,-700,-750,-800]
		for x in range(cantidad):
			x= random.choice(fuera_de_la_pantalla)
			y= random.choice(fuera_de_la_pantalla)
			zombie_nuevo=zombiediana.zombie(self.zombies,x=random.randrange(-320, 320),y=240)
			self.zombies.append(zombie_nuevo)
	
	def ha_eliminado_todos_los_zombies(self):
		return len(self.zombies)==0

#------------------------------------------------------------------------------------------














		
	

		
	
