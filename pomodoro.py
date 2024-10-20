import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        time_format = f'{mins:02d}:{secs:02d}'
        print(time_format, end='\r')
        time.sleep(1)
        total_seconds -= 1
    print("00:00")

def pomodoro_cycle(work_duration, short_break_duration, long_break_duration, cycles):
    for cycle in range(1, cycles + 1):
        print(f"Ciclo {cycle} de {cycles}")
        print("Tiempo de trabajo!")
        countdown(work_duration)
        print("Tiempo de descanso corto!")
        countdown(short_break_duration)
        clear_console()
        if cycle % 4 == 0:
            print("Tiempo de descanso largo!")
            countdown(long_break_duration)
            clear_console()

def main():
    while True:
        clear_console()
        try:
            work_duration = int(input("Introduce la duración del trabajo (minutos): "))
            short_break_duration = int(input("Introduce la duración del descanso corto (minutos): "))
            long_break_duration = int(input("Introduce la duración del descanso largo (minutos): "))
            cycles = int(input("Ingrese el número de ciclos: "))
            
            pomodoro_cycle(work_duration, short_break_duration, long_break_duration, cycles)
            
            restart = input("¿Quieres establecer otro temporizador? (s/n): ").lower()
            if restart != 's':
                break
        except ValueError:
            print("Por favor, introduce un número válido.")
            time.sleep(2)
            continue

if __name__ == "__main__":
    main()
