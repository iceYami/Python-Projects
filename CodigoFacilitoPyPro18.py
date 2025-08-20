#Dada la siguiente lista de números enteros lista = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] genera un string con los primeros 5 elementos de la lista. Cada valor debe encontrarse separado por un espacio. Imprime en consola dicho string.
lista = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
resultado = " ".join(lista[:5])
print(resultado)
