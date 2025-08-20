#Define una función que nos permita conocer si todos los elementos de una lista son el mismo. La función debe tener por nombre “iguales” y debe recibir como argumento un listado de números enteros. La función debe retornar True o False si todos los elementos de la lista son el mimos.
#- La función retornará None si la lista se encuentra vacía o solo posee un elemento.
def iguales(lista):
    if len(lista) <= 1:
        return None
    for i in range(1, len(lista)):
        if lista[i] != lista[0]:
            return False
    return True
