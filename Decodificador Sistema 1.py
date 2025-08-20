def sum_position(char):
    return ord(char.lower()) - ord('a') + 1

def position_to_char(position):
    return chr((position - 1) % 26 + ord('a'))

def decode_system_1(text):
    decoded_text = ''
    for char in text:
        if char.isalpha():
            position = sum_position(char)
            new_position = (position - 3) % 26
            if new_position <= 0:
                new_position += 26
            new_char = position_to_char(new_position)
            decoded_text += new_char
        else:
            decoded_text += char
    return decoded_text

def main_menu():
    while True:
        print("\nDecodificador Método Audrey")
        print("1. Frase codificada")
        print("2. Salir")
        
        option = input("opción: ")
        
        if option == '1':
            text = input("Frase a decodificar: ")
            result = decode_system_1(text)
            print("Frase decodificada:", result)
        elif option == '2':
            print("Fin")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main_menu()
