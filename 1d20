def obtener_numero_aleatorio():
    global seed
    a = 1103515245
    c = 12345
    m = 32768
    seed = (a * seed + c) % m
    return seed

seed = 1

def lanzar_d20():
    numero_aleatorio = obtener_numero_aleatorio()
    return (numero_aleatorio % 20) + 1

def simulador_lanzamiento_d20(num_lanzamientos):
    resultados = []
    for _ in range(num_lanzamientos):
        resultado = lanzar_d20()
        resultados.append(resultado)
    return resultados

def main():
    print("Lanza dado 1d20")
    
    while True:
        num_lanzamientos = int(input("\nCuantas veces lanzas el dado d20: "))
        
        resultados = simulador_lanzamiento_d20(num_lanzamientos)
        
        print("\nResultados:")
        for i, resultado in enumerate(resultados, start=1):
            print(f"Lanzamiento {i}: {resultado}")
        
        opcion = input("\n¿Tirar 1d20 de nuevo? (s/n): ")
        if opcion.lower() != 's':
            break

if __name__ == "__main__":
    main()
