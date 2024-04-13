def cifrar(texto, clave):
    texto_cifrado = ''
    for caracter in texto:
        if caracter.isalpha():
            offset = ord('a') if caracter.islower() else ord('A')
            indice = (ord(caracter) - offset + clave) % 26
            texto_cifrado += chr(indice + offset)
        else:
            texto_cifrado += caracter
    return texto_cifrado

def descifrar(texto_cifrado, clave):
    return cifrar(texto_cifrado, -clave)

def main():
    print("¡Bienvenida!")
    print("Elige una opción:")
    print("1. Cifrar")
    print("2. Descifrar")

    opcion = int(input("¿Qué quieres hacer?: "))
    texto = input("Introduce el texto: ")
    clave = int(input("Introduce la clave: "))

    if opcion == 1:
        texto_cifrado = cifrar(texto, clave)
        print("Texto cifrado:", texto_cifrado)
        with open("texto_cifrado.txt", "w") as file:
            file.write(texto_cifrado)
        print("Texto cifrado guardado en texto_cifrado.txt")
    elif opcion == 2:
        texto_descifrado = descifrar(texto, clave)
        print("Texto descifrado:", texto_descifrado)
        with open("texto_descifrado.txt", "w") as file:
            file.write(texto_descifrado)
        print("Texto descifrado guardado en texto_descifrado.txt")
    else:
        print("Opción invalida.")

if __name__ == "__main__":
    main()
