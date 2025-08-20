#Define una tupla de Longitud 3 (Cualquier tipo de dato) e imprime en consola el último elemento. El nombre de la tupla debe ser my_tuple.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pares = tuple(x for x in numbers if x % 2 == 0)
print(pares)
