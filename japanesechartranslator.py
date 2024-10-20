# Traductor de caracteres españoles a caracteres japoneses

traducir_es_a_jp = 
{
    'a': 'あ',
    'b': 'い',
    'c': 'う',
    'd': 'え',
    'e': 'お',
    'f': 'か',
    'g': 'き',
    'h': 'く',
    'i': 'け',
    'j': 'こ',
    'k': 'さ',
    'l': 'し',
    'm': 'す',
    'n': 'せ',
    'o': 'そ',
    'p': 'た',
    'q': 'ち',
    'r': 'つ',
    's': 'て',
    't': 'と',
    'u': 'な',
    'v': 'に',
    'w': 'ぬ',
    'x': 'ね',
    'y': 'の',
    'z': 'は',
    'á': 'ひ',
    'é': 'ふ',
    'í': 'へ',
    'ó': 'ほ',
    'ú': 'ま',
    'ñ': 'み',
    'ü': 'む',
}

def traducir_es_a_jp(texto):
    texto = texto.lower()
    traduccion = ''.join(traducir_es_a_jp.get(letra, letra) for letra in texto)
    return traduccion

def traducir_jp_a_es(texto):
    traduccion_inversa = {v: k for k, v in traducir_es_a_jp.items()}
    traduccion = ''.join(traduccion_inversa.get(letra, letra) for letra in texto)
    return traduccion

def menu():
    print("Elige una opción:")
    print("1. Español a Japonés")
    print("2. Japonés a Español")
    print("3. Salir")

while True:
    menu()
    opcion = input("Introduce tu opción: ")

    if opcion == '1':
        texto_espanol = input("Introduce el texto en español: ")
        texto_traducido_japones = traducir_es_a_jp(texto_espanol)
        print("Texto traducido a caracteres japoneses:", texto_traducido_japones)

    elif opcion == '2':
        texto_japones = input("Introduce el texto en caracteres japoneses: ")
        texto_traducido_espanol = traducir_jp_a_es(texto_japones)
        print("Texto traducido a español:", texto_traducido_espanol)

    elif opcion == '3':
        print("Nos vemos luego, ¡sayonara!")
        break

    else:
        print("Opción inválida.")
