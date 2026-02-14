import ctypes
import time

# Cargar user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Funciones necesarias
GetCursorPos = user32.GetCursorPos
SetCursorPos = user32.SetCursorPos

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

def get_mouse_position():
    point = POINT()
    GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def move_mouse(x, y):
    SetCursorPos(x, y)

def keep_awake(interval=60):
    print("Moviendo el ratón cada", interval, "segundos. Ctrl+C para salir.")
    toggle = True
    
    while True:
        x, y = get_mouse_position()
        
        if toggle:
            move_mouse(x + 1, y)
        else:
            move_mouse(x - 1, y)
        
        toggle = not toggle
        time.sleep(interval)

if __name__ == "__main__":
    keep_awake(60)  # Cambia el intervalo en segundos si quieres
