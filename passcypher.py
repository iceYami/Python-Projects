from cryptography.fernet import Fernet

def generar_clave(password):
    return Fernet.generate_key()

def cifrar_archivo(archivo, clave):
    f = Fernet(clave)
    with open(archivo, 'rb') as file:
        data = file.read()
    encrypted_data = f.encrypt(data)
    with open(archivo + '.encrypted', 'wb') as file:
        file.write(encrypted_data)

def descifrar_archivo(archivo, clave):
    f = Fernet(clave)
    with open(archivo, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(archivo.replace('.encrypted', ''), 'wb') as file:
        file.write(decrypted_data)

if __name__ == "__main__":
    password = input("Introduce la contraseña: ").encode()
    clave = generar_clave(password)
    archivo_a_cifrar = input("Introduce la ruta del archivo a cifrar: ")
    cifrar_archivo(archivo_a_cifrar, clave)
    print("Archivo prtegido.")
