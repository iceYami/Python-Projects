#Calculadora de Salarios Tecnológicos 2023 de MG

salarios = {
    "DEVOPS": {
        1: (45000, 50000),
        2: (50000, 80000),
        3: (80000, 95000),
        4: (85000, 110000)
    },
    "HELPDESK": {
        1: (25000, 32000),
        2: (32000, 40000),
        3: (35000, 48000),
        4: (42000, 60000)
    },
    "INGENIERO DE CIBERSEGURIDAD": {
        1: (28000, 36000),
        2: (36000, 55000),
        3: (55000, 70000),
        4: (70000, 90000)
    },
    "INGENIERO DE DATOS": {
        1: (35000, 45000),
        2: (40000, 68000),
        3: (60000, 80000),
        4: (80000, 100000)
    },
    "INGENIERO DE SOFTWARE": {
        1: (28000, 35000),
        2: (35000, 65000),
        3: (65000, 72000),
        4: (72000, 85000)
    },
    "PROJECT MANAGER": {
        1: (45000, 55000),
        2: (50000, 75000),
        3: (75000, 80000),
        4: (80000, 90000)
    },
    "TECNICO DE REDES": {
        1: (24000, 32000),
        2: (32000, 50000),
        3: (50000, 68000),
        4: (68000, 75000)
    },
    "TECNICO DE SISTEMAS": {
        1: (25000, 35000),
        2: (35000, 50000),
        3: (50000, 65000),
        4: (60000, 75000)
    }
}

print("Bienvenido a la Calculadora de Salarios Tecnológicos de 2023.")

def imprimir_profesiones():
    print("Profesiones disponibles:")
    for idx, profesion in enumerate(sorted(salarios.keys()), start=1):
        print(f"{idx}. {profesion}")

def imprimir_experiencia():
    print("Intervalo de experiencia:")
    print("1. ≤ 2 años")
    print("2. 2-6 años")
    print("3. 6-10 años")
    print("4. 10 años")

def calcular_salario():
    imprimir_profesiones()
    
    seleccion = input("Elige tu profesión: ")
    try:
        seleccion = int(seleccion)
        if 1 <= seleccion <= len(salarios):
            profesion = sorted(salarios.keys())[seleccion - 1]
            print(f"Tu profesión es: {profesion}")
            
            imprimir_experiencia()
            exp_seleccionada = input("Elige tu intervalo de experiencia: ")
            try:
                exp_seleccionada = int(exp_seleccionada)
                if 1 <= exp_seleccionada <= 4:
                    salario_min, salario_max = salarios[profesion][exp_seleccionada]
                    print(f"Tu salario estimado para {profesion} con la experiencia que has elegido es entre {salario_min}€ y {salario_max}€.")
                    volver_menu()
                else:
                    print("Elección no válida.")
            except ValueError:
                print("Por favor, introduce un número válido vinculado al intervalo de experiencia.")
        else:
            print("Elección no válida.")
    except ValueError:
        print("Por favor, introduce un número vinculado a una profesión de la lista.")

def volver_menu():
    respuesta = input("¿Quieres regresar al menú? (s/n): ")
    if respuesta.lower() == 's':
        calcular_salario()
    elif respuesta.lower() == 'n':
        print("Gracias por usar la calculadora de salario de MG, ¡hasta luego!")
    else:
        print("Opción inválida.")
        volver_menu()

calcular_salario()
