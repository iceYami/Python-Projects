import random

def seleccionar_palabra():
    palabras = ['sistemas', 'ciberseguridad', 'SQL', 'tecnologia', 'inteligencia', 'metasploit', 'firewall', 'phishing', 'hacking', 'wireshark', 'kali', 'networking', 'hydra']
    return random.choice(palabras)

def mostrar_tablero(palabra, letras_adivinadas):
    tablero = ''
    for letra in palabra:
        if letra in letras_adivinadas:
            tablero += letra + ' '
        else:
            tablero += '_ '
    return tablero

def mostrar_ahorcado(intentos_restantes):
    ahorcado = [
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \\
        =============
        ''',
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / 
        =============
        ''',
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |      
        =============
        ''',
        '''
           --------
           |      |
           |      O
           |     \|
           |      |
           |     
        =============
        ''',
        '''
           --------
           |      |
           |      O
           |      |
           |      |
           |     
        =============
        ''',
        '''
           --------
           |      |
           |      O
           |    
           |      
           |     
        =============
        ''',
        '''
           --------
           |      |
           |      
           |    
           |      
           |     
        =============
        '''
    ]
    print(ahorcado[intentos_restantes])

def jugar_ahorcado():
    print("¡Bienvenida al Ahorcado!")
    palabra_secreta = seleccionar_palabra()
    letras_adivinadas = []
    intentos_restantes = 6

    while True:
        print("\n" + mostrar_tablero(palabra_secreta, letras_adivinadas))
        mostrar_ahorcado(intentos_restantes)
        if intentos_restantes == 0:
            print("\n¡Has perdido! La palabra era:", palabra_secreta)
            break

        if set(palabra_secreta) == set(letras_adivinadas):
            print("\n¡Felicidades! ¡Has adivinado la palabra!")
            break

        letra = input("\nIntroduce una letra: ").lower()

        if letra in letras_adivinadas:
            print("Ya has probado esa letra. ¡Intenta otra!")
            continue
        elif letra in palabra_secreta:
            letras_adivinadas.append(letra)
        else:
            intentos_restantes -= 1
            print("Letra incorrecta. Te quedan {} intentos.".format(intentos_restantes))

    jugar_de_nuevo = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
    if jugar_de_nuevo == 's':
        jugar_ahorcado()
    else:
        print("\n¡Gracias!")

jugar_ahorcado()
