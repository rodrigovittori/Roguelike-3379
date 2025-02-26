#pgzero

"""
Version actual: [M7.L2] - Actividades Adicionales
Objetivo del ejercicio: Agregar condiciones de fin de juego
Tarea: Publicar el Juego en el HUB

NOTA: Este código también cumple con lo propuesto en la Activdad Extra "controles mejorados"

Pasos:
#1: Crear nuevas variables: una que controla el modo_actual
#2: Crear función que compruebe el fin de juego
#3: Llamar a la función que comprueba el fin de juego después de cada movimiento
#4: Modificar nuestro draw() para que en caso de "transición" nos muestre un mensaje indicando lo siguiente

=========================================================================================
Pack Kodland: https://kenney.nl/assets/roguelike-caves-dungeons (NO VIENE PRECORTADO)
Packs de assets: https://kenney.nl/assets/series:Tiny?sort=update (LO TIENEN QUE ESCALAR)
Pack escalado (drive del profe): https://drive.google.com/drive/folders/19obh4TK0RIBWlXOsaOq9uJ287jUHuLTn?usp=drive_link

> Para redimensionar assets https://imageresizer.com/bulk-resize/
"""

import random

# Ventana de juego hecha de celdas
celda = Actor('border') # Celda que voy a utilizar como referencia para mi mapa

""" ******************************************************************* """

# Paleta de terrenos:
pared =  Actor("border") # 0: Pared de bloques
piso =   Actor("floor")  # 1: Suelo liso (sin decoración)
crack =  Actor("crack")  # 2: Suelo resquebrajado/quebradizo
huesos = Actor("bones")  # 3: Suelo con una pilita de huesos

""" ******************************************************************* """

cant_celdas_ancho = 9 # Ancho del mapa (en celdas)
cant_celdas_alto = 10 # Altura del mapa (en celdas)

WIDTH =  celda.width  * cant_celdas_ancho # Ancho de la ventana (en píxeles)
HEIGHT = celda.height * cant_celdas_alto  # Alto de la ventana (en píxeles)

TITLE = "Rogue-like: Mazmorra Maldita" # Título de la ventana de juego
FPS = 30 # Número de fotogramas por segundo

""" ******************************************************************* """

# Personaje:
personaje = Actor("stand")
# Nota: si quieren llevar control de la vida, pueden crear dos atributos: "salud_max" y "salud_actual"
personaje.salud = 100
# Nota: si quieren hacer más interesante el combate pueden agregar atributos para el valor mínimo de ataque y el máximo
#       (también pueden implementar un sistema de miss y critical hits)
personaje.ataque = 5

# Corregimos spawn del Jugador:
personaje.top = celda.height
personaje.left = celda.width

""" ******************************************************************* """
################ VARIABLES ################

CANT_ENEMIGOS_A_SPAWNEAR = 5
colision = -2 # ¿XQ -2 como valor inicial?: porque es un valor que NO nos puede devolver collidelist.
modo_actual = "juego"
partida_finalizada = False # To-do: agregar variable para la habitación (no la partida)
resultado_partida = "jugando" # valores: "jugando"/"victoria"/"derrota"

# Listas
lista_enemigos = []
lista_bonus = []

""" ******************************************************************* """
################## GENERAR ENEMIGOS ##################

# To-Do: migrar a función
while (len(lista_enemigos) < CANT_ENEMIGOS_A_SPAWNEAR):
    x = (random.randint(2, cant_celdas_ancho - 2) * celda.width)
    y = (random.randint(2, cant_celdas_alto - 3) * celda.height)
    # To-Do: Agregar variable para determinar tipo de enemigo a spawnear
    
    nvo_enemigo = Actor("enemy", topleft = (x, y))

    # Validamos que los enemigos no spawneen uno sobre el otro
    posicion_duplicada = False
    for enemigo in lista_enemigos:
        if (nvo_enemigo.pos == enemigo.pos): # Si la posición de nvo_enemigo es IGUAL a la de CUALQUIER enemigo en la lista,
            posicion_duplicada = True        # Actualizamos la flag que indica que la posicion está duplicada
    if (posicion_duplicada):
        continue
    else:
        # Si NO hay conflicto: randomizamos salud, ataque y lo agregamos a lista_enemigos
        nvo_enemigo.salud = random.randint(10, 20)
        nvo_enemigo.ataque = random.randint(5, 10)
        nvo_enemigo.bonus = random.randint(0, 2) # 0: NADA / 1: curacion / 2: espadas
        lista_enemigos.append(nvo_enemigo)
        
