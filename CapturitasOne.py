import os
import time
import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pyautogui
import argparse
import sys
from typing import Optional, List
import json
import threading
import queue

class ScreenCaptureManager:
    def __init__(self):
        self.is_capturing = False
        self.capture_count = 0
        self.start_time = None
        self.images = []
        self.stop_event = threading.Event()
        
    def get_default_paths(self) -> dict:
        """Obtiene las rutas por defecto del sistema"""
        home = Path.home()
        paths = {
            'desktop': home / 'Desktop',
            'documents': home / 'Documents', 
            'downloads': home / 'Downloads',
            'pictures': home / 'Pictures',
            'current': Path.cwd()
        }
        
        # Verificar que las rutas existen
        available_paths = {}
        for name, path in paths.items():
            if path.exists():
                available_paths[name] = path
            elif name == 'current':
                available_paths[name] = path
                
        return available_paths
    
    def select_output_path(self, custom_path: Optional[str] = None) -> Path:
        """Permite seleccionar la ruta de salida"""
        if custom_path:
            path = Path(custom_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"✓ Directorio creado: {path}")
                except Exception as e:
                    print(f"✗ Error creando directorio: {e}")
                    return self.select_output_path()
            return path
        
        # Mostrar opciones por defecto
        paths = self.get_default_paths()
        print("\n📁 Rutas disponibles:")
        for i, (name, path) in enumerate(paths.items(), 1):
            print(f"{i}. {name.capitalize()}: {path}")
        print(f"{len(paths) + 1}. Especificar ruta personalizada")
        
        while True:
            try:
                choice = input(f"\nSelecciona una opción (1-{len(paths) + 1}): ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(paths):
                        selected_path = list(paths.values())[choice - 1]
                        return selected_path
                    elif choice == len(paths) + 1:
                        custom = input("Introduce la ruta personalizada: ").strip()
                        return self.select_output_path(custom)
                
                print("Opción no válida. Intenta de nuevo.")
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                sys.exit(0)
    
    def create_output_folder(self, base_path: Path) -> Path:
        """Crea una carpeta específica para esta sesión de capturas"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"screen_captures_{timestamp}"
        output_folder = base_path / folder_name
        output_folder.mkdir(exist_ok=True)
        return output_folder
    
    def add_timestamp_to_image(self, image: Image.Image, timestamp: str) -> Image.Image:
        """Añade marca de tiempo a la imagen"""
        draw = ImageDraw.Draw(image)
        
        # Intentar usar una fuente del sistema
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)  # macOS
            except:
                font = ImageFont.load_default()
        
        # Posición del texto (esquina superior derecha)
        text_bbox = draw.textbbox((0, 0), timestamp, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = image.width - text_width - 10
        y = 10
        
        # Fondo semitransparente para el texto
        padding = 5
        draw.rectangle([x-padding, y-padding, x+text_width+padding, y+text_height+padding], 
                      fill=(0, 0, 0, 180))
        
        # Texto
        draw.text((x, y), timestamp, fill=(255, 255, 255), font=font)
        
        return image
    
    def capture_screen(self, add_timestamp: bool = True) -> Optional[Image.Image]:
        """Captura la pantalla completa"""
        try:
            screenshot = pyautogui.screenshot()
            
            if add_timestamp:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                screenshot = self.add_timestamp_to_image(screenshot, timestamp)
            
            return screenshot
        except Exception as e:
            print(f"✗ Error capturando pantalla: {e}")
            return None
    
    def save_individual_images(self, output_folder: Path, format: str = 'PNG') -> List[Path]:
        """Guarda las imágenes individuales"""
        saved_files = []
        
        for i, img in enumerate(self.images):
            filename = f"capture_{i+1:04d}.{format.lower()}"
            filepath = output_folder / filename
            
            try:
                img.save(filepath, format=format)
                saved_files.append(filepath)
            except Exception as e:
                print(f"✗ Error guardando {filename}: {e}")
        
        return saved_files
    
    def create_gif(self, output_folder: Path, duration: int = 1000) -> Optional[Path]:
        """Crea un GIF animado con todas las capturas"""
        if not self.images:
            return None
        
        gif_path = output_folder / "screen_capture_animation.gif"
        
        try:
            # Redimensionar imágenes para el GIF (opcional, para reducir tamaño)
            resized_images = []
            for img in self.images:
                # Reducir a 50% del tamaño original
                new_size = (img.width // 2, img.height // 2)
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                resized_images.append(resized_img)
            
            resized_images[0].save(
                gif_path,
                save_all=True,
                append_images=resized_images[1:],
                duration=duration,
                loop=0
            )
            
            return gif_path
        except Exception as e:
            print(f"✗ Error creando GIF: {e}")
            return None
    
    def create_contact_sheet(self, output_folder: Path, cols: int = 4) -> Optional[Path]:
        """Crea una hoja de contacto con miniaturas de todas las capturas"""
        if not self.images:
            return None
        
        # Calcular dimensiones
        thumb_size = (200, 150)
        margin = 10
        
        rows = (len(self.images) + cols - 1) // cols
        sheet_width = cols * thumb_size[0] + (cols + 1) * margin
        sheet_height = rows * thumb_size[1] + (rows + 1) * margin
        
        # Crear imagen de la hoja de contacto
        contact_sheet = Image.new('RGB', (sheet_width, sheet_height), 'white')
        
        try:
            for i, img in enumerate(self.images):
                row = i // cols
                col = i % cols
                
                # Crear miniatura
                thumbnail = img.copy()
                thumbnail.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                
                # Calcular posición
                x = col * thumb_size[0] + (col + 1) * margin
                y = row * thumb_size[1] + (row + 1) * margin
                
                # Pegar miniatura
                contact_sheet.paste(thumbnail, (x, y))
            
            sheet_path = output_folder / "contact_sheet.png"
            contact_sheet.save(sheet_path)
            return sheet_path
            
        except Exception as e:
            print(f"✗ Error creando hoja de contacto: {e}")
            return None
    
    def save_session_info(self, output_folder: Path, saved_files: List[Path]):
        """Guarda información de la sesión"""
        info = {
            'session_start': self.start_time.isoformat() if self.start_time else None,
            'session_end': datetime.datetime.now().isoformat(),
            'total_captures': self.capture_count,
            'output_folder': str(output_folder),
            'individual_files': [str(f) for f in saved_files]
        }
        
        info_path = output_folder / "session_info.json"
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
    
    def display_progress(self, current: int, total: int):
        """Muestra progreso de captura"""
        progress = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f'\r📸 Capturando: |{bar}| {current}/{total} ({progress:.1f}%)', end='')
    
    def start_capture(self, duration_minutes: float, interval: float = 1.0, 
                     output_path: Optional[str] = None):
        """Inicia el proceso de captura"""
        print("🎬 Iniciando capturador de pantalla avanzado")
        print(f"⏱️  Duración: {duration_minutes} minutos")
        print(f"📊 Intervalo: {interval} segundos")
        
        # Seleccionar ruta de salida
        base_path = self.select_output_path(output_path)
        output_folder = self.create_output_folder(base_path)
        
        print(f"📁 Guardando en: {output_folder}")
        
        # Calcular totales
        total_seconds = duration_minutes * 60
        total_captures = int(total_seconds / interval)
        
        print(f"📷 Se realizarán aproximadamente {total_captures} capturas")
        print("\n⏳ Iniciando en 3 segundos...")
        time.sleep(3)
        
        # Iniciar captura
        self.is_capturing = True
        self.start_time = datetime.datetime.now()
        self.capture_count = 0
        self.images = []
        
        try:
            end_time = time.time() + total_seconds
            
            while time.time() < end_time and self.is_capturing:
                screenshot = self.capture_screen()
                if screenshot:
                    self.images.append(screenshot)
                    self.capture_count += 1
                    self.display_progress(self.capture_count, total_captures)
                
                time.sleep(interval)
            
            print(f"\n✅ Captura completada! {self.capture_count} imágenes capturadas")
            
        except KeyboardInterrupt:
            print(f"\n⏹️  Captura detenida por el usuario. {self.capture_count} imágenes capturadas")
        
        finally:
            self.is_capturing = False
            
            if self.images:
                print("\n💾 Procesando y guardando archivos...")
                
                # Guardar imágenes individuales
                saved_files = self.save_individual_images(output_folder)
                print(f"✅ {len(saved_files)} imágenes guardadas")
                
                # Crear GIF
                gif_path = self.create_gif(output_folder)
                if gif_path:
                    print(f"🎞️  GIF creado: {gif_path}")
                
                # Crear hoja de contacto
                contact_path = self.create_contact_sheet(output_folder)
                if contact_path:
                    print(f"📄 Hoja de contacto creada: {contact_path}")
                
                # Guardar información de sesión
                self.save_session_info(output_folder, saved_files)
                
                print(f"\n🎉 Proceso completado exitosamente!")
                print(f"📂 Todos los archivos en: {output_folder}")
                
                # Mostrar resumen
                total_size = sum(f.stat().st_size for f in saved_files) / (1024 * 1024)
                print(f"📊 Resumen:")
                print(f"   • Capturas realizadas: {self.capture_count}")
                print(f"   • Tamaño total: {total_size:.1f} MB")
                print(f"   • Duración real: {(datetime.datetime.now() - self.start_time).total_seconds():.1f} segundos")


def main():
    # Verificar dependencias
    try:
        import pyautogui
        import PIL
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias.")
        print("Instala con: pip install pillow pyautogui")
        sys.exit(1)
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Capturador de pantalla avanzado')
    parser.add_argument('--duration', '-d', type=float, default=None,
                       help='Duración en minutos')
    parser.add_argument('--interval', '-i', type=float, default=1.0,
                       help='Intervalo entre capturas en segundos (default: 1.0)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Ruta de salida personalizada')
    parser.add_argument('--no-timestamp', action='store_true',
                       help='No añadir marca de tiempo a las imágenes')
    
    args = parser.parse_args()
    
    # Crear instancia del capturador
    capturer = ScreenCaptureManager()
    
    # Obtener duración si no se especificó
    if args.duration is None:
        while True:
            try:
                duration_input = input("🕐 Duración en minutos: ").strip()
                duration = float(duration_input)
                if duration > 0:
                    break
                else:
                    print("La duración debe ser mayor que 0")
            except ValueError:
                print("Por favor introduce un número válido")
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                sys.exit(0)
    else:
        duration = args.duration
    
    # Iniciar captura
    capturer.start_capture(
        duration_minutes=duration,
        interval=args.interval,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
