#Crea una variable de tipo string llamada name . Imprime en consola el valor de dicha variable con todas sus letras en minúsculas, exceptuando la primera, que debe encontrarse en mayúsculas.
name = 'CodigoFacilito'
formatted_name = name[0].upper() + name[1:].lower()
print(formatted_name)
