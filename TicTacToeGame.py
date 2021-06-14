import pygame
import math
import random

pygame.init()
WIDTH = 500
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Las imágenes están en la carpeta images, sin embargo, para que el programa ejecute, esa dirección dependerá
#de dónde haya descargado el archivo

X_IMAGE = pygame.transform.scale(pygame.image.load("C:/Users/USUARIO\Desktop/u201718420_u201416126_u201514555/Tic-Tac-Toe/Images/x.png"), (150, 150))
O_IMAGE = pygame.transform.scale(pygame.image.load("C:/Users/USUARIO\Desktop/u201718420_u201416126_u201514555/Tic-Tac-Toe/Images/o.png"), (150, 150))
END_FONT = pygame.font.SysFont('courier', 40)

#Función para dibujar la matriz en pygame
def dibujarMatriz():
    espacios = WIDTH // ROWS
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * espacios
        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

#Inicializar la representación del tablero con una matriz
def Inicializar():
    distanciaAlCentro = WIDTH // ROWS // 2
    matriz_juego = [[None, None, None], [None, None, None], [None, None, None]]

    #crear matriz vacía
    for i in range(len(matriz_juego)):
        for j in range(len(matriz_juego[i])):
            x = distanciaAlCentro * (2 * j + 1)
            y = distanciaAlCentro * (2 * i + 1)
            matriz_juego[i][j] = (x, y, "", True)

    return matriz_juego

#Turno del jugador
def AccionJugador(matriz_juego):
    global turnoDeX, turnoDeO, imagenes, posicion
    m_x, m_y = pygame.mouse.get_pos()
    for i in range(len(matriz_juego)):
        for j in range(len(matriz_juego[i])):
            x, y, char, clickValido = matriz_juego[i][j]
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2) #verificar que el click sea dentro de la ventana
            if clickValido:
                if turnoDeO and dis < WIDTH // ROWS // 2:
                    imagenes.append((x, y, O_IMAGE))
                    turnoDeX = True #Cambio de turno
                    turnoDeO = False #Cambio de turno
                    print(posicion)
                    matriz_juego[i][j] = (x, y, 'o', False)
                    #Si el usuario jugó en una esquina
                    if (x == 83 and y == 83) or (x == 415 and y == 83) or (x == 83 and y == 415) or (x == 415 and y == 415):
                        posicion = "Corner"
                        return posicion
                    #Si el usuario jugó en un borde
                    if (x == 249 and y == 83) or (x == 83 and y == 249) or (x == 415 and y == 249) or (x == 249 and y == 415):
                        posicion = "Edge"
                        return posicion
                    #Si el usuario jugó en el centro
                    if x == 249 and y == 249:
                        posicion = "Center"
                        return posicion
    return posicion

#Turno del sistema experto
def PcTurn(matriz_juego):
    global turnoDeX, turnoDeO
    if turnoDeX:
        turnoDeX = False
        turnoDeO = True
        return Conditions(matriz_juego, posicion)

