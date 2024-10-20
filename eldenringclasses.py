def mostrar_menu_clases():
    print("¡Bienvenida a la Breve Guía de Clases para Elden Ring de MG!")

    clases = [
        ("Astrologo", "Inteligencia, mente, aguante y vigor", "Bastón de piedra refulgente de Azur"),
        ("Bandido", "Destreza, aguante, vigor y arcano", "Reduvia "),
        ("Confesor", "Fe, vigor, mente y destreza", "Guadaña Alada"),
        ("Guerrero", "Vigor, resistencia, destreza y fuerza", "Espadón de Starscourge, Espada de escamas de dragón de Magma"),
        ("Heroe", "Fuerza, resistencia, vigor y destreza", "Espadón de Hoja Injertada"),
        ("Miserable", "Fuerza, destreza e inteligencia, vigor y aguante", "Reduvia"),
        ("Prisionero", "Inteligencia, vigor, mente y destreza", "Estoque de Rogier"),
        ("Profeta", "Mente, fe, vigor y arcano", "Guadaña Alada"),
        ("Samurai", "Destreza, vigor, aguante y mente", "Ríos de sangre"),
        ("Vagante", "Fuerza, resistencia y vigor", "Espada del Señor"),
    ]

    print("Elige una clase para tu personaje:")
    for idx, (nombre, _, _) in enumerate(clases, start=1):
        print(f"{idx}. {nombre}")

    return clases

def obtener_info_clase(clase, clases):
    clase_seleccionada = clases[clase - 1]
    return clase_seleccionada

def main():
    while True:
        clases = mostrar_menu_clases()
        seleccion = int(input("Elige la clase: "))

        if seleccion < 1 or seleccion > len(clases):
            print("Selección inválida.")
            continue

        clase, atributos, mejor_arma = obtener_info_clase(seleccion, clases)

        print(f"Has escogido la clase {clase}.")
        print(f"Atributos recomendados: {atributos}.")
        print(f"Mejor arma: {mejor_arma}.")

        volver = input("¿Deseas volver a elegir una clase? (s/n): ")
        if volver.lower() != 's':
            break

if __name__ == "__main__":
    main()
