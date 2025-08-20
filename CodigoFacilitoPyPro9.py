#Crea una matriz de 3x3 e imprime en consola True si: El primer elemento de cada fila es un número par. El nombre de la matriz debe ser matrix.
matrix = [
    [2, 5, 8],
    [4, 7, 1],
    [6, 3, 9]
]
is_first_elements_even = all(row[0] % 2 == 0 for row in matrix)
print(is_first_elements_even)
