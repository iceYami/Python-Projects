def sumar(a, b):
    return a + b
def restar(a, b):
    return a - b
def multiplicar(a, b):
    return a * b
def dividir(a, b):
    if b != 0:
        return a / b

def calculadora():
    while True:
        print("\nSeleccione la operación")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplica")
        print("4. Divide")
        operacion = input("Introduzca el número de la operación")

        if operacion in ['1', '2', '3', '4']:
            num1 = float(input("Primer número"))
            num2 = float(input("Segundo número"))

            if operacion == '1':
                print("Resultado:", sumar(num1, num2))
            elif operacion == '2':
                print("Resultado:", restar(num1, num2))
            elif operacion == '3':
                print("Resultado:", multiplicar(num1, num2))
            elif operacion == '4':
                resultado = dividir(num1, num2)
                if resultado is not None:
                    print("Resultado:", resultado)

calculadora()
