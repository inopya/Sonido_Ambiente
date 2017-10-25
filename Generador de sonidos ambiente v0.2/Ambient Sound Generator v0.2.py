#!/usr/bin/env python
#-*- coding: UTF-8 -*-

#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                   Generador de  sonidos ambiente                * #
# *                    Autor: Eulogio López Cayuela                 * #
# *                                                                 * #
# *                  Versión 0.2    Fecha: 16/05/2015               * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################



import pygame, random, sys
from pygame.locals import *

# ---------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# ---------------------------------------------


FPS = 40 # Número de frames por segundo

ANCHO_PANTALLA = 400
ALTO_PANTALLA = 400
SCREEN_RESIZE = 0
SCREEN_COLOR_BITS = 32
fondoActivo = False
soundLevel = 0.3



# Bloque de definicion de colores con nombres para facilitar su uso.
COLOR_BLANCO = (255, 255, 255)
COLOR_BLANCO_SUCIO = (150, 150, 150) # Color Blanco sucio.
COLOR_NEGRO = (0, 0, 0)
COLOR_NEGRO_SUCIO = (35, 25, 35) # Color Gris oscuro casi negro.
COLOR_ROJO = (255, 0, 0)
COLOR_ROJO_OSCURO = (175, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_AZUL_OSCURO = (0, 0, 170)
COLOR_AZUL_CIELO = (45, 180, 235)
COLOR_AMARILLO = (255,255,0)
COLOR_ROSA = (255,0,210) # Color Rosa vivo.


BACKGROUND_COLOR = COLOR_NEGRO

# inicializar valores del juego
cogerObjeto = False
tecla_CONTROL = False
primerClick = False
segundoClick = False
leftButton = False
mmiddleButton = False
rightButton = False
index = 0 #indice utilicado para localizar a los controles de volumen

# --------------------------------------------
# FIN DEL BLOQUE DE DEFINICIÓN DE CONSTANTES
# --------------------------------------------

# --------------------------------------------
#  INICIO DEL BLOQUE DE DEFINICIÓN DE CLASES
# --------------------------------------------
class ControlDeVolumen:
    def __init__(self, posicion, size, indice, componentes, canal):
        self.size = size
        self.x = posicion[0]
        self.y = posicion[1]
        self.componentes = componentes
        self.canal = canal
                
        #Definicion de los elementos del control de volumen
        # * Barra
        self.barra = self.componentes[0] #diccionario que contiene la barra
        self.barraImage = self.barra['surface'] #palabra 'surface' con la imagen de la barra
        self.barraImage = pygame.transform.scale(self.barraImage, (int(self.size), int(4)))
        self.barraRect = self.barraImage.get_rect() #obtencion del -rect- al crear objeto
        self.barraRect.width = size
        self.barraRect.left = self.x #asignacion de su posicion x propia
        self.barraRect.centery = self.y #asignacion de su posicion y propia
        # * Cursor
        self.cursor = self.componentes[1] #diccionario que contiene el cursor
        self.cursorImage = self.cursor['surface']
        self.cursorRect = self.cursorImage.get_rect()
        self.cursorRect.left = self.x
        self.cursorRect.centery = self.y
        # * Altavoz
        self.altavoz = self.componentes[2] #diccionario que contiene el altavoz
        self.altavozImage = self.altavoz['mute']
        self.altavozMute = True
        self.altavozRect = self.altavozImage.get_rect()
        self.altavozRect.left = self.barraRect.right + 5
        self.altavozRect.centery = self.y

        self.recorrido = self.barraRect.width - self.cursorRect.width

    def draw(self, screen):
        screen.blit( self.barraImage, self.barraRect)
        screen.blit( self.cursorImage, self.cursorRect)
        # comprobar que icono le corresponde al altavoz segun su estado
        if self.altavozMute == False:
            self.altavozImage = self.altavoz['surface']
        else:
            self.altavozImage = self.altavoz['mute']
        screen.blit( self.altavozImage, self.altavozRect)

    # Metodos para los controles de volumen
    def cambiarVolumen(self):
        self.cursorPos = self.cursorRect.left - self.barraRect.left
        self.soundLevel = self.cursorPos/self.recorrido
        self.altavozImage = self.altavoz['mute']
        self.canal.set_volume(self.soundLevel)
        if self.soundLevel > 0.0:
            self.altavozMute = False
        else:
            self.altavozMute = True
    def muteUnMute(self):
        if self.altavozMute == False:
            self.cambiarVolumen()
        else:
            self.canal.set_volume(0)
        

# --------------------------------------------
#    FIN DEL BLOQUE DE DEFINICIÓN DE CLASES
# --------------------------------------------




# --------------------------------------------
# INICIO DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------   
def finalizarPrograma():
    pygame.quit()
    sys.exit()
    
# --------------------------------------------
def comprobarControlVolumen(posicion,listaObjetos):
    '''
    En cada llamada 'traemos' la -lista de objetos Seleccionables- y las -coordenadas del raton-
    Comprueba si al hacer click con el ratón en esas coordenadas
    hay un objeto perteneciente a la lista 'ObjetosSeleccionables'.
    '''
    x = posicion[0]
    y = posicion[1]
    for objeto in listaObjetos:
        rect = objeto.altavozRect
        if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
            objeto.altavozMute = not objeto.altavozMute
            objeto.muteUnMute()
            return(False)
        
        rect = objeto.cursorRect
        if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
            return(objeto)

    return(False)

# --------------------------------------------
def dibujar_Textos(text, size, color, surface, x, y, posicion = 0):
    textobj = size.render(text, 1, color)
    textrect = textobj.get_rect()
##    print (textrect.right)
    if posicion == 1: # centrado respecto de (y)
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = y
    if posicion == 2: # alineacion Derecha respecto de (x,y)
        textrect.topright = (x, y)
    if posicion == 0: # alineacion Izquierda respecto de (x,y)
        textrect.topleft = (x, y)
    if posicion == 3: # alineacion centro y devuelve espacio lateral
        textrect.centerx = SCREEN.get_rect().centerx
        textrect.centery = y
        surface.blit(textobj, textrect)
        return (textrect.width)
    surface.blit(textobj, textrect)



    
# --------------------------------------------
def esperarPulsacionTeclado(): # no se usa, por si creo la opcion de usar teclas de control
                               # la hice para el programa de Logica.
    pygame.event.set_allowed([KEYDOWN, KEYUP])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                finalizarPrograma()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pulsar 'escape' para terminar
                    finalizarPrograma()
                return

# --------------------------------------------
def mostrarPantallaInicial():# no se usa, por si creo una pantalla inicial tenerla de guia
                             # la hice para el programa de Logica.
    global ANCHO_PANTALLA, ALTO_PANTALLA
    mostarTextosDeInicio()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                finalizarPrograma()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    ANCHO_PANTALLA -=10
                if event.key == K_RIGHT:
                    ANCHO_PANTALLA +=10
                if event.key == K_UP:
                    ALTO_PANTALLA -= 10
                if event.key == K_DOWN:
                    ALTO_PANTALLA += 10
                if event.key == K_ESCAPE: # pulsar 'escape' para terminar
                    finalizarPrograma()
                if event.key == K_SPACE:  # pulsar 'espacio' para continuar
                    return
                mostarTextosDeInicio()

# --------------------------------------------
def mostarTextosDeInicio():  # no se usa, por si creo una pantalla inicial tenerla de guia
                             # la hice para el programa de Logica.
    global ANCHO_PANTALLA, ALTO_PANTALLA, SCREEN
    SCREEN.fill(BACKGROUND_COLOR)
    q = 6
    # Mostrar pantalla de inicio
    SCREEN = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
    dibujar_Textos('GENERADOR', font48, COLOR_VERDE, SCREEN, 0, (ALTO_PANTALLA / q),1)
    dibujar_Textos('DE SONIDO AMBIENTE',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, 0, (ALTO_PANTALLA / q) + 60,1)
    dibujar_Textos('modificar el tamaño de la ventana ahora',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, 0, (ALTO_PANTALLA / q) + 80,1)

    dibujar_Textos('TECLAS DE JUEGO',
                   font25, COLOR_AZUL_CIELO, SCREEN, 0, (ALTO_PANTALLA / q) + 130,1)
    offset = dibujar_Textos('\'RATON:\'  Usa el ratón para desplazar al jugador',
                   font25, COLOR_AZUL_CIELO, SCREEN, 0, (ALTO_PANTALLA / q) + 160,3)
    x = int(ANCHO_PANTALLA - offset)/2
    dibujar_Textos('(Tambien puedes usar las flechas)',
                   font20, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 170,0)

    dibujar_Textos('\'A:\' Acelerar Enemigos (si han sido frenados)',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 190,0)
    dibujar_Textos('\'Z:\'  Frenar Enemigos',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 210,0)
    dibujar_Textos('(los cambios de velocidad afectan a todos los niveles',
                   font20, COLOR_ROJO, SCREEN, x, (ALTO_PANTALLA / q) + 230,0)
    dibujar_Textos('pero no evita los incrementos de velocidad de cada nivel)',
                   font20, COLOR_ROJO, SCREEN, x, (ALTO_PANTALLA / q) + 245,0)
    dibujar_Textos('\'BARRA ESPACIADORA:\'  Disparar',
                   font25, COLOR_AZUL_CIELO, SCREEN, x, (ALTO_PANTALLA / q) + 265,0)
    dibujar_Textos('\'ESC:\'  Salir del juego',
                   font25, COLOR_BLANCO_SUCIO, SCREEN, x, (ALTO_PANTALLA / q) + 285,0)


    dibujar_Textos('Pulsa la tecla DISPARO para comenzar',
                   font25, COLOR_AMARILLO, SCREEN, 0, (ALTO_PANTALLA / q) + 345,1)

    pygame.display.update()
    return


# --------------------------------------------
#  FIN DEL BLOQUE DE DEFINICIÓN DE FUNCIONES
# --------------------------------------------



# ********************************************
#           INICIO DEL PROGRAMA
# ********************************************


# Inicializar la ventana y el cursor
pygame.init()
mainClock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA),SCREEN_RESIZE,SCREEN_COLOR_BITS)
pygame.display.set_caption(' Sonidos Ambiente v0.2 ')
pygame.mouse.set_visible(True)

