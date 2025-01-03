import random

def generar_contraseña(longitud_minima=14):
    if longitud_minima <= 14:
        raise ValueError("La longitud de la contraseña debe ser mayor a 14 caracteres.")
    
    mayúsculas = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    minúsculas = "abcdefghijklmnñopqrstuvwxyz"
    dígitos = "0123456789"
    caracteres_especiales = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    longitud = random.randint(longitud_minima + 1, longitud_minima + 10)
    
    contraseña = [
        random.choice(mayúsculas),
        random.choice(minúsculas),
        random.choice(dígitos),
        random.choice(caracteres_especiales)
    ]
    
    todos_los_caracteres = mayúsculas + minúsculas + dígitos + caracteres_especiales
    
    while len(contraseña) < longitud:
        caracter = random.choice(todos_los_caracteres)
        if caracter not in contraseña:
            contraseña.append(caracter)
    random.shuffle(contraseña)
    
    return ''.join(contraseña)

print(generar_contraseña(14))
