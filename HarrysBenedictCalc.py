import random

def calcular_tmb(sexo, peso, altura, edad):

    if sexo.lower() == 'hombre':
        return 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    elif sexo.lower() == 'mujer':
        return 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    else:
        raise ValueError("Sexo no válido. Usa 'hombre' o 'mujer'.")

def calcular_calorias_diarias(tmb, factor_actividad):
  
    factores = {
        'sedentario': 1.2,
        'ligeramente activo': 1.375,
        'moderadamente activo': 1.55,
        'muy activo': 1.725,
        'extremadamente activo': 1.9
    }
    if factor_actividad.lower() not in factores:
        raise ValueError("Factor de actividad no válido.")
    return tmb * factores[factor_actividad.lower()]

def recomendar_macros(calorias):

    macros = {
        'proteínas': (calorias * 0.10 / 4, calorias * 0.35 / 4),
        'carbohidratos': (calorias * 0.45 / 4, calorias * 0.65 / 4),
        'grasas': (calorias * 0.20 / 9, calorias * 0.35 / 9)
    }
    return macros

def obtener_entrada_usuario(mensaje, tipo):

    while True:
        entrada = input(mensaje).strip()
        try:
            if tipo == 'float':
                return float(entrada)
            elif tipo == 'int':
                return int(entrada)
            elif tipo == 'str':
                return entrada.lower()
        except ValueError:
            print(f"Error.")

def mostrar_frase_motivadora():

    frases = [
        "¡Sigue adelante, cada paso cuenta!",
        "¡Estás haciendo un gran trabajo, no te rindas!",
        "¡Tu esfuerzo está dando frutos!",
        "¡Cada día es una nueva oportunidad para mejorar!",
        "¡Cree en ti misma y todo será posible!"
    ]
    print(f"\n{random.choice(frases)}\n")

def main():

    while True:
        print("Calculadora de Calorías Diarias")
        
        sexo = obtener_entrada_usuario("Ingrese su sexo (hombre/mujer): ", 'str')
        peso = obtener_entrada_usuario("Ingrese su peso en kg: ", 'float')
        altura = obtener_entrada_usuario("Ingrese su altura en cm: ", 'float')
        edad = obtener_entrada_usuario("Ingrese su edad en años: ", 'int')
        factor_actividad = obtener_entrada_usuario("Introduce nivel de actividad (sedentario/ligeramente activo/moderadamente activo/muy activo/extremadamente activo): ", 'str')
        
        try:
            tmb = calcular_tmb(sexo, peso, altura, edad)
            calorias_diarias = calcular_calorias_diarias(tmb, factor_actividad)
            macros = recomendar_macros(calorias_diarias)
        
            print(f"\nCalorías diarias necesarias: {calorias_diarias:.2f} kcal")
            print("\nRecomendaciones de macronutrientes (gramos por día):")
            print(f"Proteínas: {macros['proteínas'][0]:.2f}g - {macros['proteínas'][1]:.2f}g")
            print(f"Carbohidratos: {macros['carbohidratos'][0]:.2f}g - {macros['carbohidratos'][1]:.2f}g")
            print(f"Grasas: {macros['grasas'][0]:.2f}g - {macros['grasas'][1]:.2f}g")
            
            print("\nImportancia de los macronutrientes:")
            print("Proteínas: Necesarias para la reparación y crecimiento muscular.")
            print("Carbohidratos: Principal fuente de energía para el cuerpo.")
            print("Grasas: Esenciales para la absorción de vitaminas y funcionamiento hormonal.")
            
            mostrar_frase_motivadora()
            
            reiniciar = input("¿Deseas usar la calculadora de nuevo? (s/n): ").strip().lower()
            if reiniciar != 's':
                print("Gracias por usar la calculadora. ¡Hasta pronto!")
                break
        
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
