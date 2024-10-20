def es_par(num):
    return num % 2 == 0

def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def analizar_numero(num):
    def imprimir_con_retraso(mensaje):
        for char in mensaje:
            print(char, end='', flush=True)
    
    if isinstance(num, int):
        tipo = "entero"
    elif isinstance(num, float):
        tipo = "decimal"
    else:
        tipo = "no válido"
    
    imprimir_con_retraso(f"Tipo de número: {tipo}\n")
    
    if isinstance(num, (int, float)):
        if es_par(num):
            imprimir_con_retraso(f"El número {num} es par.\n")
        else:
            imprimir_con_retraso(f"El número {num} es impar.\n")
        
        if isinstance(num, int):
            if es_primo(num):
                imprimir_con_retraso(f"El número {num} es primo.\n")
            else:
                imprimir_con_retraso(f"El número {num} no es primo.\n")
                imprimir_con_retraso(f"Números primos de los que {num} es múltiplo:\n")
                for i in range(2, num):
                    if es_primo(i) and num % i == 0:
                        imprimir_con_retraso(f"{i}\n")
    else:
        imprimir_con_retraso("No se puede determinar para este número.\n")

def mensaje_bienvenida():
    print("Bienvenida al Analizador de Números")
    print("Elige:")
    print("1. Número")
    print("2. Salir")

def obtener_opcion_usuario():
    while True:
        opcion = input("Elige opción (1 o 2): ")
        if opcion in ['1', '2']:
            return opcion
        else:
            print("Opción inválida.")

while True:
    mensaje_bienvenida()
    opcion = obtener_opcion_usuario()
    
    if opcion == '2':
        print("¡Chao pescao!")
        break
    
    if opcion == '1':
        try:
            entrada = input("Introduce un número (o 'salir' para terminar): ")
            
            if entrada.lower() == 'salir':
                print("Chao pescao")
                break
            
            numero = eval(entrada)
            analizar_numero(numero)
        except (NameError, SyntaxError):
            print("Entrada inválida. Ingresa un número entero o decimal.")
        except ZeroDivisionError:
            print("División por cero no permitida.")
        except Exception as e:
            print(f"Error: {e}")
