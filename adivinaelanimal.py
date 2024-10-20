import time

class Animal:
    def __init__(self, nombre, sonido):
        self.nombre = nombre
        self.sonido = sonido.lower()

animales = [
    Animal("perro", "guau"),
    Animal("gato", "miau"),
    Animal("vaca", "mu"),
    Animal("pollo", "cucurucú"),
    Animal("elefante", "barritar"),
    Animal("cerdo", "oink"),
    Animal("caballo", "relincho"),
    Animal("oveja", "beee"),
    Animal("pato", "cuac"),
    Animal("loro", "grar"),
    Animal("tigre", "rugir"),
    Animal("león", "rugir"),
    Animal("mono", "chillar"),
    Animal("delfín", "chirrido"),
    Animal("ballena", "canto"),
    Animal("rana", "croac"),
    Animal("cabra", "meee"),
    Animal("búho", "ulular"),
    Animal("abeja", "zumbido"),
    Animal("cisne", "trompeteo"),
    Animal("gallo", "kikirikí"),
]

def adivinar_animal():
    print("Piensa en un animal y escribe 'listo' cuando estés listo para comenzar.")
    while True:
        respuesta = input().strip().lower()
        if respuesta == "listo":
            break
        else:
            print("Por favor escribe 'listo' para comenzar.")
    
    print("\nPiensa en el sonido del animal que elegiste.")
    time.sleep(1)
    print("\nVoy a hacerte algunas preguntas para adivinar qué animal es.")
    time.sleep(1)
    
    posibles_animales = animales[:]
    
    while len(posibles_animales) > 1:
        pregunta = f"¿El animal hace el sonido '{posibles_animales[0].sonido}'? (sí/no): "
        respuesta = input(pregunta).strip().lower()
        
        if respuesta == "sí":
            posibles_animales = [animal for animal in posibles_animales if animal.sonido == posibles_animales[0].sonido]
        elif respuesta == "no":
            posibles_animales = [animal for animal in posibles_animales if animal.sonido != posibles_animales[0].sonido]
        else:
            print("Respuesta no válida. Por favor responde con 'sí' o 'no'.")
    
    animal_adivinado = posibles_animales[0]
    print(f"\n¡He adivinado que estás pensando en un {animal_adivinado.nombre}!")
    print("¡Gracias por jugar!")

adivinar_animal()