################## MAPAS ##################

mapa =   [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 1, 2, 1, 3, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 0], 
          [0, 1, 3, 2, 1, 1, 3, 1, 0], 
          [0, 1, 1, 1, 1, 3, 1, 1, 0], 
          [0, 1, 1, 3, 1, 1, 2, 1, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1] ] # Fila extra para mostrar el texto

mapa_2 = [ [0, 0, 0, 0, 0, 0, 0, 0, 0], 
           [0, 1, 1, 1, 1, 1, 1, 1, 0], 
           [0, 1, 1, 3, 1, 3, 1, 1, 0], 
           [0, 1, 1, 3, 1, 3, 1, 1, 0], 
           [0, 1, 1, 1, 1, 1, 1, 1, 0], 
           [0, 3, 1, 1, 1, 1, 1, 3, 0], 
           [0, 1, 3, 1, 1, 1, 3, 1, 0], 
           [0, 1, 1, 3, 3, 3, 1, 1, 0], 
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [-1, -1, -1, -1, -1, -1, -1, -1, -1] ] # Fila extra para mostrar el texto


##########################################

mapa_actual = mapa # mapa a dibujar // cambiar valor si cambiamos de habitación

"""   #####################
     # FUNCIONES PROPIAS #
    #####################   """

def comprobar_fin_de_juego():
    global modo_actual, partida_finalizada, resultado_partida
    
    if (personaje.salud <= 0): # El personaje fue derrotado
        modo_actual = "transicion"
        partida_finalizada = True
        resultado_partida = "derrota"

    elif ((lista_enemigos == []) and (personaje.salud > 0)): # NOTA: tener en cuenta si se modifica el juego (bonus, transciciones, etc)
        modo_actual = "transicion"
        partida_finalizada = True
        resultado_partida = "victoria"

def dibujar_mapa(mapa):

  for fila in range(len(mapa)):
    for columna in range(len(mapa[fila])):

      """
      Lista códigos terrenos
      
      0: pared
      1: piso (sin nada)
      2: piso (roto/resquebrajado)
      3: piso (c/ huesitos)
      """

      if (mapa[fila][columna] == 0): # pared
        pared.left = pared.width * columna
        pared.top = pared.height * fila
        pared.draw()

      elif (mapa[fila][columna] == 1): # piso (sin nada)
        piso.left = piso.width * columna
        piso.top = piso.height * fila
        piso.draw()

      elif (mapa[fila][columna] == 2): # piso (roto/resquebrajado)
        crack.left = crack.width * columna
        crack.top = crack.height * fila
        crack.draw()

      elif (mapa[fila][columna] == 3): # piso (c/ huesitos)
        huesos.left = huesos.width * columna
        huesos.top = huesos.height * fila
        huesos.draw()
    
    # Agregar texto?


"""   #####################
     # FUNCIONES PG-ZERO #
    #####################   """

def draw():

    if (modo_actual == "juego"):
        screen.fill("#2f3542") # rgb = (47, 53, 66)
        dibujar_mapa(mapa_actual)
    
        for bonus in lista_bonus:
            bonus.draw()
    
        for enemigo in lista_enemigos:
            enemigo.draw()
        
        personaje.draw()
        
        # Mostramos valores personaje:
        screen.draw.text(("❤️: " + str(personaje.salud)), midleft=(30, (HEIGHT - int(celda.height/2))), color = 'white', fontsize = 24)
        screen.draw.text(("🗡️: " + str(personaje.ataque)), midright=((WIDTH - 30), (HEIGHT - int(celda.height/2))), color = 'white', fontsize = 24)
    

    elif (modo_actual == "transicion"):
        screen.fill("#2f3542")  # rgb = (47, 53, 66)
        
        if (partida_finalizada):
            if (resultado_partida == "victoria"):
                screen.draw.text("¡Ganaste!", center=(WIDTH/2, HEIGHT/3), color = 'white', fontsize = 46)
                screen.draw.text("Presiona [Espacio] para reiniciar", center=(WIDTH/2, HEIGHT/3 *2), color = 'white', fontsize = 24)
            else:
                screen.draw.text("¡Perdiste!", center=(WIDTH/2, HEIGHT/3), color = 'white', fontsize = 46)
                screen.draw.text("Presiona [Espacio] para reiniciar", center=(WIDTH/2, HEIGHT/3 *2), color = 'white', fontsize = 24)

            screen.draw.text("** Tienes que programar el reinicio de Juego** ", center=(WIDTH/2, HEIGHT/5 *4), color = 'yellow', fontsize = 18)
            
        else:
            # Partida NO-finalizada
            screen.draw.text("Entrando a la Sala: [NEXT]", center=(WIDTH/2, HEIGHT/3), color = 'white', fontsize = 46)
            screen.draw.text("Presiona [Espacio] para reiniciar", center=(WIDTH/2, HEIGHT/3 *2), color = 'white', fontsize = 24)
    
