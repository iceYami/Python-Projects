import tkinter as tk
from tkinter import messagebox
import random
import time
from tkinter.simpledialog import askinteger, askstring

# Lista de bromas
jokes = [
    "¡Tu PC decidió irse de vacaciones!",
    "¿Seguro que ese archivo es importante?",
    "Tu CPU está a punto de pedir una huelga.",
    "Error 404: ¡Tu inteligencia no se encuentra!",
    "Advertencia: ¡Tu café está a punto de enfriarse!",
    "Felicidades, has desbloqueado el nivel... ninguno.",
    "Oops... parece que has roto el internet.",
    "¿Te has planteado apagar y encender tu cerebro?",
    "El sistema se ha actualizado... pero no te has dado cuenta.",
    "Cuidado, ¡estás a punto de instalar el caos!"
]

# Función para mostrar ventana emergente
def show_joke(joke_type="info", joke_text=""):
    if joke_type == "info":
        messagebox.showinfo("Broma", joke_text)
    elif joke_type == "warning":
        messagebox.showwarning("Advertencia", joke_text)
    elif joke_type == "error":
        messagebox.showerror("Error", joke_text)

# Función principal para gestionar las bromas
def start_jokes():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    
    # Preguntar al usuario cuántas bromas quiere ver
    joke_count = askinteger("Número de bromas", "¿Cuántas bromas quieres que te salgan?", minvalue=1, maxvalue=len(jokes))
    if joke_count is None:  # Si cancela
        return
    
    # Preguntar intervalo entre ventanas
    interval = askinteger("Intervalo", "¿Cada cuántos segundos quieres que salten las bromas?", minvalue=1, maxvalue=60)
    if interval is None:
        return
    
    # Preguntar el tipo de ventana
    joke_type = askstring("Tipo de broma", "Escribe el tipo de broma: 'info', 'warning', o 'error'.")
    if joke_type not in ["info", "warning", "error"]:
        joke_type = "info"  # Valor por defecto si el usuario no escribe un tipo válido

    # Mostrar las bromas de acuerdo al número e intervalo
    for _ in range(joke_count):
        joke = random.choice(jokes)  # Selecciona una broma aleatoria
        show_joke(joke_type, joke)
        time.sleep(interval)  # Espera el intervalo especificado antes de la siguiente broma

# Menú principal para iniciar las bromas
def main_menu():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    while True:
        # Menú con opciones
        option = messagebox.askquestion("Menú de Bromas", "¿Quieres empezar con las bromas?", icon='question')
        
        if option == 'yes':
            start_jokes()
        else:
            messagebox.showinfo("Salir", "¡Hasta luego! Recuerda que las bromas no se van por mucho tiempo.")
            break

if __name__ == "__main__":
    main_menu()
