import random

class RuletaRusa:
    def __init__(self, nombre_jugador, num_balas_reales, num_balas_fogueo, num_vacios, num_jugadores=2):
        self.nombre_jugador = nombre_jugador
        self.num_balas_reales = num_balas_reales
        self.num_balas_fogueo = num_balas_fogueo
        self.num_vacios = num_vacios
        self.num_jugadores = num_jugadores
        self.bala = 0
        self.jugador_actual = random.randint(0, num_jugadores - 1)
        self.balas = [1] * num_balas_reales + [2] * num_balas_fogueo + [0] * num_vacios
        random.shuffle(self.balas)
    
    def disparar(self, jugador, rival=None):
        if self.bala == 0:
            self.bala = self.balas.pop()
        
        if self.bala == 1:
            print("¡BOOM! Jugador", jugador, "ha sido eliminado.")
            return False
        elif self.bala == 2:
            print("¡Click! Jugador", jugador, "sobrevive (fue una bala de fogueo).")
            if rival is not None:
                self.jugador_actual = rival
            return True
        else:
            print("¡Click! Jugador", jugador, "sobrevive (bala vacía).")
            if rival is not None:
                self.jugador_actual = rival
            return True

    def jugar(self):
        while len(self.balas) > 0:
            print("\nTurno de", self.nombre_jugador)
            print("Opciones:")
            print("1. Dispararse a sí mismo")
            print("2. Disparar a su rival")
            
            accion = int(input("Elige una opción: "))
            
            if accion == 1:
                if not self.disparar(self.nombre_jugador):
                    return "¡Fin del juego!"
                print("¡Felicidades,", self.nombre_jugador + ", has ganado 10 millones de euros y un Lamborghini verde!")
                return "¡Fin del juego!"
            elif accion == 2:
                rival = int(input("Elige el número del rival a disparar: ")) % self.num_jugadores
                if not self.disparar(self.nombre_jugador, rival):
                    return "¡Fin del juego!"
            else:
                print("Opción inválida.")
                continue
            
            self.jugador_actual = (self.jugador_actual + 1) % self.num_jugadores
        
        return "¡Todos sobreviven! ¡Fin del juego!"