def on_key_down(key):

  global colision

  pos_previa = personaje.pos # Posición previa a pulsar la tecla
  
  if ((keyboard.right or keyboard.d) and (personaje.x < (WIDTH - celda.width * 2))):
    # ¿Xq 2?: Una (a la que me voy a desplazar) y otra (por la pared, que NO puedo atravesar)
    personaje.x += celda.width
    personaje.image = "stand" # xq stand mira a la dcha
        
  elif ((keyboard.left or keyboard.a) and (personaje.x > (celda.width * 2))):
    personaje.x -= celda.width
    personaje.image = "left" # xq mira a la izq
        
  elif ((keyboard.down or keyboard.s) and (personaje.y < HEIGHT - celda.height * 3)):
    # ¿Xq 3?: Una (a la que me voy a desplazar), otra (por la pared, que NO puedo atravesar) Y UNA TERCERA (para mostrar el texto)
    personaje.y += celda.height
    
  elif ((keyboard.up or keyboard.w) and (personaje.y > (celda.height * 2))):
        personaje.y -= celda.height

  ################## COLISIONES ##################

  colision = personaje.collidelist(lista_enemigos)

  if (colision != -1):
      # Si hubo colisión con un enemigo:

      # Paso 1: Calculamos daños
      enemigo_atacado = lista_enemigos[colision]
      enemigo_atacado.salud -= personaje.ataque
      personaje.salud -= enemigo_atacado.ataque
      # Nota: Podríamos agrgar un sistema de puntos de daño flotantes en pantalla

      # Paso 2: Volvemos al personaje a su posición anterior:
      personaje.pos = pos_previa
      
      # Si el enemigo se quedó sin puntos de salud, lo eliminamos:
      if (enemigo_atacado.salud <= 0):
          
          # ANTES DE DESTRUÍRLO/ELIMINARLO -> Spawneamos bonus:
          if (enemigo_atacado.bonus == 0):
              # NADA
              enemigo_atacado.bonus += 0 # TENGO que poner algo para que python NO devuelva error
              
          elif (enemigo_atacado.bonus == 1):
              # Spawneamos curación:
              nvo_bonus = Actor("heart", enemigo_atacado.pos)    # Spawneo un nuevo bonus en la posición del enemigo derrotado
              lista_bonus.append(nvo_bonus)                      # Lo agrego a la lista de bonus

          elif (enemigo_atacado.bonus == 2):
              # Spawneamos mejora ataque:
              nvo_bonus = Actor("sword", enemigo_atacado.pos)    # Spawneo un nuevo bonus en la posición del enemigo derrotado
              lista_bonus.append(nvo_bonus)                      # Lo agrego a la lista de bonus

          # Ya creado el bonus, bye bye~♥
          
          # Método Nº 1: pop() con índice según colision
          #lista_enemigos.pop(colision)

          # Método Nº 2: remove(enemigo_atacado)
          lista_enemigos.remove(enemigo_atacado)

          # To-do: modificar la casilla / spawnear una pila de huesitos donde muere el esqueleto
  
  else: #Si NO hay colisión con enemigos...
      
      """ >>> COLISIONES CON BONUS <<< """

      if (personaje.collidelist(lista_bonus) != -1):

          # identificamos el bonus que hemos encontrado:
          bonus_encontrado = lista_bonus[personaje.collidelist(lista_bonus)]

          if (bonus_encontrado.image == "heart"):
              # Si es una CURACIÓN:
              personaje.salud += 15
          
          elif (bonus_encontrado.image == "sword"):
              # Si es un bonus de ATAQUE:
              personaje.ataque += 5

          # Ya aplicado el efecto, eliminamos el bonus:
          lista_bonus.remove(bonus_encontrado)
          
  comprobar_fin_de_juego()