#Función para detectar quién está a punto de ganar,
#recibe el tablero y el símbolo, 'x' u 'o'.
def IsAboutToWin(matriz_juego, symbol):
    #primera fila
    if matriz_juego[0][0][2] == symbol and matriz_juego[0][1][2] == symbol and matriz_juego[0][2][3] == True:
        return (415, 83, 0, 2, True) #Retornar las coordenadas en la ventana, la posición en la matriz, y verdadero
    if matriz_juego[0][0][2] == symbol and matriz_juego[0][1][3] == True and matriz_juego[0][2][2] == symbol:
        return (249, 83, 0, 1, True)
    if matriz_juego[0][0][3] == True and matriz_juego[0][1][2] == symbol and matriz_juego[0][2][2] == symbol:
        return (83, 83, 0, 0, True)
    
    #segunda fila
    if matriz_juego[1][0][2] == symbol and matriz_juego[1][1][2] == symbol and matriz_juego[1][2][3] == True:
        return (415, 249, 1, 2, True)
    if matriz_juego[1][0][2] == symbol and matriz_juego[1][1][3] == True and matriz_juego[1][2][2] == symbol:
        return (249, 249, 1, 1, True)
    if matriz_juego[1][0][3] == True and matriz_juego[1][1][2] == symbol and matriz_juego[1][2][2] == symbol:
        return (83, 249, 1, 0, True)

    #tercera fila
    if matriz_juego[2][0][2] == symbol and matriz_juego[2][1][2] == symbol and matriz_juego[2][2][3] == True:
        return (415, 415, 2, 2, True)
    if matriz_juego[2][0][2] == symbol and matriz_juego[2][1][3] == True and matriz_juego[2][2][2] == symbol:
        return (249, 415, 2, 1, True)
    if matriz_juego[2][0][3] == True and matriz_juego[2][1][2] == symbol and matriz_juego[2][2][2] == symbol:
        return (83, 415, 2, 0, True)

    #primera columna
    if matriz_juego[0][0][2] == symbol and matriz_juego[1][0][2] == symbol and matriz_juego[2][0][3] == True:
        return (83, 415, 2, 0, True)
    if matriz_juego[0][0][2] == symbol and matriz_juego[1][0][3] == True and matriz_juego[2][0][2] == symbol:
        return (83, 249, 1, 0, True)
    if matriz_juego[0][0][3] == True and matriz_juego[1][0][2] == symbol and matriz_juego[2][0][2] == symbol:
        return (83, 83, 0, 0, True)

    #segunda columna
    if matriz_juego[0][1][2] == symbol and matriz_juego[1][1][2] == symbol and matriz_juego[2][1][3] == True:
        return (249, 415, 2, 1, True)
    if matriz_juego[0][1][2] == symbol and matriz_juego[1][1][3] == True and matriz_juego[2][1][2] == symbol:
        return (249, 249, 1, 1, True)
    if matriz_juego[0][1][3] == True and matriz_juego[1][1][2] == symbol and matriz_juego[2][1][2] == symbol:
        return (249, 83, 0, 1, True)

    #tercera columna
    if matriz_juego[0][2][2] == symbol and matriz_juego[1][2][2] == symbol and matriz_juego[2][2][3] == True:
        return (415, 415, 2, 2, True)
    if matriz_juego[0][2][2] == symbol and matriz_juego[1][2][3] == True and matriz_juego[2][2][2] == symbol:
        return (415, 249, 1, 2, True)
    if matriz_juego[0][2][3] == True and matriz_juego[1][2][2] == symbol and matriz_juego[2][2][2] == symbol:
        return (415, 83, 0, 2, True)

    #primera diagonal
    if matriz_juego[0][0][2] == symbol and matriz_juego[1][1][2] == symbol and matriz_juego[2][2][3] == True:
        return (415, 415, 2, 2, True)
    if matriz_juego[0][0][2] == symbol and matriz_juego[1][1][3] == True and matriz_juego[2][2][2] == symbol:
        return (249, 249, 1, 1, True)
    if matriz_juego[0][0][3] == True and matriz_juego[1][1][2] == symbol and matriz_juego[2][2][2] == symbol:
        return (83, 83, 0, 0, True)

    #segunda diagonal
    if matriz_juego[0][2][2] == symbol and matriz_juego[1][1][2] == symbol and matriz_juego[2][0][3] == True:
        return (83, 415, 2, 0, True)
    if matriz_juego[0][2][2] == symbol and matriz_juego[1][1][3] == True and matriz_juego[2][0][2] == symbol:
        return (249, 249, 1, 1, True)
    if matriz_juego[0][2][3] == True and matriz_juego[1][1][2] == symbol and matriz_juego[2][0][2] == symbol:
        return (415, 83, 0, 2, True)

    #Si nadie está a punto de ganar
    return (-1,-1,-1,-1, False)

def AllCornersOccupied(matriz_juego):
    #Validamos que todas las esquinas estén ocupadas
    if matriz_juego[0][0][3] == False and matriz_juego[0][2][3] == False and matriz_juego[2][0][3] == False and matriz_juego[2][2][3] == False:
        return True

def AllEdgesOccupied(matriz_juego):
    #Validamos que todos los bordes estén ocupados
    if matriz_juego[0][1][3] == False and matriz_juego[1][0][3] == False and matriz_juego[1][2][3] == False and matriz_juego[2][1][3] == False:
        return True

def CenterOccupied(matriz_juego):
    #Validamos que el centro esté ocupado
    if matriz_juego[1][1][3] == False:
        return True

#Poner una X en el borde
def PlaceXinEdge(matriz_juego):
    if AllEdgesOccupied(matriz_juego):
        PlaceXinCorner(matriz_juego)
    else:
        if matriz_juego[0][1][3] == True:
            matriz_juego[0][1] = (249,83,'x', False)
            imagenes.append((249, 93, X_IMAGE))
            return matriz_juego
        if matriz_juego[1][0][3] == True:
            matriz_juego[1][0] = (83,249,'x',False)
            imagenes.append((83, 249, X_IMAGE))
            return matriz_juego
        if matriz_juego[1][2][3]:
            matriz_juego[1][2] = (415,249,'x',False)
            imagenes.append((415, 249, X_IMAGE))
            return matriz_juego
        if matriz_juego[2][1][3]:
            matriz_juego[2][1] = (249,415,'x',False)
            imagenes.append((249, 415, X_IMAGE))
            return matriz_juego
    return matriz_juego

#Poner X en el centro
def PlaceXinCenter(matriz_juego):
    if matriz_juego[1][1][3] == True:
        matriz_juego[1][1]=(249,249,'x',False)
        imagenes.append((249, 249, X_IMAGE))
    else:
        PlaceXinEdge(matriz_juego)
    return matriz_juego

#Poner X en la esquina
def PlaceXinCorner(matriz_juego):
    if AllCornersOccupied(matriz_juego):
        PlaceXinEdge(matriz_juego)
    else:
        if matriz_juego[0][0][3] == True:
            matriz_juego[0][0] = (83,83,'x',False)
            imagenes.append((83, 83, X_IMAGE))
            return matriz_juego
        if matriz_juego[2][2][3] == True:
            matriz_juego[2][2] = (415,415,'x',False)
            imagenes.append((415, 415, X_IMAGE))
            return matriz_juego
        if matriz_juego[0][2][3] == True:
            matriz_juego[0][2] = (415,83,'x',False)
            imagenes.append((415, 83, X_IMAGE))
            return matriz_juego
        if matriz_juego[2][0][3] == True:
            matriz_juego[2][0] = (83,415,'x',False)
            imagenes.append((83, 415, X_IMAGE))
            return matriz_juego
    return matriz_juego

