import random

def mostrar_bienvenida():
    print("*" * 40)
    print("¡Bienvenida a tu Gestor de Actividades!")
    print("*" * 40)

def cargar_actividades():

    try:
        with open("actividades.txt", "r") as archivo:
            actividades = archivo.read().splitlines()
        return actividades

    except FileNotFoundError:
        print("No se encontró el archivo 'actividades.txt'. Se creará uno nuevo.")
        actividades_por_defecto = 

[
            "Ir al gimnasio",
            "Leer un libro",
            "Cocinar una nueva receta",
            "Ver una película",
            "Escribir",
            "Estudiar",
            "Investigar algo nuevo",
            "Llamar a un ser querido",
            "Hablar con un familiar",
            "Salir a dar un paseo",
            "Tomar el sol",
            "Leer un manga"
        ]

        return actividades_por_defecto

def guardar_actividades(actividades):
    with open("actividades.txt", "w") as archivo:
        for actividad in actividades:
            archivo.write(actividad + "\n")

def agregar_actividad(actividades):
    nueva_actividad = input("Introduce una nueva actividad: ")
    actividades.append(nueva_actividad)
    print("¡Actividad añadida!")

def seleccionar_actividad(actividades):
    print("*" * 40)

    if actividades:
        actividad_elegida = random.choice(actividades)
        print("La actividad elegida es:", actividad_elegida)

    else:
        print("No hay actividades disponibles.")
    print("*" * 40)

def main():
    mostrar_bienvenida()
    actividades = cargar_actividades()

    while True:
        print("\n--- Menú ---")
        print("1. Agregar nueva actividad")
        print("2. Elige una actividad")
        print("3. Guarda lista de actividades")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            agregar_actividad(actividades)
        elif opcion == "2":
            seleccionar_actividad(actividades)
        elif opcion == "3":
            guardar_actividades(actividades)
            print("Lista de actividades guardada correctamente.")
        elif opcion == "4":
            print("*" * 40)
            print("¡Hasta luego!")
            print("*" * 40)
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