# Definir tipos de letra
font20 = pygame.font.SysFont(None, 20)
font25 = pygame.font.SysFont(None, 25)
font30 = pygame.font.SysFont(None, 30)
font35 = pygame.font.SysFont(None, 35)
font40 = pygame.font.SysFont(None, 40)
font45 = pygame.font.SysFont(None, 45)
font48 = pygame.font.SysFont(None, 48)
font50 = pygame.font.SysFont(None, 50)
font65 = pygame.font.SysFont(None, 65)

# Inicializar MIXER para audio
pygame.mixer.init()

# Definir y cargar sonidos
lluviaSound = pygame.mixer.Sound('sonidos/lluvia.ogg')
truenoSound = pygame.mixer.Sound('sonidos/truenos.ogg')
vientoSound = pygame.mixer.Sound('sonidos/viento.ogg')
fuegoSound = pygame.mixer.Sound('sonidos/fuego.ogg')
grilloSound = pygame.mixer.Sound('sonidos/grillos.ogg')
pajaroSound = pygame.mixer.Sound('sonidos/pajaros.ogg')

print ('CARGA FINALIZADA')
#pygame.mixer.Channel(0).play(sound1, loops=-1) # Linea de ejemplo de llamada a un canal



# Establecer canales de audio (le pongo nombres en singular)
lluvia = pygame.mixer.Channel(0)
trueno = pygame.mixer.Channel(1)
viento = pygame.mixer.Channel(2)
fuego = pygame.mixer.Channel(3)
grillo = pygame.mixer.Channel(4)
pajaro = pygame.mixer.Channel(5)

