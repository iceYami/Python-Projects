def calcular_salario_por_hora(salario_mensual, horas_semanales):
    horas_mensuales = horas_semanales * 4.33
    return salario_mensual / horas_mensuales

def salario_anual_a_mensual(salario_anual, pagas_anuales):
    return salario_anual / pagas_anuales

def salario_mensual_a_anual(salario_mensual, pagas_anuales):
    return salario_mensual * pagas_anuales

def neto_a_bruto(salario_neto, tasa_impuestos):
    return salario_neto / (1 - tasa_impuestos)

def bruto_a_neto(salario_bruto, tasa_impuestos):
    return salario_bruto * (1 - tasa_impuestos)

def obtener_opcion(prompt, opciones):
    while True:
        print(prompt)
        for i, opcion in enumerate(opciones, 1):
            print(f"{i}. {opcion}")
        seleccion = input("Seleccione una opción: ")
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(opciones):
            return int(seleccion)
        else:
            print("Opción no válida. Inténtelo de nuevo.\n")

def obtener_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.\n")

def iniciar_calculadora():
    while True:
        tipo_salario = obtener_opcion("Elija el tipo de salario:", ["Salario Bruto", "Salario Neto"])
        periodo_salario = obtener_opcion("Elija el periodo del salario:", ["Mensual", "Anual"])
        salario = obtener_float("Ingrese el monto del salario: ")
        tasa_impuestos = obtener_float("Ingrese la tasa de impuestos en porcentaje (ejemplo: 20 para 20%): ") / 100
        pagas_anuales = obtener_opcion("Elija el número de pagas anuales:", ["12 pagas", "14 pagas"])
        pagas_anuales = 12 if pagas_anuales == 1 else 14

        if tipo_salario == 1:
            if periodo_salario == 1:
                salario_bruto_mensual = salario
                salario_bruto_anual = salario_mensual_a_anual(salario, pagas_anuales)
            else:
                salario_bruto_anual = salario
                salario_bruto_mensual = salario_anual_a_mensual(salario, pagas_anuales)
            salario_neto_mensual = bruto_a_neto(salario_bruto_mensual, tasa_impuestos)
            salario_neto_anual = salario_mensual_a_anual(salario_neto_mensual, pagas_anuales)
        else:
            if periodo_salario == 1:
                salario_neto_mensual = salario
                salario_neto_anual = salario_mensual_a_anual(salario, pagas_anuales)
            else:
                salario_neto_anual = salario
                salario_neto_mensual = salario_anual_a_mensual(salario, pagas_anuales)
            salario_bruto_mensual = neto_a_bruto(salario_neto_mensual, tasa_impuestos)
            salario_bruto_anual = salario_mensual_a_anual(salario_bruto_mensual, pagas_anuales)

        horas_semanales = obtener_float("Ingrese el número de horas trabajadas por semana: ")
        salario_bruto_por_hora = calcular_salario_por_hora(salario_bruto_mensual, horas_semanales)
        salario_neto_por_hora = calcular_salario_por_hora(salario_neto_mensual, horas_semanales)

        print("\nResultados:")
        print(f"Salario Bruto Mensual: ${salario_bruto_mensual:.2f}")
        print(f"Salario Bruto Anual: ${salario_bruto_anual:.2f}")
        print(f"Salario Neto Mensual: ${salario_neto_mensual:.2f}")
        print(f"Salario Neto Anual: ${salario_neto_anual:.2f}")
        print(f"Salario Bruto por Hora: ${salario_bruto_por_hora:.2f}")
        print(f"Salario Neto por Hora: ${salario_neto_por_hora:.2f}")

        reiniciar = input("¿Desea realizar otra consulta? (s/n): ").strip().lower()
        if reiniciar != 's':
            break

if __name__ == "__main__":
    iniciar_calculadora()
