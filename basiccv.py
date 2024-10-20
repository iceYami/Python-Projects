class CV:
    def __init__(self):
        self.nombre_apellidos = ""
        self.email = ""
        self.telefono = ""
        self.estudios = []
        self.experiencia = []
        self.certificados = []
        self.idiomas = []

    def agregar_nombre_apellidos(self, nombre_apellidos):
        self.nombre_apellidos = nombre_apellidos

    def agregar_email(self, email):
        self.email = email

    def agregar_telefono(self, telefono):
        self.telefono = telefono

    def agregar_estudio(self, estudio):
        self.estudios.append(estudio)

    def agregar_experiencia(self, experiencia):
        self.experiencia.append(experiencia)

    def agregar_certificado(self, certificado):
        self.certificados.append(certificado)

    def agregar_idioma(self, idioma):
        self.idiomas.append(idioma)

    def limpiar_datos(self):
        self.nombre_apellidos = ""
        self.email = ""
        self.telefono = ""
        self.estudios = []
        self.experiencia = []
        self.certificados = []
        self.idiomas = []

    def generar_cv(self):
        print("----- CV de", self.nombre_apellidos, "-----")
        print("Email:", self.email)
        print("Teléfono:", self.telefono)
        print("\nEstudios:")
        for estudio in self.estudios:
            print("- Año:", estudio[0], "|", "Título:", estudio[1])
        print("\nExperiencia Laboral:")
        for exp in self.experiencia:
            print("- Año:", exp[0], "|", "Descripción:", exp[1])
        if self.certificados:
            print("\nCertificados:")
            for certificado in self.certificados:
                print("-", certificado)
        if self.idiomas:
            print("\nIdiomas:")
            for idioma in self.idiomas:
                print("-", idioma)

print("¡Bienvenido al Creador Básico de CVs de MG!")

cv = CV()

nombre_apellidos = input("Introduce tu nombre y apellidos: ")
cv.agregar_nombre_apellidos(nombre_apellidos)

email = input("Introduce tu email: ")
cv.agregar_email(email)
telefono = input("Introduce tu número de teléfono: ")
cv.agregar_telefono(telefono)

while True:
    año_estudio = input("Introduce el año en el que cursaste tu formación: ")
    titulo_estudio = input("Introduce el título de tu formación: ")
    cv.agregar_estudio((año_estudio, titulo_estudio))
    agregar_otro = input("¿Quieres añadir otro estudio? (s/n): ")
    if agregar_otro.lower() != 's':
        break

while True:
    año_experiencia = input("Introduce el intervalo de tu experiencia laboral: ")
    descripcion_experiencia = input("Introduce la descripción de esta experiencia laboral: ")
    cv.agregar_experiencia((año_experiencia, descripcion_experiencia))
    agregar_otra = input("¿Quieres añadir otra experiencia laboral? (s/n): ")
    if agregar_otra.lower() != 's':
        break

agregar_certificados = input("¿Quieres añadir certificados? (s/n): ")
if agregar_certificados.lower() == 's':
    while True:
        certificado = input("Introduce un certificado: ")
        cv.agregar_certificado(certificado)
        agregar_otro = input("¿Quieres añadir otro certificado? (s/n): ")
        if agregar_otro.lower() != 's':
            break

agregar_idiomas = input("¿Quieres añadir idiomas? (s/n): ")
if agregar_idiomas.lower() == 's':
    while True:
        idioma = input("Introduce un idioma: ")
        cv.agregar_idioma(idioma)
        agregar_otro = input("¿Quieres añadir otro idioma? (s/n): ")
        if agregar_otro.lower() != 's':
            break

cv.generar_cv()

borrar_datos = input("¿Deseas borrar los datos introducidos? (s/n): ")
if borrar_datos.lower() == 's':
    cv.limpiar_datos()
    print("Los datos han sido borrados.")

ver_cv = input("¿Deseas ver el CV generado? (s/n): ")
if ver_cv.lower() == 's':
    cv.generar_cv()
else:
    print("Gracias por utilizar el Creador Básico de CV de MG. ¡Hasta luego!")
