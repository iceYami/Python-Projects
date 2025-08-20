#Define una lista de longitud 10 de Strings. La lista debe tener por nombre strings_list Genera una sub lista con los 3 primeros y últimos elementos. Imprime en consola la nueva sub lista.
strings_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
sublist = strings_list[:3] + strings_list[-3:]
print(sublist)
