import datetime
import os

ARCHIVO_CUMPLEAÑOS = 'cumpleaños.txt'

def cargar_cumpleaños():
    lista_cumpleaños = {}
    if os.path.exists(ARCHIVO_CUMPLEAÑOS):
        with open(ARCHIVO_CUMPLEAÑOS, 'r') as archivo:
            for linea in archivo:
                nombre, fecha = linea.strip().split(',')
                lista_cumpleaños[nombre] = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
    return lista_cumpleaños

def guardar_cumpleaños(lista_cumpleaños):
    with open(ARCHIVO_CUMPLEAÑOS, 'w') as archivo:
        for nombre, fecha in lista_cumpleaños.items():
            archivo.write(f'{nombre},{fecha}\n')

def añadir_cumpleaños(lista_cumpleaños):
    nombre = input("Introduce el nombre: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    fecha = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
    lista_cumpleaños[nombre] = fecha
    guardar_cumpleaños(lista_cumpleaños)
    print(f"Cumpleaños de {nombre} guardado para el {fecha}.")

def revisar_proximos_cumpleaños(lista_cumpleaños):
    hoy = datetime.date.today()
    dias_proximos = 5
    for nombre, fecha in lista_cumpleaños.items():
        siguiente_cumple = fecha.replace(year=hoy.year)
        if siguiente_cumple < hoy:
            siguiente_cumple = siguiente_cumple.replace(year=hoy.year + 1)
        dias_restantes = (siguiente_cumple - hoy).days
        if 0 <= dias_restantes <= dias_proximos:
            print(f"El cumpleaños de {nombre} es en {dias_restantes} días ({siguiente_cumple}).")

def iniciar_menu():
    lista_cumpleaños = cargar_cumpleaños()
    while True:
        print("\n1. Añadir cumpleaños")
        print("2. Ver próximos cumpleaños")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            añadir_cumpleaños(lista_cumpleaños)
        elif opcion == '2':
            revisar_proximos_cumpleaños(lista_cumpleaños)
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, prueba de nuevo.")

if __name__ == "__main__":
    iniciar_menu()