# Establecer volumen inicial para cada canal
lluvia.set_volume(0.0)
trueno.set_volume(0.0)
viento.set_volume(0.0)
fuego.set_volume(0.0)
grillo.set_volume(0.0)
pajaro.set_volume(0.0)

# Asignacion de cada sonido a su canal correspondiente
# y forzar reproduccion continua 'loops = -1'
lluvia.play(lluviaSound, loops=-1)
trueno.play(truenoSound, loops=-1)
viento.play(vientoSound, loops=-1)
fuego.play(fuegoSound, loops=-1)
grillo.play(grilloSound, loops=-1)
pajaro.play(pajaroSound, loops=-1)

# Definir imagenes para los iconos
##lluviaImagen = pygame.image.load('imagenes/lluvia.png')
##lluviaRect = lluviaImagen.get_rect()
##
##truenoImagen = pygame.image.load('imagenes/trueno.png')
##truenoRect = truenoImagen.get_rect()
##
##vientoImagen = pygame.image.load('imagenes/viento.png')
##vientoRect = vientoImagen.get_rect()


# Definir imagenes para el control de volumen
barraImagen = pygame.image.load('imagenes/barravolumen.png')
barraRect = barraImagen.get_rect()
deslizanteImagen = pygame.image.load('imagenes/deslizantevolumen.png')
deslizanteRect = deslizanteImagen.get_rect()
altavozImagen = pygame.image.load('imagenes/altavozvolumen.png')
altavozMute = pygame.image.load('imagenes/altavozmute.png')
altavozRect = altavozImagen.get_rect()


barraVolumen = {'rect':barraRect,'surface':barraImagen,'index':1003,}
deslizanteVolumen = {'rect':deslizanteRect,'surface':deslizanteImagen,'index':1004,}
altavozVolumen = {'rect':altavozRect,'surface':altavozImagen,'mute':altavozMute,'index':1005,}

componentesMixer = [barraVolumen, deslizanteVolumen, altavozVolumen]

control_01 = ControlDeVolumen((90, 25),250, 1, componentesMixer, lluvia)
control_02 = ControlDeVolumen((90, 75),250, 2, componentesMixer, trueno)
control_03 = ControlDeVolumen((90,125),250, 3, componentesMixer, viento)
control_04 = ControlDeVolumen((90,175),250, 4, componentesMixer, fuego)
control_05 = ControlDeVolumen((90,225),250, 4, componentesMixer, grillo)
control_06 = ControlDeVolumen((90,275),250, 4, componentesMixer, pajaro)

