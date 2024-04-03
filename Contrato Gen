# Generador de contratos de MG

def generar_contrato():

    empresa_nombre = input("Nombre de la empresa: ")
    empresa_cif = input("CIF/NIF/NIE de la empresa: ")
    trabajador_nombre = input("Nombre del trabajador: ")
    trabajador_dni = input("DNI del trabajador: ")
    fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ")
    puesto = input("Puesto: ")
    salario = input("Salario: ")
    
 nombre_archivo = f"Contrato_{trabajador_nombre.replace(' ', '_')}.doc"
 with open(nombre_archivo, "w") as archivo:
 archivo.write(contenido_contrato)
 print(f"El contrato se ha generado correctamente como '{nombre_archivo}' en la carpeta del código.")

def main():
    print("Contratos Gen")
    generar_contrato()

    while True:
        respuesta = input("¿Quieres generar otro? (s/n): ").lower()
        if respuesta != "s":
            break
        generar_contrato()

if __name__ == "__main__":
    main()
