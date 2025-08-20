def sum_position(char):
    return ord(char.lower()) - ord('a') + 1

def position_to_char(position):
    return chr((position - 1) % 26 + ord('a'))

def encode_system_1(text):
    encoded_text = ''
    for char in text:
        if char.isalpha():
            position = sum_position(char)
            new_position = (position + 3) % 26
            if new_position == 0:
                new_position = 26
            new_char = position_to_char(new_position)
            encoded_text += new_char
        else:
            encoded_text += char
    return encoded_text

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

def encode_system_2(text):
    encoded_text = ''
    for char in text:
        if char.isalpha():
            position = sum_position(char)
            new_position = (position * 2) % 26
            if new_position == 0:
                new_position = 26
            new_char = position_to_char(new_position)
            encoded_text += new_char
        else:
            encoded_text += char
    return encoded_text

def decode_system_2(text):
    decoded_text = ''
    for char in text:
        if char.isalpha():
            position = sum_position(char)
            # Find the modular inverse of 2 mod 26, which is 13 (because 2 * 13 ≡ 1 mod 26)
            inv = 13
            new_position = (position * inv) % 26
            if new_position == 0:
                new_position = 26
            new_char = position_to_char(new_position)
            decoded_text += new_char
        else:
            decoded_text += char
    return decoded_text

def main_menu():
    while True:
        print("\nBienvenida al juego")
        print("opciones:")
        print("1. Codifica en codigo 1")
        print("2. Decodifica en codigo 1")
        print("3. Codificar en codigo 2")
        print("4. Decodificar en codigo 2")
        print("5. Atras")
        
        option = input("di opcion: ")
        
        if option in ['1', '2', '3', '4']:
            text = input("Di la frase: ")
            if option == '1':
                result = encode_system_1(text)
            elif option == '2':
                result = decode_system_1(text)
            elif option == '3':
                result = encode_system_2(text)
            elif option == '4':
                result = decode_system_2(text)
            print("resultado:", result)
        elif option == '5':
            print("fin")
            break
        else:
            print("invalido")

if __name__ == "__main__":
    main_menu()
