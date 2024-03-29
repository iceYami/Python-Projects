import random

def bienvenida():
    print("¡Bienvenida al Dilema del Prisionero!")
    print("Puedes optar por Confesar (C) o No Confesar (N).")

def jugar_prisionero():
    decisiones_usuario = []
    decisiones_oponente = []

    while True:
        decision_usuario = input("\n¿Confesar (C) o No Confesar (N)? (Escribe 'salir' para terminar) ").upper()
        
        if decision_usuario == 'SALIR':
            break
        
        decision_oponente = random.choice(['C', 'N'])

        decisiones_usuario.append(decision_usuario)
        decisiones_oponente.append(decision_oponente)

        print("El otro prisionero ha tomado la decisión de:", decision_oponente)

        if decision_usuario == 'C' and decision_oponente == 'C':
            print("Ambos habéis confesado. Sois condenados a 12 años de prisión cada uno.")
        elif decision_usuario == 'C' and decision_oponente == 'N':
            print("Eliges confesar, y el otro prisionero elige no confesar. Eres condenado a 10 años de prisión, mientras el otro prisionero sale libre.")
        elif decision_usuario == 'N' and decision_oponente == 'C':
            print("No confiesas, y el otro prisionero elige confesar. Eres liberada, mientras el otro prisionero es condenado a 10 años de prisión.")
        else:
            print("Ambos decidís no confesar. Sois condenados a 2 años de prisión cada uno.")

    print("\nTus decisiones:", decisiones_usuario)
    print("Decisiones de tu oponente:", decisiones_oponente)

    jugar_nuevamente = input("¿Quieres jugar de nuevo? (S/N): ").upper()
    if jugar_nuevamente == 'S':
        jugar_prisionero()
    else:
        print("¡Hasta luego!")

# Programa principal
bienvenida()
jugar_prisionero()
