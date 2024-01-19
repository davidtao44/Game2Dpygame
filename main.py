#Juego 2D sencillo, donde el objetivo es eliminar la mayor cantidad de enemigos posible
#Este contiene un menu de pausa y un limitador de disparos para nivelar el juego, consta con la visualizacion de su vida
#visualizacion de los disparos y el puntaje.
#Hecho por David Esteban Gonzalez Becerra
import sys
import pygame, random

# Inicializamos pygame
pygame.init()

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

#Se crea la ventana donde se desarrollara el juego
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GAME-OPENDG")


# variables globales
white = ((255, 255, 255))
black = (0, 0, 0)
fondo = pygame.image.load("imagenes/fondo.png")
run = True  # si run es verdadero entrara al while y se ejecutara el juego 
character_speed = 5  # Velocidad de movimiento del personaje
pausa = False # variable para el menu de pausa
velocidad_FPS = 30
selector_test = 0
posicion_x,posicion_y = 385,200 #posicion inicial del selector de velocidades, (menu de pausa seccion opciones)
vida_personaje = 100
contador_disparos = 0 #inicializacion
time = 0  #recarga de disparos
ciclos_sin_disparar = 100 #Se lleva el tiempo o ciclos sin disparar
puntaje_maximo = 100
contador_enemigos = 0 #contador de enemigos eliminados


