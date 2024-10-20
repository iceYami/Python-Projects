def contar_caracteres(texto):
    total_caracteres = len(texto)
    mayusculas = sum(1 for c in texto if c.isupper())
    minusculas = sum(1 for c in texto if c.islower())
    numeros = sum(1 for c in texto if c.isdigit())
    especiales = total_caracteres - (mayusculas + minusculas + numeros)
    palabras = len(texto.split())
    
    print("\nEstadísticas:")
    print(f"Nº total de caracteres: {total_caracteres}")
    print(f"Nº de palabras: {palabras}")
    print(f"Nº de caracteres en mayúsculas: {mayusculas}")
    print(f"Nº de caracteres en minúsculas: {minusculas}")
    print(f"Nº de números: {numeros}")
    print(f"Nº de caracteres especiales: {especiales}")

def main():
    print("¡Bienvenido!")
    while True:
        texto = input("\nIntroduce un texto (o escribe 'salir' para terminar): ")
        if texto.lower() == 'salir':
            print("¡Hasta luego!")
            break
        contar_caracteres(texto)
        
        opcion = input("\n¿Quieres introducir otro texto? (s/n): ")
        if opcion.lower() != 's':
            print("¡Hasta otra!")
            break

if __name__ == "__main__":
    main()
