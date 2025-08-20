import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
import sys
from pathlib import Path

class PythonToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Converter")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Variables
        self.selected_files = []
        self.output_dir = ""
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
        # Verificar PyInstaller
        self.check_pyinstaller()
    
    def setup_style(self):
        """Configurar estilo moderno"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores modernos
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        style.configure('Modern.TButton', padding=(10, 5))
        
    def create_widgets(self):
        """Crear la interfaz gráfica"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Python to EXE Converter", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de selección de archivos
        files_frame = ttk.LabelFrame(main_frame, text="Selección de Archivos Python", 
                                    padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        
        # Botones de selección rápida
        quick_buttons_frame = ttk.Frame(files_frame)
        quick_buttons_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(quick_buttons_frame, text="Desktop", 
                  command=lambda: self.browse_folder(Path.home() / "Desktop"),
                  style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(quick_buttons_frame, text="Documents", 
                  command=lambda: self.browse_folder(Path.home() / "Documents"),
                  style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_buttons_frame, text="Downloads", 
                  command=lambda: self.browse_folder(Path.home() / "Downloads"),
                  style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quick_buttons_frame, text="Examinar...", 
                  command=self.browse_files,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=5)
        
        # Lista de archivos seleccionados
        ttk.Label(files_frame, text="Archivos seleccionados:", 
                 style='Heading.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        self.files_listbox = tk.Listbox(files_frame, height=6, selectmode=tk.EXTENDED)
        self.files_listbox.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        files_scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, 
                                       command=self.files_listbox.yview)
        files_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), pady=(0, 10))
        self.files_listbox.config(yscrollcommand=files_scrollbar.set)
        
        # Botón para eliminar archivos seleccionados
        ttk.Button(files_frame, text="Eliminar seleccionados", 
                  command=self.remove_selected_files).grid(row=3, column=0, sticky=tk.W)
        
        # Sección de configuración de salida
        output_frame = ttk.LabelFrame(main_frame, text="Configuración de Salida", 
                                     padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Carpeta de salida:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_var = tk.StringVar()
        self.output_var.set(str(Path.home() / "Desktop"))
        self.output_dir = str(Path.home() / "Desktop")
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, state='readonly')
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Examinar", 
                  command=self.browse_output_folder).grid(row=0, column=2)
        
        # Opciones adicionales
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.onefile_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Un solo archivo ejecutable (--onefile)", 
                       variable=self.onefile_var).grid(row=0, column=0, sticky=tk.W)
        
        self.noconsole_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Sin ventana de consola (--noconsole)", 
                       variable=self.noconsole_var).grid(row=1, column=0, sticky=tk.W)
        
        # Botón de conversión
        convert_frame = ttk.Frame(main_frame)
        convert_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.convert_button = ttk.Button(convert_frame, text="Convertir a EXE", 
                                        command=self.start_conversion,
                                        style='Modern.TButton')
        self.convert_button.pack(pady=10)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Log de salida
        log_frame = ttk.LabelFrame(main_frame, text="Log de Conversión", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def check_pyinstaller(self):
        """Verificar si PyInstaller está instalado"""
        try:
            subprocess.run([sys.executable, '-c', 'import PyInstaller'], 
                          check=True, capture_output=True)
            self.log_message("✓ PyInstaller detectado correctamente")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_message("⚠ PyInstaller no está instalado")
            response = messagebox.askyesno(
                "PyInstaller requerido",
                "PyInstaller no está instalado. ¿Desea instalarlo automáticamente?\n"
                "Esto puede tardar unos minutos."
            )
            if response:
                self.install_pyinstaller()
    
    def install_pyinstaller(self):
        """Instalar PyInstaller automáticamente"""
        def install():
            try:
                self.log_message("Instalando PyInstaller...")
                self.progress.start()
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                                      capture_output=True, text=True)
                self.progress.stop()
                
                if result.returncode == 0:
                    self.log_message("✓ PyInstaller instalado correctamente")
                else:
                    self.log_message(f"✗ Error instalando PyInstaller: {result.stderr}")
            except Exception as e:
                self.progress.stop()
                self.log_message(f"✗ Error instalando PyInstaller: {str(e)}")
        
        threading.Thread(target=install, daemon=True).start()
    
    def browse_files(self):
        """Examinar archivos Python"""
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def browse_folder(self, default_path=None):
        """Examinar carpeta para buscar archivos Python"""
        if default_path and default_path.exists():
            initialdir = str(default_path)
        else:
            initialdir = str(Path.home())
            
        folder = filedialog.askdirectory(title="Seleccionar carpeta", initialdir=initialdir)
        if folder:
            py_files = list(Path(folder).glob("*.py"))
            added_count = 0
            for file in py_files:
                file_str = str(file)
                if file_str not in self.selected_files:
                    self.selected_files.append(file_str)
                    self.files_listbox.insert(tk.END, file.name)
                    added_count += 1
            
            if added_count > 0:
                self.log_message(f"✓ Se agregaron {added_count} archivos Python de {folder}")
            else:
                self.log_message(f"No se encontraron archivos Python nuevos en {folder}")
    
    def remove_selected_files(self):
        """Eliminar archivos seleccionados de la lista"""
        selected_indices = self.files_listbox.curselection()
        for index in reversed(selected_indices):
            del self.selected_files[index]
            self.files_listbox.delete(index)
    
    def browse_output_folder(self):
        """Examinar carpeta de salida"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder:
            self.output_dir = folder
            self.output_var.set(folder)
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def start_conversion(self):
        """Iniciar proceso de conversión en hilo separado"""
        if not self.selected_files:
            messagebox.showwarning("Sin archivos", "Por favor selecciona al menos un archivo Python.")
            return
        
        self.convert_button.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.convert_files, daemon=True)
        thread.start()
    
    def convert_files(self):
        """Convertir archivos Python a EXE"""
        successful_conversions = 0
        total_files = len(self.selected_files)
        
        self.log_message(f"Iniciando conversión de {total_files} archivo(s)...")
        
        for i, file_path in enumerate(self.selected_files, 1):
            try:
                self.log_message(f"[{i}/{total_files}] Procesando: {os.path.basename(file_path)}")
                
                # Construir comando PyInstaller
                cmd = [sys.executable, '-m', 'PyInstaller']
                
                if self.onefile_var.get():
                    cmd.append('--onefile')
                
                if self.noconsole_var.get():
                    cmd.append('--noconsole')
                
                cmd.extend(['--distpath', self.output_dir])
                cmd.extend(['--workpath', os.path.join(self.output_dir, 'build')])
                cmd.extend(['--specpath', os.path.join(self.output_dir, 'spec')])
                cmd.append('--clean')
                cmd.append(file_path)
                
                # Ejecutar PyInstaller
                result = subprocess.run(cmd, capture_output=True, text=True, 
                                      cwd=os.path.dirname(file_path))
                
                if result.returncode == 0:
                    successful_conversions += 1
                    self.log_message(f"✓ {os.path.basename(file_path)} convertido exitosamente")
                else:
                    self.log_message(f"✗ Error convirtiendo {os.path.basename(file_path)}")
                    if result.stderr:
                        self.log_message(f"Error: {result.stderr[:200]}...")
                        
            except Exception as e:
                self.log_message(f"✗ Excepción procesando {os.path.basename(file_path)}: {str(e)}")
        
        # Finalizar
        self.progress.stop()
        self.convert_button.config(state='normal')
        
        self.log_message(f"\n=== Conversión completada ===")
        self.log_message(f"Exitosos: {successful_conversions}/{total_files}")
        self.log_message(f"Archivos EXE guardados en: {self.output_dir}")
        
        if successful_conversions > 0:
            messagebox.showinfo("Conversión completada", 
                              f"Se convirtieron {successful_conversions} de {total_files} archivos exitosamente.\n"
                              f"Los archivos EXE están en: {self.output_dir}")
        else:
            messagebox.showerror("Conversión fallida", 
                               "No se pudo convertir ningún archivo. Revisa el log para más detalles.")

def main():
    root = tk.Tk()
    app = PythonToExeConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