#Poner X en un lugar dado
#Esta función la usamos cuando el usuario está a punto de ganar
def PlaceXIn(matriz_juego, x, y, i, j):
    matriz_juego[i][j] = (x, y, 'x', False)
    imagenes.append((x, y, X_IMAGE))
    return matriz_juego

#Sistema experto
def Conditions(matriz_juego, posicion):
    data = IsAboutToWin(matriz_juego, 'x')
    if data[4] == True:
        print("La pc está a punto de ganar")
        return PlaceXIn(matriz_juego, data[0], data[1], data[2], data[3]) #Bloqueamos la posible victoria del usuario
    data_human = IsAboutToWin(matriz_juego, 'o')
    if data_human[4] == True:
        print("El humano está a punto de ganar")
        return PlaceXIn(matriz_juego, data_human[0], data_human[1], data_human[2], data_human[3])
    else:
        if posicion == "Empty":
            return PlaceXinCorner(matriz_juego)
        else:
            if posicion == "Edge":
               return PlaceXinCenter(matriz_juego)
            if posicion == "Corner":
               return PlaceXinCorner(matriz_juego)
            if posicion == "Center":
               return PlaceXinCorner(matriz_juego)

#Si cualquiera de los dos está a punto de ganar
def AnyVictory(matriz_juego):
    for row in range(len(matriz_juego)):
        if (matriz_juego[0][0][2] == matriz_juego[0][1][2] == matriz_juego[0][2][2]) and matriz_juego[0][0][2] != "":
            MostrarMensaje(matriz_juego[0][0][2].upper() + " ha ganado!")
            return True

    for row in range(len(matriz_juego)):
        if (matriz_juego[1][0][2] == matriz_juego[1][1][2] == matriz_juego[1][2][2]) and matriz_juego[1][0][2] != "":
            MostrarMensaje(matriz_juego[1][0][2].upper() + " ha ganado!")
            return True

    for row in range(len(matriz_juego)):
        if (matriz_juego[2][0][2] == matriz_juego[2][1][2] == matriz_juego[2][2][2]) and matriz_juego[2][0][2] != "":
            MostrarMensaje(matriz_juego[2][0][2].upper() + " ha ganado!")
            return True

    for col in range(len(matriz_juego)):
        if (matriz_juego[0][0][2] == matriz_juego[1][0][2] == matriz_juego[2][0][2]) and matriz_juego[0][0][2] != "":
            MostrarMensaje(matriz_juego[0][0][2].upper() + " ha ganado!")
            return True

    for col in range(len(matriz_juego)):
        if (matriz_juego[0][1][2] == matriz_juego[1][1][2] == matriz_juego[2][1][2]) and matriz_juego[0][1][2] != "":
            MostrarMensaje(matriz_juego[0][1][2].upper() + " ha ganado!")
            return True

    for col in range(len(matriz_juego)):
        if (matriz_juego[0][2][2] == matriz_juego[1][2][2] == matriz_juego[2][2][2]) and matriz_juego[0][2][2] != "":
            MostrarMensaje(matriz_juego[0][2][2].upper() + " has won!")
            return True

    if (matriz_juego[0][0][2] == matriz_juego[1][1][2] == matriz_juego[2][2][2]) and matriz_juego[0][0][2] != "":
        MostrarMensaje(matriz_juego[0][0][2].upper() + " ha ganado!")
        return True

    if (matriz_juego[0][2][2] == matriz_juego[1][1][2] == matriz_juego[2][0][2]) and matriz_juego[0][2][2] != "":
        MostrarMensaje(matriz_juego[0][2][2].upper() + " ha ganado!")
        return True

    return False

#Empate
def Draw(matriz_juego):
    for i in range(len(matriz_juego)):
        for j in range(len(matriz_juego[i])):
            if matriz_juego[i][j][2] == "":
                return False

    MostrarMensaje("Es un empate!")
    return True

#Mostrar mensaje si es victoria de 'x', de 'o' o empate
def MostrarMensaje(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

#Dibujar en pygame
def render():
    win.fill(WHITE)
    dibujarMatriz()

    # Drawing X's and O's
    for image in imagenes:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def main():
    global turnoDeX, turnoDeO, imagenes, draw, posicion

    imagenes = []
    draw = False
    posicion = "Empty"
    run = True

    turnoDeX = True
    turnoDeO = False

    matriz_juego = Inicializar()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            PcTurn(matriz_juego)
            #Si se hace click
            if event.type == pygame.MOUSEBUTTONDOWN:
               posicion = AccionJugador(matriz_juego)

        render()

        if AnyVictory(matriz_juego) or Draw(matriz_juego):
            run = False


while True:
    if __name__ == '__main__':
        main()