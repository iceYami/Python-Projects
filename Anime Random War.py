import random

def elegir_aleatorio(lista):
    indice = int((len(lista) * (hash(str(lista)) % 100) / 100)) % len(lista)
    return lista[indice]

def retraso(segundos):
    tiempo_objetivo = segundos * 10**6  # Convertir segundos a microsegundos
    tiempo_inicio = 0
    while tiempo_inicio < tiempo_objetivo:
        tiempo_inicio += 1

def batalla():
    heroinas = [
        "Ymir (Attack on Titan)", "Saber (Fate/stay night)", "Mikasa Ackerman (Attack on Titan)",
        "Chizuru Mizuhara (Rent-a-Girlfriend)", "Akari Mizunashi (Aria the Animation)", 
        "Kaguya Shinomiya (Kaguya-sama: Love Is War)", "Yukino Yukinoshita (My Teen Romantic Comedy)",
        "Madoka Kaname (Puella Magi Madoka Magica)", "Homura Akemi (Puella Magi Madoka Magica)",
        "Yuriko Nanao (Citrus)", "Mikako Satsukitane (Heaven's Lost Property)", "Futaba Igarashi (Citrus)",
        "Hana N. (Bloom Into You)", "Sayaka Miki (Puella Magi Madoka Magica)", "Yui Hirasawa (K-On!)",
        "Ami Mizuno (Sailor Moon)", "Tsubomi Kido (Saki)", "Chitoge Kirisaki (Nisekoi)", 
        "Mikako Satsukitane (Heaven's Lost Property)", "Tina Sprout (Toradora!)", "Aoi Kiriya (Uta no Prince-sama)"
    ]

    villanas = [
        "Yuzu Aihara (Citrus)", "Nina (Citrus)", "Sayaka Miki (Puella Magi Madoka Magica)",
        "Kyouko Sakura (Puella Magi Madoka Magica)", "Ymir (Attack on Titan)", "Kurumi Tokisaki (Date A Live)",
        "Akane Hiyama (My Senpai is Annoying)", "Milly Ashford (Code Geass)", "Saber (Fate/stay night)",
        "Moka Akashiya (Rosario + Vampire)", "Nanako Usami (Citrus)", "Yui Hirasawa (K-On!)", 
        "Shiro (No Game No Life)", "Satsuki Kiryuin (Kill la Kill)", "Tayuya (Naruto)", 
        "Erina Nakiri (Food Wars)", "Alice Zuberg (Sword Art Online: Alicization)", "Ami Mizuno (Sailor Moon)",
        "Kaede Azusa (Bloom Into You)", "Lalatina (Konosuba)", "Chitoge Kirisaki (Nisekoi)", "Madoka Kaname"
    ]

    print("¡La batalla comienza!")
    retraso(2)  # Esperar 2 segundos

    heroina = elegir_aleatorio(heroinas)
    villana = elegir_aleatorio(villanas)

    print(f"{heroina} se enfrenta a {villana}")
    retraso(2)  # Esperar 2 segundos

    ganador = elegir_aleatorio([heroina, villana])
    if ganador in heroinas:
        resultado = "¡La Heroína ha ganado!"
    else:
        resultado = "¡La Villana ha ganado!"

    print(resultado)
    retraso(2)

def principal():
    while True:
        batalla()
        repetir = input("¿Quieres simular otra batalla? (s/n): ")
        if repetir.lower() != 's':
            break
        retraso(2)  # Esperar 2 segundos antes de la siguiente simulación

if __name__ == "__main__":
    principal()
