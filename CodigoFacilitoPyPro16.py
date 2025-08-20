#Crea una variable de tipo string llamada name e imprime en consola True o False si el primer o último carácter son vocales.
name = "Ejemplo"
if name[0].lower() in "aeiou" or name[-1].lower() in "aeiou":
    print(True)
else:
    print(False)
