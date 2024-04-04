import random

def imprimir_tablero(tablero):
    for i in range(0, 9, 3):
        print(tablero[i] + '|' + tablero[i + 1] + '|' + tablero[i + 2])

def turno_jugador(tablero):
    while True:
        try:
            posicion = int(input('Elige una posición para colocar la X del 1 al 9: ')) - 1
            if tablero[posicion] == '_':
                tablero[posicion] = 'X'
                break
            else:
                print("Posición ocupada, elige otra.")
        except ValueError:
            print("Introduce un número del 1 al 9.")

def turno_adversario(tablero):
    while True:
        posicion = random.randint(0, 8)
        if tablero[posicion] == '_':
            tablero[posicion] = 'O'
            break

def hay_ganador(tablero):
    combinaciones_ganadoras = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                               (0, 3, 6), (1, 4, 7), (2, 5, 8),
                               (0, 4, 8), (2, 4, 6)]

    for combo in combinaciones_ganadoras:
        if tablero[combo[0]] == tablero[combo[1]] == tablero[combo[2]] != '_':
        return True
        return False

def tablero_lleno(tablero):
    return '_' not in tablero

def jugar():
    while True:
        tablero = ['_'] * 9

        while True:
            print("\nTablero actual:")
            imprimir_tablero(tablero)
            
            turno_jugador(tablero)
            if hay_ganador(tablero):
                print("\n¡Felicidades! ¡Has ganado!")
                break
            elif tablero_lleno(tablero):
                print("\n¡Empate!")
                break
            
            print("\nTurno de la computadora:")
            turno_adversario(tablero)
            if hay_ganador(tablero):
                print("\n¡El adversario ha ganado!")
                break
            elif tablero_lleno(tablero):
                print("\n¡Empate!")
                break

        jugar_nuevamente = input("¿Quieres jugar otra vez? (s/n): ")
        if jugar_nuevamente.lower() != 's':
            break

jugar()
