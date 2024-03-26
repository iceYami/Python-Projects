# Libro Aventuras de MG
class Aventuras:
    def __init__(self):
        self.paginas = {}
        self.pagina_actual = None

    def agregar_pagina(self, numero_pagina, texto, opciones):
        self.paginas[numero_pagina] = {"texto": texto, "opciones": opciones}

    def comenzar_aventura(self, numero_pagina):
        self.pagina_actual = numero_pagina

    def pasar_pagina(self, opcion):
        if opcion in self.paginas[self.pagina_actual]["opciones"]:
            siguiente_pagina = self.paginas[self.pagina_actual]["opciones"][opcion]
            # Verificar si es una página final y mostrar mensaje de agradecimiento
            if not self.paginas[siguiente_pagina]["opciones"]:
                print("Gracias por jugar la Aventura de MG")
            else:
                print(self.paginas[siguiente_pagina]["texto"])
            self.pagina_actual = siguiente_pagina
        else:
            print("Opción inválida. Elige otra opción.")

libro = Aventuras()

# Agregar páginas
libro.agregar_pagina(1, "Te encuentras en una bifurcación con dos caminos, ¿cuál eliges? (1 o 2)", {"1": 2, "2": 3})
libro.agregar_pagina(2, "Has llegado a la fortaleza de la noble elfa Ariman Campbell y decides quedarte con ella para buscar la Blue Obsidian. Fin de la Aventura.", {})
libro.agregar_pagina(3, "Te encuentras en una sala con las malvadas de Enormita. ¿Qué haces? (1: Luchar, 2: Correr)", {"1": 4, "2": 5})
libro.agregar_pagina(4, "Luchas contra Enormita, superando todos sus sucios trucos, y después de una ardua batalla les derrotas. ¡Enhorabuena, ahora eres su Líder!", {})
libro.agregar_pagina(5, "Huyes pero Enormita te da alcance y te apresan para que permanezcas con ellas para siempre.", {})

libro.comenzar_aventura(1)

# Iterar sobre las páginas
while True:
    print(libro.paginas[libro.pagina_actual]["texto"])
    opciones = libro.paginas[libro.pagina_actual]["opciones"]
    print("Opciones disponibles:", opciones)
    eleccion = input("Elige una opción: ")
    libro.pasar_pagina(eleccion)
