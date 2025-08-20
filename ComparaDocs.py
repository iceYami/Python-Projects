#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparador de Documentos Avanzado
Permite comparar documentos de texto, Word, PDF y generar reportes detallados
Autor: Assistant
Fecha: 2025
"""

import os
import sys
import difflib
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import unicodedata

# Importaciones opcionales con manejo de errores
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import mammoth
    MAMMOTH_AVAILABLE = True
except ImportError:
    MAMMOTH_AVAILABLE = False

class Colors:
    """Códigos de colores para terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class DocumentComparator:
    """Clase principal para comparar documentos"""
    
    def __init__(self):
        self.supported_formats = {
            '.txt': 'Texto plano',
            '.md': 'Markdown',
            '.py': 'Python',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.xml': 'XML',
            '.json': 'JSON',
            '.csv': 'CSV',
            '.log': 'Log'
        }
        
        if DOCX_AVAILABLE:
            self.supported_formats['.docx'] = 'Word Document'
        if PDF_AVAILABLE:
            self.supported_formats['.pdf'] = 'PDF'
        if MAMMOTH_AVAILABLE:
            self.supported_formats['.doc'] = 'Word Document (Legacy)'
    
    def print_header(self):
        """Imprime el header del programa"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}     📄 COMPARADOR DE DOCUMENTOS AVANZADO 📄{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.YELLOW}Formatos soportados:{Colors.END}")
        for ext, desc in self.supported_formats.items():
            print(f"  • {ext} - {desc}")
        print()
    
    def get_default_paths(self) -> Dict[str, str]:
        """Obtiene rutas por defecto del sistema"""
        home = Path.home()
        paths = {
            'desktop': home / 'Desktop',
            'downloads': home / 'Downloads',
            'documents': home / 'Documents',
            'home': home,
            'current': Path.cwd()
        }
        
        # Verificar que las rutas existan
        available_paths = {}
        for name, path in paths.items():
            if path.exists():
                available_paths[name] = str(path)
        
        return available_paths
    
    def select_file(self, file_number: int) -> Optional[str]:
        """Permite seleccionar un archivo"""
        print(f"\n{Colors.BOLD}=== SELECCIÓN DE ARCHIVO {file_number} ==={Colors.END}")
        
        # Mostrar opciones por defecto
        default_paths = self.get_default_paths()
        print(f"\n{Colors.GREEN}Opciones rápidas:{Colors.END}")
        for i, (name, path) in enumerate(default_paths.items(), 1):
            print(f"  {i}. {name.capitalize()}: {path}")
        
        print(f"  {len(default_paths) + 1}. Introducir ruta personalizada")
        print(f"  {len(default_paths) + 2}. Cancelar")
        
        try:
            choice = input(f"\n{Colors.YELLOW}Selecciona una opción: {Colors.END}")
            choice = int(choice.strip())
            
            if choice == len(default_paths) + 2:
                return None
            elif choice == len(default_paths) + 1:
                custom_path = input(f"{Colors.YELLOW}Introduce la ruta completa del archivo: {Colors.END}")
                return custom_path.strip()
            elif 1 <= choice <= len(default_paths):
                selected_path = list(default_paths.values())[choice - 1]
                return self.browse_directory(selected_path)
            else:
                print(f"{Colors.RED}Opción inválida{Colors.END}")
                return self.select_file(file_number)
        
        except ValueError:
            print(f"{Colors.RED}Por favor, introduce un número válido{Colors.END}")
            return self.select_file(file_number)
    
    def browse_directory(self, directory: str) -> Optional[str]:
        """Navega por un directorio para seleccionar archivo"""
        try:
            path = Path(directory)
            if not path.exists():
                print(f"{Colors.RED}La ruta no existe: {directory}{Colors.END}")
                return None
            
            files = []
            dirs = []
            
            for item in path.iterdir():
                if item.is_file() and item.suffix.lower() in self.supported_formats:
                    files.append(item)
                elif item.is_dir() and not item.name.startswith('.'):
                    dirs.append(item)
            
            print(f"\n{Colors.BLUE}Contenido de: {directory}{Colors.END}")
            print(f"{Colors.YELLOW}Directorios:{Colors.END}")
            
            options = []
            
            # Opción para subir directorio
            if path.parent != path:
                options.append(("📁 ..", str(path.parent)))
                print(f"  1. 📁 .. (directorio padre)")
            
            # Mostrar directorios
            for i, dir_path in enumerate(dirs, len(options) + 1):
                options.append((f"📁 {dir_path.name}", str(dir_path)))
                print(f"  {i}. 📁 {dir_path.name}")
            
            print(f"\n{Colors.GREEN}Archivos:{Colors.END}")
            # Mostrar archivos
            for i, file_path in enumerate(files, len(options) + 1):
                options.append((f"📄 {file_path.name}", str(file_path)))
                print(f"  {i}. 📄 {file_path.name}")
            
            if not options:
                print(f"{Colors.RED}No hay archivos compatibles en este directorio{Colors.END}")
                return None
            
            print(f"\n  {len(options) + 1}. Volver al menú anterior")
            
            try:
                choice = input(f"\n{Colors.YELLOW}Selecciona una opción: {Colors.END}")
                choice = int(choice.strip())
                
                if choice == len(options) + 1:
                    return None
                elif 1 <= choice <= len(options):
                    selected_item = options[choice - 1][1]
                    selected_path = Path(selected_item)
                    
                    if selected_path.is_dir():
                        return self.browse_directory(str(selected_path))
                    else:
                        return str(selected_path)
                else:
                    print(f"{Colors.RED}Opción inválida{Colors.END}")
                    return self.browse_directory(directory)
            
            except ValueError:
                print(f"{Colors.RED}Por favor, introduce un número válido{Colors.END}")
                return self.browse_directory(directory)
        
        except Exception as e:
            print(f"{Colors.RED}Error al navegar por el directorio: {e}{Colors.END}")
            return None
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Lee el contenido de un archivo según su tipo"""
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"{Colors.RED}El archivo no existe: {file_path}{Colors.END}")
                return None
            
            extension = path.suffix.lower()
            
            if extension == '.pdf':
                return self.read_pdf(file_path)
            elif extension == '.docx':
                return self.read_docx(file_path)
            elif extension == '.doc':
                return self.read_doc(file_path)
            else:
                return self.read_text_file(file_path)
        
        except Exception as e:
            print(f"{Colors.RED}Error al leer el archivo {file_path}: {e}{Colors.END}")
            return None
    
    def read_text_file(self, file_path: str) -> Optional[str]:
        """Lee archivos de texto plano"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        print(f"{Colors.RED}No se pudo leer el archivo con ninguna codificación{Colors.END}")
        return None
    
    def read_pdf(self, file_path: str) -> Optional[str]:
        """Lee archivos PDF"""
        if not PDF_AVAILABLE:
            print(f"{Colors.RED}PyPDF2 no está disponible. Instala con: pip install PyPDF2{Colors.END}")
            return None
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"{Colors.RED}Error al leer PDF: {e}{Colors.END}")
            return None
    
    def read_docx(self, file_path: str) -> Optional[str]:
        """Lee archivos Word (.docx)"""
        if not DOCX_AVAILABLE:
            print(f"{Colors.RED}python-docx no está disponible. Instala con: pip install python-docx{Colors.END}")
            return None
        
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"{Colors.RED}Error al leer DOCX: {e}{Colors.END}")
            return None
    
    def read_doc(self, file_path: str) -> Optional[str]:
        """Lee archivos Word legacy (.doc)"""
        if not MAMMOTH_AVAILABLE:
            print(f"{Colors.RED}mammoth no está disponible. Instala con: pip install mammoth{Colors.END}")
            return None
        
        try:
            with open(file_path, 'rb') as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                return result.value
        except Exception as e:
            print(f"{Colors.RED}Error al leer DOC: {e}{Colors.END}")
            return None
    
    def normalize_text(self, text: str) -> str:
        """Normaliza el texto para mejor comparación"""
        # Normalizar unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar espacios al inicio y final de líneas
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        
        return '\n'.join(lines)
    
    def compare_documents(self, text1: str, text2: str, file1: str, file2: str) -> Tuple[str, str]:
        """Compara dos documentos y genera reportes"""
        print(f"\n{Colors.BLUE}Comparando documentos...{Colors.END}")
        
        # Normalizar textos
        text1_norm = self.normalize_text(text1)
        text2_norm = self.normalize_text(text2)
        
        # Dividir en líneas
        lines1 = text1_norm.split('\n')
        lines2 = text2_norm.split('\n')
        
        # Generar diferencias
        diff = list(difflib.unified_diff(
            lines1, lines2,
            fromfile=f"Archivo 1: {Path(file1).name}",
            tofile=f"Archivo 2: {Path(file2).name}",
            lineterm='',
            n=3
        ))
        
        # Generar reporte HTML con diferencias resaltadas
        html_diff = difflib.HtmlDiff()
        diff_html = html_diff.make_file(
            lines1, lines2,
            fromdesc=f"Archivo 1: {Path(file1).name}",
            todesc=f"Archivo 2: {Path(file2).name}",
            context=True,
            numlines=3
        )
        
        # Generar reporte de cambios
        changes_report = self.generate_changes_report(lines1, lines2, file1, file2)
        
        return diff_html, changes_report
    
    def generate_changes_report(self, lines1: List[str], lines2: List[str], file1: str, file2: str) -> str:
        """Genera un reporte detallado de cambios"""
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        
        report = []
        report.append("="*80)
        report.append("REPORTE DE CAMBIOS ENTRE DOCUMENTOS")
        report.append("="*80)
        report.append(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Archivo 1: {file1}")
        report.append(f"Archivo 2: {file2}")
        report.append(f"Total de líneas archivo 1: {len(lines1)}")
        report.append(f"Total de líneas archivo 2: {len(lines2)}")
        report.append("")
        
        # Estadísticas
        opcodes = matcher.get_opcodes()
        additions = deletions = modifications = 0
        
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'insert':
                additions += (j2 - j1)
            elif tag == 'delete':
                deletions += (i2 - i1)
            elif tag == 'replace':
                modifications += max(i2 - i1, j2 - j1)
        
        report.append("ESTADÍSTICAS DE CAMBIOS:")
        report.append(f"- Líneas añadidas: {additions}")
        report.append(f"- Líneas eliminadas: {deletions}")
        report.append(f"- Líneas modificadas: {modifications}")
        report.append(f"- Similitud: {matcher.ratio()*100:.2f}%")
        report.append("")
        
        # Detalle de cambios
        report.append("DETALLE DE CAMBIOS:")
        report.append("-" * 50)
        
        change_number = 1
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                continue
            
            report.append(f"\n{change_number}. CAMBIO - {tag.upper()}:")
            
            if tag == 'delete':
                report.append(f"   Ubicación en archivo 1: líneas {i1+1} a {i2}")
                report.append("   Contenido eliminado:")
                for i in range(i1, i2):
                    report.append(f"   - {lines1[i]}")
            
            elif tag == 'insert':
                report.append(f"   Ubicación en archivo 2: líneas {j1+1} a {j2}")
                report.append("   Contenido añadido:")
                for j in range(j1, j2):
                    report.append(f"   + {lines2[j]}")
            
            elif tag == 'replace':
                report.append(f"   Ubicación en archivo 1: líneas {i1+1} a {i2}")
                report.append(f"   Ubicación en archivo 2: líneas {j1+1} a {j2}")
                report.append("   Contenido original:")
                for i in range(i1, i2):
                    report.append(f"   - {lines1[i]}")
                report.append("   Contenido nuevo:")
                for j in range(j1, j2):
                    report.append(f"   + {lines2[j]}")
            
            change_number += 1
        
        if change_number == 1:
            report.append("No se encontraron diferencias entre los documentos.")
        
        return '\n'.join(report)
    
    def save_reports(self, html_diff: str, changes_report: str, file1: str, file2: str) -> Tuple[str, str]:
        """Guarda los reportes en archivos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Crear directorio de reportes
        reports_dir = Path('reportes_comparacion')
        reports_dir.mkdir(exist_ok=True)
        
        # Nombres de archivos
        file1_name = Path(file1).stem
        file2_name = Path(file2).stem
        
        html_filename = f"diferencias_{file1_name}_vs_{file2_name}_{timestamp}.html"
        txt_filename = f"reporte_cambios_{file1_name}_vs_{file2_name}_{timestamp}.txt"
        
        html_path = reports_dir / html_filename
        txt_path = reports_dir / txt_filename
        
        # Guardar archivos
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_diff)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(changes_report)
            
            return str(html_path), str(txt_path)
        
        except Exception as e:
            print(f"{Colors.RED}Error al guardar reportes: {e}{Colors.END}")
            return None, None
    
    def run(self):
        """Ejecuta el comparador"""
        self.print_header()
        
        try:
            # Seleccionar primer archivo
            print(f"{Colors.BOLD}Selecciona el primer documento:{Colors.END}")
            file1 = self.select_file(1)
            if not file1:
                print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
                return
            
            # Leer primer archivo
            print(f"\n{Colors.BLUE}Leyendo archivo 1: {file1}{Colors.END}")
            text1 = self.read_file(file1)
            if not text1:
                print(f"{Colors.RED}No se pudo leer el primer archivo{Colors.END}")
                return
            
            # Seleccionar segundo archivo
            print(f"\n{Colors.BOLD}Selecciona el segundo documento:{Colors.END}")
            file2 = self.select_file(2)
            if not file2:
                print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
                return
            
            # Leer segundo archivo
            print(f"\n{Colors.BLUE}Leyendo archivo 2: {file2}{Colors.END}")
            text2 = self.read_file(file2)
            if not text2:
                print(f"{Colors.RED}No se pudo leer el segundo archivo{Colors.END}")
                return
            
            # Comparar documentos
            html_diff, changes_report = self.compare_documents(text1, text2, file1, file2)
            
            # Guardar reportes
            html_path, txt_path = self.save_reports(html_diff, changes_report, file1, file2)
            
            if html_path and txt_path:
                print(f"\n{Colors.GREEN}✅ Comparación completada exitosamente!{Colors.END}")
                print(f"\n{Colors.BOLD}Archivos generados:{Colors.END}")
                print(f"📄 Reporte HTML con diferencias resaltadas: {Colors.CYAN}{html_path}{Colors.END}")
                print(f"📄 Reporte de cambios detallado: {Colors.CYAN}{txt_path}{Colors.END}")
                
                # Mostrar resumen en consola
                print(f"\n{Colors.YELLOW}Resumen de la comparación:{Colors.END}")
                summary_lines = changes_report.split('\n')[:20]  # Primeras 20 líneas
                for line in summary_lines:
                    print(line)
                
                if len(changes_report.split('\n')) > 20:
                    print(f"\n{Colors.MAGENTA}... (ver reporte completo en {txt_path}){Colors.END}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operación cancelada por el usuario{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")

def main():
    """Función principal"""
    try:
        comparator = DocumentComparator()
        comparator.run()
    except Exception as e:
        print(f"{Colors.RED}Error crítico: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
