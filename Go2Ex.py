import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import threading

class PythonToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor Python a EXE")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.selected_file = ""
        self.output_dir = ""
        
        self.create_widgets()
        self.check_pyinstaller()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Convertidor Python a EXE", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de archivo
        ttk.Label(main_frame, text="Archivo Python:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.file_entry = ttk.Entry(main_frame, width=50)
        self.file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text="Seleccionar", 
                  command=self.select_file).grid(row=1, column=2, pady=5)
        
        # Directorio de salida
        ttk.Label(main_frame, text="Directorio de salida:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_entry = ttk.Entry(main_frame, width=50)
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text="Seleccionar", 
                  command=self.select_output_dir).grid(row=2, column=2, pady=5)
        
        # Opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        
        # Variables para checkboxes
        self.onefile_var = tk.BooleanVar(value=True)
        self.noconsole_var = tk.BooleanVar(value=False)
        self.debug_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Archivo único (--onefile)", 
                       variable=self.onefile_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Sin consola (--noconsole/--windowed)", 
                       variable=self.noconsole_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Modo debug (--debug)", 
                       variable=self.debug_var).grid(row=2, column=0, sticky=tk.W)
        
        # Icono
        ttk.Label(options_frame, text="Icono (opcional):").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        icon_frame = ttk.Frame(options_frame)
        icon_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        icon_frame.columnconfigure(0, weight=1)
        
        self.icon_entry = ttk.Entry(icon_frame)
        self.icon_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(icon_frame, text="Seleccionar", 
                  command=self.select_icon).grid(row=0, column=1)
        
        # Botón convertir
        self.convert_button = ttk.Button(main_frame, text="Convertir a EXE", 
                                       command=self.convert_to_exe)
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log de conversión", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def check_pyinstaller(self):
        """Verifica si PyInstaller está instalado"""
        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                          capture_output=True, check=True)
            self.log("PyInstaller está instalado y listo para usar.")
        except subprocess.CalledProcessError:
            self.log("PyInstaller no está instalado.")
            self.log("Instalando PyInstaller...")
            self.install_pyinstaller()
    
    def install_pyinstaller(self):
        """Instala PyInstaller"""
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                          capture_output=True, check=True)
            self.log("PyInstaller instalado correctamente.")
        except subprocess.CalledProcessError as e:
            self.log(f"Error al instalar PyInstaller: {e}")
            messagebox.showerror("Error", "No se pudo instalar PyInstaller. Instálalo manualmente con: pip install pyinstaller")
    
    def select_file(self):
        """Selecciona el archivo Python"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            
            # Establecer directorio de salida por defecto
            if not self.output_dir:
                default_output = os.path.join(os.path.dirname(file_path), "dist")
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, default_output)
    
    def select_output_dir(self):
        """Selecciona el directorio de salida"""
        dir_path = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if dir_path:
            self.output_dir = dir_path
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)
    
    def select_icon(self):
        """Selecciona el icono"""
        icon_path = filedialog.askopenfilename(
            title="Seleccionar icono",
            filetypes=[("Icon files", "*.ico"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if icon_path:
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, icon_path)
    
    def log(self, message):
        """Añade mensaje al log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def convert_to_exe(self):
        """Convierte el archivo Python a EXE"""
        if not self.selected_file:
            messagebox.showerror("Error", "Selecciona un archivo Python")
            return
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "El archivo seleccionado no existe")
            return
        
        # Ejecutar conversión en hilo separado
        self.convert_button.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self._convert_thread)
        thread.start()
    
    def _convert_thread(self):
        """Hilo para la conversión"""
        try:
            # Construir comando PyInstaller
            cmd = [sys.executable, "-m", "PyInstaller"]
            
            # Opciones
            if self.onefile_var.get():
                cmd.append("--onefile")
            
            if self.noconsole_var.get():
                cmd.append("--noconsole")
            
            if self.debug_var.get():
                cmd.append("--debug")
            
            # Directorio de salida
            output_dir = self.output_entry.get()
            if output_dir:
                cmd.extend(["--distpath", output_dir])
            
            # Icono
            icon_path = self.icon_entry.get()
            if icon_path and os.path.exists(icon_path):
                cmd.extend(["--icon", icon_path])
            
            # Archivo a convertir
            cmd.append(self.selected_file)
            
            self.log(f"Ejecutando: {' '.join(cmd)}")
            self.log("Iniciando conversión...")
            
            # Ejecutar PyInstaller
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(self.selected_file)
            )
            
            # Leer salida en tiempo real
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log("¡Conversión completada exitosamente!")
                exe_name = os.path.splitext(os.path.basename(self.selected_file))[0] + ".exe"
                exe_path = os.path.join(output_dir or "dist", exe_name)
                self.log(f"Archivo EXE creado: {exe_path}")
                messagebox.showinfo("Éxito", f"Conversión completada.\nArchivo creado: {exe_path}")
            else:
                self.log("Error durante la conversión")
                messagebox.showerror("Error", "Error durante la conversión. Revisa el log para más detalles.")
        
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Error durante la conversión: {str(e)}")
        
        finally:
            # Restaurar interfaz
            self.root.after(0, self._restore_ui)
    
    def _restore_ui(self):
        """Restaura la interfaz después de la conversión"""
        self.progress.stop()
        self.convert_button.config(state='normal')

def main():
    root = tk.Tk()
    app = PythonToExeConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
