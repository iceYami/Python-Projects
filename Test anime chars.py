def main():
    print("¡Bienvenido al test de personajes de Citrus!")
    print("Responde las siguientes preguntas para descubrir qué personaje de *Citrus* eres.")

    character_scores = {
        "Yuzu Aihara": 0,
        "Mayo Aihara": 0,
        "Harumi Sae": 0,
        "Nijika Kugasaki": 0,
        "Himeko Momokino": 0,
        "Sara Tachibana": 0,
        "Shou Aihara": 0
    }

    print("\nPregunta 1: ¿Cómo prefieres pasar tu tiempo libre?")
    print("a) Pasando tiempo con tus amigos y familia")
    print("b) Estudiando o mejorando tus habilidades")
    print("c) Buscando nuevas aventuras o experiencias")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Nijika Kugasaki"] += 1
        character_scores["Himeko Momokino"] += 1
    elif answer == "b":
        character_scores["Mayo Aihara"] += 1
        character_scores["Harumi Sae"] += 1
        character_scores["Sara Tachibana"] += 1
    elif answer == "c":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Shou Aihara"] += 1

    print("\nPregunta 2: ¿Qué es lo más importante para ti en una relación?")
    print("a) La comunicación y el respeto mutuo")
    print("b) El apoyo incondicional y la confianza")
    print("c) La pasión y la emoción de estar juntos")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Mayo Aihara"] += 1
        character_scores["Yuzu Aihara"] += 1
        character_scores["Sara Tachibana"] += 1
    elif answer == "b":
        character_scores["Nijika Kugasaki"] += 1
        character_scores["Himeko Momokino"] += 1
        character_scores["Harumi Sae"] += 1
    elif answer == "c":
        character_scores["Shou Aihara"] += 1
        character_scores["Yuzu Aihara"] += 1

    print("\nPregunta 3: ¿Cómo manejas los problemas personales?")
    print("a) Trato de hablar sobre ellos con los demás")
    print("b) Prefiero enfrentar los problemas por mí misma")
    print("c) Suelo guardarme los sentimientos y actuar con frialdad")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Mayo Aihara"] += 1
        character_scores["Nijika Kugasaki"] += 1
    elif answer == "b":
        character_scores["Harumi Sae"] += 1
        character_scores["Sara Tachibana"] += 1
    elif answer == "c":
        character_scores["Shou Aihara"] += 1
        character_scores["Mayo Aihara"] += 1

    print("\nPregunta 4: ¿Qué tipo de persona eres en un grupo?")
    print("a) Siempre trato de liderar y motivar al grupo")
    print("b) Soy alguien que ofrece consejos y apoyo")
    print("c) Me gusta seguir y aportar cuando es necesario")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Mayo Aihara"] += 1
        character_scores["Harumi Sae"] += 1
    elif answer == "b":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Nijika Kugasaki"] += 1
        character_scores["Himeko Momokino"] += 1
    elif answer == "c":
        character_scores["Shou Aihara"] += 1
        character_scores["Sara Tachibana"] += 1

    print("\nPregunta 5: ¿Qué harías si te enamoras de alguien?")
    print("a) Lucharé por ella, sin importar lo que pase")
    print("b) Me tomaré mi tiempo y analizaré la situación")
    print("c) Intentaré mantener mis sentimientos bajo control")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Shou Aihara"] += 1
    elif answer == "b":
        character_scores["Mayo Aihara"] += 1
        character_scores["Nijika Kugasaki"] += 1
    elif answer == "c":
        character_scores["Harumi Sae"] += 1
        character_scores["Sara Tachibana"] += 1

    print("\nPregunta 6: ¿Cómo manejas los conflictos en una relación?")
    print("a) Prefiero resolverlos a través del diálogo abierto")
    print("b) Suelo distanciarme y pensar en la situación")
    print("c) A veces, la mejor opción es ignorar el conflicto")
    answer = input("Tu elección (a/b/c): ").lower()
    if answer == "a":
        character_scores["Yuzu Aihara"] += 1
        character_scores["Nijika Kugasaki"] += 1
    elif answer == "b":
        character_scores["Mayo Aihara"] += 1
        character_scores["Sara Tachibana"] += 1
    elif answer == "c":
        character_scores["Shou Aihara"] += 1
        character_scores["Harumi Sae"] += 1

    # Determinamos el personaje con más puntos
    max_score = max(character_scores.values())
    top_characters = [char for char, score in character_scores.items() if score == max_score]

    print("\nEres más como:")
    for character in top_characters:
        print("-", character)

if __name__ == "__main__":
    main()