#Se crea un objeto para el personaje y se crea su rectangulo
character = pygame.image.load("imagenes/main_character.png")
character_rect = character.get_rect()
#Posicion  inicial del personaje 
character_rect.move_ip((width//2)-35, (height//2)-50) 
'''(width//2)-35, (height//2)-50, esto ya que la posicion la cuenta desde la parte superior izquierda, 
entonces teniendo encuenta las dimensiones de la imagen(70x100), se tienen encuentan esos px
por ejemplo para ubicar el personaje en la seccion central'''


#creacion de botones menu pausa
boton_continuar = pygame.image.load("imagenes/Botones/Continuar.png")
boton_continuar_rect = boton_continuar.get_rect()
boton_continuar_rect.move_ip((width//2)-80, (height//2)-70) 
boton_opciones = pygame.image.load("imagenes/Botones/opciones.png")
boton_opciones_rect = boton_continuar.get_rect()
boton_opciones_rect.move_ip((width//2)-60, (height//2)-10) 
boton_salir = pygame.image.load("imagenes/Botones/salir.png")
boton_salir_rect = boton_continuar.get_rect()
boton_salir_rect.move_ip((width//2)-80, (height//2)+50) 
velocidad_juego = pygame.image.load("imagenes/Botones/velocidad_juego.png")
velocidad_juego_rect = velocidad_juego.get_rect()
velocidad_juego_rect.move_ip(0, 0) 
#variables para el testigo de pausa
testigo_pausa = pygame.image.load("imagenes/pausa.png")
testigo_pausa_rect = testigo_pausa.get_rect()
testigo_pausa_rect.move_ip(550,0)
#variables para los disparos
shot = pygame.image.load("imagenes/disparo.png")
shot_rect = shot.get_rect()
shot_speed = 10  # Velocidad del disparo
shots = []  # Lista para almacenar los disparos


#funciones 
#Funcion para el moviento del personaje a travez de la ventana
def movimiento_personaje(keys):

    global character_rect,width,height

    if keys[pygame.K_UP]:
        character_rect = character_rect.move(0, -character_speed)
    elif keys[pygame.K_DOWN]:
        character_rect = character_rect.move(0, character_speed)
    elif keys[pygame.K_RIGHT]:
        character_rect = character_rect.move(character_speed, 0)
    elif keys[pygame.K_LEFT]:
        character_rect = character_rect.move(-character_speed, 0)
    #Para que el personaje no supere los bordes de la ventana, usando min() y max()
    character_rect.left = max(0, character_rect.left)
    character_rect.right = min(width, character_rect.right)
    character_rect.top = max(0, character_rect.top)
    character_rect.bottom = min(height, character_rect.bottom)

#Funcion para que el personaje no atravieze objetos colocados en la ventana
def colicion_personajeObjeto(personaje_rect, objeto_rect):

    if personaje_rect.colliderect(objeto_rect):
        # Colisión con el lado izquierdo del objeto
        if personaje_rect.right > objeto_rect.left and personaje_rect.left < objeto_rect.left:
            personaje_rect.right = objeto_rect.left

       # Colisión con el lado derecho del objeto
        elif personaje_rect.left < objeto_rect.right and personaje_rect.right > objeto_rect.right:
            personaje_rect.left = objeto_rect.right

       # Colisión en la parte inferior del objeto
        elif personaje_rect.top < objeto_rect.bottom and personaje_rect.bottom > objeto_rect.bottom:
            personaje_rect.top = objeto_rect.bottom

        # Colisión en la parte superior del objeto
        elif personaje_rect.bottom > objeto_rect.top and personaje_rect.top < objeto_rect.top:
            personaje_rect.bottom = objeto_rect.top

#Funcion para la colicion entre el personaje y enemigo
def colicion_personajeEnemigo(personaje_rect, objeto_rect):
    global vida_personaje

    if personaje_rect.colliderect(objeto_rect):
        # Colisión con el lado izquierdo del objeto
        if personaje_rect.right > objeto_rect.left and personaje_rect.left < objeto_rect.left:
            personaje_rect.right = objeto_rect.left
            actualizar_vida()

       # Colisión con el lado derecho del objeto
        elif personaje_rect.left < objeto_rect.right and personaje_rect.right > objeto_rect.right:
            personaje_rect.left = objeto_rect.right
            actualizar_vida()

       # Colisión en la parte inferior del objeto
        elif personaje_rect.top < objeto_rect.bottom and personaje_rect.bottom > objeto_rect.bottom:
            personaje_rect.top = objeto_rect.bottom
            actualizar_vida()

        # Colisión en la parte superior del objeto
        elif personaje_rect.bottom > objeto_rect.top and personaje_rect.top < objeto_rect.top:
            personaje_rect.bottom = objeto_rect.top
            actualizar_vida()     


#Funcion para disparar
def disparar():
    x = character_rect.centerx  # La posición x del disparo es el centro del personaje
    y = character_rect.centery  # La posición y del disparo es el centro del personaje
    Nuevoshot_rect = shot.get_rect() #Se crea un nuevo rectangulo para cada disparo   
    shots.append(Nuevoshot_rect)
    Nuevoshot_rect.move_ip(x, y)
    
#funcion para la creación de la barra de vida 
def barraVida(ruta_imagen, x, y):
    imagen = pygame.image.load(ruta_imagen)
    rect = imagen.get_rect()
    rect.move_ip(x, y)
    return imagen, rect

#Se reutiliza la funcion barraVida en los siguientes casos
#funcion graficar n° de balas 
graficarmunicion = barraVida
#Funcion para crear objetos en el juego 
Objetos_obstaculo = barraVida
#Funcion para crear distintos caminos en el juego
cargar_camino = barraVida
#Funcion para crear barra de carga municion
barra_Carga_Municion = barraVida
#Funcion para crear variables para visualizar el puntaje en pantalla
graficarpuntaje = barraVida

#Funcion para el texto de la puntuacion
def textoPuntuacion (frame, text, size, x, y):
    font = pygame.font.SysFont('CascadiaCode', size, bold = False)
    text_frame = font.render(text, False, black, None)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x,y)
    frame.blit(text_frame, text_rect)

#Funcion para la creacion de enemigos
def crear_enemigo():
    x = 650 
    y = random.randint(0, height - 50)  # La altura máxima que puede apareces el enemigo
    enemigo = pygame.image.load("imagenes/enemigo1.png")
    enemigo_rect = enemigo.get_rect()
    enemigo_rect.move_ip(x, y)
    return enemigo, enemigo_rect

#Para disminuir la vida del jugador por cada vez que el enemigo colicione contra el, se encuentra en la funcion colicion_personajeEnemigo
def actualizar_vida():
    global vida_personaje
    vida_personaje -= 1 
    if vida_personaje <= 0:
        print("Game Over")  
        pygame.quit()
        sys.exit()
#Funcion para entrar al menu de pausa, ya que pasa de False a True la variable pausa 
def toggle_pausa():
    global pausa
    pausa = not pausa


           
#Se crea una lista de los objetos-obstaculo
Objetos_obstaculo_lista = [
    Objetos_obstaculo("imagenes/casa1.png",width//2-200,height//2-125),
    Objetos_obstaculo("imagenes/casa1.png",550,175),
    Objetos_obstaculo("imagenes/Arbol_pequeño.png",0,0),
    Objetos_obstaculo("imagenes/Arbol_pequeño.png",200,0),
    Objetos_obstaculo("imagenes/Arbol_pequeño.png",400,0),
    Objetos_obstaculo("imagenes/Arbol_pequeño.png",600,0),
    Objetos_obstaculo("imagenes/Roca.png",0,300),
    Objetos_obstaculo("imagenes/Roca.png",0,350)
]
#Se crea una lista para la visualizacion de "caminos"
caminos = [
    cargar_camino("imagenes/camino_horizontal.png", 200, 92),
    cargar_camino("imagenes/camino_horizontal.png", 200, 491),
    cargar_camino("imagenes/camino_horizontal.png", 555, 92),
    cargar_camino("imagenes/camino_horizontal.png", 553, 491),
    cargar_camino("imagenes/camino_horizontal.png", -50, 92),
    cargar_camino("imagenes/camino_horizontal.png", -50, 491),
    cargar_camino("imagenes/camino_vertical.png", 56, 265),
    cargar_camino("imagenes/camino_vertical.png", 409, 265),
    cargar_camino("imagenes/camino_vertical.png", 765, 265),
    cargar_camino("imagenes/camino_interseccion.png", 25, 440),
    cargar_camino("imagenes/camino_interseccion.png", 378, 440),
    cargar_camino("imagenes/camino_interseccion.png", 733, 440),
    cargar_camino("imagenes/camino_tee.png", 25, 89),
    cargar_camino("imagenes/camino_tee.png", 378, 89),
    cargar_camino("imagenes/camino_tee.png", 733, 89),
]

#Lista para la visualizacion de las barras de vida 
barra_Vida = [barraVida("imagenes/barravida/BarraVida_player.png", 0, 0),
              barraVida("imagenes/barravida/BarraVida_player_75.png", 0, 0),
              barraVida("imagenes/barravida/BarraVida_player_50.png", 0, 0),
              barraVida("imagenes/barravida/BarraVida_player_25.png", 0, 0),
              barraVida("imagenes/barravida/BarraVida_player_0.png", 0, 0)]

#Lista para la visualizacion de la "municion" disponible
Municion = [graficarmunicion("imagenes/Municion/Full.png", 0, 520),
            graficarmunicion("imagenes/Municion/3.png", 0, 520),
            graficarmunicion("imagenes/Municion/2.png", 0, 520),
            graficarmunicion("imagenes/Municion/1.png", 0, 520),
            graficarmunicion("imagenes/Municion/0.png", 0, 520)]

#Lista para la visualizacion de la barra de carga de la municion
barra_Carga = []
for i in range(ciclos_sin_disparar):
    barra_Carga.append(barra_Carga_Municion("imagenes/carga_municion.png",4*i,570))


#Lista que  va almacenando cada uno de los enemigos "creados"
enemigos = []

#Ejecución del juego 
while run:
    #captura de los eventos que se han producido en los perifericos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                toggle_pausa()
            elif event.key == pygame.K_SPACE:
                disparar()
                contador_disparos += 1 
                       

    if not pausa:    
        
        # Limpiamos la pantalla
        screen.fill(white)
        

        # Agregar la creación de enemigos con cierta probabilidad
        if random.randint(0, 100) < 7:  # Probabilidad del 7%
            enemigos.append(crear_enemigo())

        # Capturamos las teclas presionadas
        keys = pygame.key.get_pressed()

        # Llama a la función para manejar el movimiento del personaje
        movimiento_personaje(keys)  
    
        # Redimensiona la imagen de fondo al tamaño de la ventana
        fondo_redimensionado = pygame.transform.scale(fondo, (width, height))

        # Dibuja el fondo redimensionado
        screen.blit(fondo_redimensionado, (0, 0))
        
        #para visualizar objetos del mapa
        for camino_img, camino_rect in caminos:
            screen.blit(camino_img, camino_rect)
        
        for objeto_img, objeto_rect in Objetos_obstaculo_lista:
            screen.blit(objeto_img, objeto_rect)

        for objeto_mapa in Objetos_obstaculo_lista:
            colicion_personajeObjeto(character_rect, objeto_mapa[1])
            for enemigo_img, enemigo_rect in enemigos:
                colicion_personajeObjeto(enemigo_rect,objeto_mapa[1])

        # Para visualizar enemigos
        for enemigo_img, enemigo_rect in enemigos:
            screen.blit(enemigo_img, enemigo_rect)

        # Para la visualizacion del personaje
        screen.blit(character,character_rect)

        # Actualizar la posición de los enemigos
        for enemigo_img, enemigo_rect in enemigos:
            enemigo_rect.move_ip(-5, random.randint(-5,5))  # Ajusta la velocidad del enemigo según sea necesario, la posicion en Y va variando aleatoriamente
        
        # Colisión con el enemigo
            colicion_personajeEnemigo(character_rect,enemigo_rect)    

        # Elimina enemigos que salen de la pantalla
            if enemigo_rect.right > width:     
                enemigos.remove((enemigo_img, enemigo_rect))

        #Configuracion de la barra de vida respecto a la vida del personaje
        if vida_personaje <= 100 and vida_personaje >= 90:
            screen.blit(barra_Vida[0][0],barra_Vida[0][1])
        elif vida_personaje <=90 and vida_personaje >= 60:
            screen.blit(barra_Vida[1][0],barra_Vida[1][1])
        elif vida_personaje <=60 and vida_personaje >= 40:
            screen.blit(barra_Vida[2][0],barra_Vida[2][1])
        elif vida_personaje <=40 and vida_personaje >= 20:
            screen.blit(barra_Vida[3][0],barra_Vida[3][1])
        elif vida_personaje <=20 and vida_personaje >= 0:
            screen.blit(barra_Vida[4][0],barra_Vida[4][1])  
        
    
        shots_to_remove = []  #Se agregan aqui los disparos que salen de la pantalla o que colicionan con un enemigo
        if contador_disparos <= 4:  #Para limitar la cantidad de disparos a 4
            
            #se grafican los disparos que le quedan al jugador 
            if contador_disparos == 0:
                screen.blit(Municion[0][0],Municion[0][1]) 
            elif contador_disparos == 1:
                screen.blit(Municion[1][0],Municion[1][1])
            elif contador_disparos == 2:
                screen.blit(Municion[2][0],Municion[2][1])
            elif contador_disparos == 3:
                screen.blit(Municion[3][0],Municion[3][1])
            elif contador_disparos == 4:
                screen.blit(Municion[4][0],Municion[4][1])

            for shot_rect in shots:
                screen.blit(shot, shot_rect)
                shot_rect.move_ip(shot_speed, 0)  # Mueve el disparo hacia la derecha

                # Verifica colisiones con los enemigos
                remove_shot = False
                for enemigo_img, enemigo_rect in enemigos:
                    # Verifica que enemigo_rect tenga coordenadas numéricas válidas
                    if isinstance(enemigo_rect.x, (int, float)) and isinstance(enemigo_rect.y, (int, float)):
                        if shot_rect.colliderect(enemigo_rect): #entra si el disparo a colicionado con un enemigo
                            enemigos.remove((enemigo_img, enemigo_rect))
                            remove_shot = True
                            contador_enemigos += 1
                            break  # Sale del bucle al colisionar con un enemigo

                # Verifica si el disparo sale de la pantalla
                if shot_rect.left > width:
                    remove_shot = True
                #se agrega a la lista shots_to_remove
                if remove_shot:
                    shots_to_remove.append(shot_rect)

        else:

            #grafica "0 municion"
            screen.blit(Municion[4][0],Municion[4][1])

            #barra de carga munición
            visualizacion_barra = []
            for j in range(time):
               visualizacion_barra.append(screen.blit(barra_Carga[j][0],barra_Carga[j][1]))

            #Se incrementa la variable time, tiempo que dura el personaje sin munición  
            time += 1
            #determina el "tiempo" para volver disparar en el juego
            if time > ciclos_sin_disparar:
                    contador_disparos = 0
                    time = 0
            shots.clear() #se eliminan todos los elementos de la lista que guardan los disparos en juego

        #Se grafica el puntaje
        textoPuntuacion(screen, (' Puntaje: '+ str(contador_enemigos)+ '     '), 25 , width-70, 550)
        
        #Elimina los disparos que salen de la pantalla y han colisionado con enemigos
        for shot_rect in shots_to_remove:
            shots.remove(shot_rect)

        #Para visualizar el testigo de pausa            
        screen.blit(testigo_pausa, testigo_pausa_rect)
 
        # Actualizamos la pantalla
        pygame.display.flip()

    #Menu de pausa
    else:

        # Limpiamos la pantalla
        screen.fill(black)
        # Capturamos las teclas del mouse y su posicion
        mouse_posicion = pygame.mouse.get_pos()
        #print(mouse_posicion)
        mouse_key = pygame.mouse.get_pressed()
        

        #boton continuar
        if mouse_posicion[0] > 320 and mouse_posicion[0] < 454 and mouse_posicion[1] > 229 and mouse_posicion[1] < 270:
            if mouse_key[0]:
               toggle_pausa()  #cambia el valor de la variable pausa para retornar al juego la cambia de true a false.

        #boton opciones
        elif mouse_posicion[0] > 340 and mouse_posicion[0] < 432 and mouse_posicion[1] > 290 and mouse_posicion[1] < 330:
            while mouse_key[0]:
                #captura de teclas teclado
                key_p = pygame.key.get_pressed()
                # Capturamos las teclas del mouse y su posicion
                mouse_posicion_opciones = pygame.mouse.get_pos()
                mouse_key_opciones = pygame.mouse.get_pressed()
                

                #Se limpia pantalla        
                screen.fill(black)

                #carga del fondo de la ventana opciones
                screen.blit(velocidad_juego,velocidad_juego_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                if key_p[pygame.K_r]:   #para romper el ciclo while y volver al menu principal de pausa
                    print(key_p[pygame.K_r])
                    break
                #"velocidades (FPS)"

                #velocidad baja
                elif mouse_posicion_opciones[0] > 195 and mouse_posicion_opciones[0] < 236 and mouse_posicion_opciones[1] > 217 and mouse_posicion_opciones[1] < 256:
                    if mouse_key_opciones[0]:
                        velocidad_FPS = 15
                        posicion_x,posicion_y = 200,200
                        #print(mouse_posicion_opciones)
                #velocidad media
                elif mouse_posicion_opciones[0] > 378 and  mouse_posicion_opciones[0] < 420 and mouse_posicion_opciones[1] > 217 and mouse_posicion_opciones[1] < 255:
                    if mouse_key_opciones[0]:
                        velocidad_FPS = 30
                        posicion_x,posicion_y = 385,200
                #velocidad alta
                elif mouse_posicion_opciones[0] > 565 and mouse_posicion_opciones[0] < 607 and mouse_posicion_opciones[1] > 217 and mouse_posicion_opciones[1] < 255 :
                    if mouse_key_opciones[0]:
                        velocidad_FPS = 50
                        posicion_x,posicion_y = 570,200
                
                selector = pygame.image.load("imagenes/Botones/seleccion.png") #imagen selector
                selector_rect = selector.get_rect()
                selector_rect.move_ip(posicion_x,posicion_y)  #posicion segun el campo de velocidad seleccionado
                screen.blit(selector,selector_rect)
                #actualizamos la pantalla
                pygame.display.flip()
        
        #boton salir
        elif mouse_posicion[0] > 320 and mouse_posicion[0] < 455 and mouse_posicion[1] > 350 and mouse_posicion[1] < 388:
            if mouse_key[0]:
                #print(mouse_posicion)
                pygame.quit()
                sys.exit()


        #print(pygame.mouse.get_pressed())
       
        screen.blit(boton_continuar,boton_continuar_rect)
        screen.blit(boton_opciones,boton_opciones_rect)
        screen.blit(boton_salir,boton_salir_rect)

        # Actualizamos la pantalla
        pygame.display.flip()


    # Establecemos la velocidad del juego
    clock.tick(velocidad_FPS)

pygame.quit()
sys.exit()