listaControles = [control_01, control_02, control_03, control_04,control_05, control_06]


imagen_Fondo = pygame.image.load('imagenes/fondo.jpg').convert()



# ********************************************
# Bucle principal del programa
# ********************************************

'''
http://soundrts.blogspot.com.es/2008/01/some-pygame-examples-for-audiogame.html

https://sivasantosh.wordpress.com/2012/07/16/basic-sound-handling-pygame/
'''




while True: # Bucle para el programa. Mientras esté activo

    # Atender eventos de teclado y raton
    for event in pygame.event.get():
        if event.type == QUIT:
            finalizarPrograma()
        if event.type == MOUSEBUTTONDOWN:
            leftButton, mmiddleButton, rightButton = pygame.mouse.get_pressed()
            movRelativoX1, movRelativoY1 = pygame.mouse.get_pos()
            item = comprobarControlVolumen(event.pos, listaControles)
            # Gesion de click sobre objeto Puerta
            if item != False and leftButton == True:
                # * Seleccion de objeto para moverlo, (si se mantiene pulsado el ratón)
                focusRect = item.cursorRect
                x,y = pygame.mouse.get_pos()
                offsetX = x - focusRect.centerx # Distancia x del centro del objeto al puntero del raton
                offsetY = y - focusRect.centery # Distancia y del centro del objeto al puntero del raton
                cogerObjeto = True
        if event.type == MOUSEBUTTONUP:
            movRelativoX2, movRelativoY2 = pygame.mouse.get_pos()
            if movRelativoX2 - movRelativoX1 == 0 and movRelativoY2 - movRelativoY1 == 0:
                primerClick = True
            if segundoClick == True:
                primerClick = False
                segundoClick = False
            cogerObjeto = False
            

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                finalizarPrograma()
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                lluvia.pause()
            if event.key == pygame.K_o:
                lluvia.unpause()

            if event.key == pygame.K_a:
                soundLevel = lluvia.get_volume()
                soundLevel += 0.03
                if soundLevel > 1.0:
                    soundLevel = 1.0
                lluvia.set_volume(soundLevel)
                print (soundLevel)
            if event.key == pygame.K_z:
                soundLevel = lluvia.get_volume()
                soundLevel -= 0.03
                if soundLevel < 0.0:
                    soundLevel = 0.0
                lluvia.set_volume(soundLevel)
                print (soundLevel)
                

    # borrar la pantalla y
    # Establecer imagen (o un color) de fondo
    if fondoActivo == True:
        SCREEN.blit(imagen_Fondo, (0,0))
    else:
        SCREEN.fill(BACKGROUND_COLOR)


    # dibujar el contol de volumen
    for control_volumen in listaControles:
        control_volumen.draw(SCREEN)
        
    # Dibujar Etiquetas(y otros textos)
    dibujar_Textos('LLUVIA',  font20, COLOR_BLANCO_SUCIO, SCREEN, 10,  15, 0)
    dibujar_Textos('TRUENOS', font20, COLOR_BLANCO_SUCIO, SCREEN, 10,  65, 0)
    dibujar_Textos('VIENTO',  font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 115, 0)
    dibujar_Textos('FUEGO',   font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 165, 0) 
    dibujar_Textos('GRILLOS', font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 215, 0)
    dibujar_Textos('PAJAROS', font20, COLOR_BLANCO_SUCIO, SCREEN, 10, 265, 0)

    dibujar_Textos('GENERADOR DE SONIDO AMBIENTE',
                   font30, COLOR_AZUL_OSCURO, SCREEN, 0, 320, 3)
    dibujar_Textos('v0.2',
                   font35, COLOR_AZUL_OSCURO, SCREEN, 0, 360, 3)
   
    # Mover Objeto: Si hay objeto Focus seleccionado, moverlo
    if cogerObjeto == True:
        borde = False
        movRelativoX, movRelativoY = pygame.mouse.get_rel()
        posX, posY = pygame.mouse.get_pos()# posicion del raton mientras 'sujeta' un objeto
        focusRect.centerx = (posX-offsetX)
        # comprobar si el objeto rebasa los limites
        if focusRect.left < item.barraRect.left:
            focusRect.left = item.barraRect.left
            borde = True
        if focusRect.right > item.barraRect.right:
            focusRect.right = item.barraRect.right
            borde = True
        if borde == True:
            #pass
            pygame.mouse.set_pos(offsetX + focusRect.centerx, posY)
        item.cambiarVolumen()        
        
        
    

##    # Hacer una pausa si se pulsa la tecla designada para ello ('P')
##    if pausarPartida == True:
##        esperarPulsacionTeclado()


    pygame.display.update()
    # Control de tiempo del reloj del programa
    mainClock.tick(FPS)


