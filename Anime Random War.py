import random

def choose_random(lst):
    index = int((len(lst) * (hash(str(lst)) % 100) / 100)) % len(lst)
    return lst[index]

def delay(seconds):
    target_time = seconds * 10**6  # Convert seconds to microseconds
    start_time = 0
    while start_time < target_time:
        start_time += 1

def battle_yuri():
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

    print("The yuri battle begins!")
    delay(2)  # Wait for 2 seconds

    hero = choose_random(heroinas)
    villain = choose_random(villanas)

    print(f"{hero} faces {villain}")
    delay(2)  # Wait for 2 seconds

    winner = choose_random([hero, villain])
    if winner in heroinas:
        result = "The Heroine has won!"
    else:
        result = "The Villain has won!"

    print(result)
    delay(2)

def main():
    while True:
        battle_yuri()
        repeat = input("Do you want to simulate another battle? (y/n): ")
        if repeat.lower() != 'y':
            break
        delay(2)  # Wait for 2 seconds before the next simulation

if __name__ == "__main__":
    main()
