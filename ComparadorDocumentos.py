#!/usr/bin/env python3
"""
Comparador de Documentos Profesional
====================================

Este script compara dos documentos de diferentes formatos (DOC, DOCX, RTF, TXT, PDF)
y genera un reporte HTML con las diferencias resaltadas visualmente.

Características:
- Soporte para múltiples formatos de archivo
- Comparación inteligente línea por línea
- Reporte HTML con colores diferenciados
- Estadísticas de diferencias
- Manejo robusto de errores
- Interfaz de línea de comandos amigable

Autor: Claude AI
Fecha: 2025
"""

import argparse
import difflib
import html
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import re

# Importaciones para lectura de documentos
try:
    import docx
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import pypandoc
    PANDOC_AVAILABLE = True
except ImportError:
    PANDOC_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from striprtf.striprtf import rtf_to_text
    RTF_AVAILABLE = True
except ImportError:
    RTF_AVAILABLE = False


class DocumentReader:
    """Clase para leer diferentes tipos de documentos"""
    
    @staticmethod
    def read_txt(filepath: str) -> str:
        """Lee archivos de texto plano"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    @staticmethod
    def read_docx(filepath: str) -> str:
        """Lee archivos DOCX"""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx no está instalado. Instálalo con: pip install python-docx")
        
        doc = Document(filepath)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    
    @staticmethod
    def read_rtf(filepath: str) -> str:
        """Lee archivos RTF"""
        if not RTF_AVAILABLE:
            raise ImportError("striprtf no está instalado. Instálalo con: pip install striprtf")
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            rtf_content = f.read()
        return rtf_to_text(rtf_content)
    
    @staticmethod
    def read_pdf(filepath: str) -> str:
        """Lee archivos PDF"""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 no está instalado. Instálalo con: pip install PyPDF2")
        
        text = []
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    @staticmethod
    def read_doc(filepath: str) -> str:
        """Lee archivos DOC usando pandoc"""
        if not PANDOC_AVAILABLE:
            raise ImportError("pypandoc no está instalado. Instálalo con: pip install pypandoc")
        
        return pypandoc.convert_file(filepath, 'plain')
    
    @staticmethod
    def read_document(filepath: str) -> str:
        """Lee un documento basándose en su extensión"""
        filepath = Path(filepath)
        extension = filepath.suffix.lower()
        
        readers = {
            '.txt': DocumentReader.read_txt,
            '.docx': DocumentReader.read_docx,
            '.rtf': DocumentReader.read_rtf,
            '.pdf': DocumentReader.read_pdf,
            '.doc': DocumentReader.read_doc,
        }
        
        if extension not in readers:
            raise ValueError(f"Formato de archivo no soportado: {extension}")
        
        try:
            return readers[extension](str(filepath))
        except Exception as e:
            raise RuntimeError(f"Error al leer {filepath}: {str(e)}")


class DocumentComparator:
    """Clase principal para comparar documentos"""
    
    def __init__(self):
        self.html_template = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparación de Documentos</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .legend {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .legend-item {{
            display: inline-block;
            margin: 5px 15px;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        .content {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .diff-content {{
            font-family: 'Courier New', monospace;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .added {{
            background-color: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
            padding: 2px 5px;
            margin: 2px 0;
        }}
        
        .removed {{
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
            padding: 2px 5px;
            margin: 2px 0;
            text-decoration: line-through;
        }}
        
        .changed {{
            background-color: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
            padding: 2px 5px;
            margin: 2px 0;
        }}
        
        .line-number {{
            color: #666;
            font-size: 0.9em;
            margin-right: 10px;
            user-select: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📄 Comparación de Documentos</h1>
        <p>Análisis detallado de diferencias entre documentos</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_lines}</div>
            <div>Líneas Totales</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{added_lines}</div>
            <div>Líneas Añadidas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{removed_lines}</div>
            <div>Líneas Eliminadas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{similarity:.1f}%</div>
            <div>Similitud</div>
        </div>
    </div>
    
    <div class="legend">
        <h3>📋 Leyenda:</h3>
        <span class="legend-item added">+ Contenido añadido (Documento 2)</span>
        <span class="legend-item removed">- Contenido eliminado (Documento 1)</span>
        <span class="legend-item changed">~ Contenido modificado</span>
    </div>
    
    <div class="content">
        <h2>🔍 Diferencias Encontradas</h2>
        <div class="diff-content">
{diff_content}
        </div>
    </div>
    
    <div class="content" style="margin-top: 20px;">
        <h3>ℹ️ Información de Archivos</h3>
        <p><strong>Documento 1:</strong> {file1}</p>
        <p><strong>Documento 2:</strong> {file2}</p>
        <p><strong>Generado el:</strong> {timestamp}</p>
    </div>
</body>
</html>
        '''
    
    def normalize_text(self, text: str) -> List[str]:
        """Normaliza el texto para una mejor comparación"""
        # Normalizar espacios y saltos de línea
        text = re.sub(r'\r\n|\r', '\n', text)
        text = re.sub(r'\n+', '\n', text)
        text = text.strip()
        
        # Dividir en líneas y limpiar
        lines = text.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Eliminar espacios extras pero mantener la estructura
            line = ' '.join(line.split())
            if line:  # Solo añadir líneas no vacías
                normalized_lines.append(line)
        
        return normalized_lines
    
    def generate_html_diff(self, lines1: List[str], lines2: List[str]) -> Tuple[str, dict]:
        """Genera un diff HTML con estadísticas"""
        differ = difflib.unified_diff(
            lines1, lines2,
            fromfile='Documento 1',
            tofile='Documento 2',
            lineterm=''
        )
        
        diff_content = []
        added_lines = 0
        removed_lines = 0
        line_number = 0
        
        for line in differ:
            line_number += 1
            escaped_line = html.escape(line)
            
            if line.startswith('+++') or line.startswith('---'):
                continue
            elif line.startswith('@@'):
                diff_content.append(f'<div class="line-number">Línea {line_number}</div>')
                continue
            elif line.startswith('+'):
                added_lines += 1
                content = escaped_line[1:].strip()
                diff_content.append(f'<div class="added">+ {content}</div>')
            elif line.startswith('-'):
                removed_lines += 1
                content = escaped_line[1:].strip()
                diff_content.append(f'<div class="removed">- {content}</div>')
            else:
                content = escaped_line.strip()
                if content:
                    diff_content.append(f'<div>{content}</div>')
        
        # Calcular similitud
        similarity = difflib.SequenceMatcher(None, lines1, lines2).ratio() * 100
        
        stats = {
            'total_lines': len(lines1) + len(lines2),
            'added_lines': added_lines,
            'removed_lines': removed_lines,
            'similarity': similarity
        }
        
        return '\n'.join(diff_content), stats
    
    def compare_documents(self, file1: str, file2: str, output_file: str = None) -> str:
        """Compara dos documentos y genera un reporte HTML"""
        print(f"🔍 Leyendo documento 1: {file1}")
        try:
            text1 = DocumentReader.read_document(file1)
        except Exception as e:
            raise RuntimeError(f"Error al leer {file1}: {str(e)}")
        
        print(f"🔍 Leyendo documento 2: {file2}")
        try:
            text2 = DocumentReader.read_document(file2)
        except Exception as e:
            raise RuntimeError(f"Error al leer {file2}: {str(e)}")
        
        print("⚙️ Normalizando textos...")
        lines1 = self.normalize_text(text1)
        lines2 = self.normalize_text(text2)
        
        print("🔄 Generando comparación...")
        diff_content, stats = self.generate_html_diff(lines1, lines2)
        
        # Generar nombre de archivo de salida si no se especifica
        if output_file is None:
            output_file = f"comparacion_{Path(file1).stem}_vs_{Path(file2).stem}.html"
        
        # Generar HTML final
        from datetime import datetime
        html_output = self.html_template.format(
            diff_content=diff_content,
            file1=os.path.basename(file1),
            file2=os.path.basename(file2),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **stats
        )
        
        print(f"💾 Guardando reporte: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        return output_file


def print_requirements():
    """Imprime los requisitos del sistema"""
    print("📋 Dependencias requeridas:")
    print("pip install python-docx pypandoc PyPDF2 striprtf")
    print("\nNota: Para archivos DOC también necesitas pandoc instalado en tu sistema")


def main():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(
        description='Compara dos documentos y genera un reporte HTML con las diferencias',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Formatos soportados:
  .txt    - Texto plano
  .docx   - Microsoft Word (requiere python-docx)
  .doc    - Microsoft Word antiguo (requiere pandoc)
  .rtf    - Rich Text Format (requiere striprtf)
  .pdf    - PDF (requiere PyPDF2)

Ejemplos de uso:
  python comparador.py documento1.docx documento2.docx
  python comparador.py -o resultado.html archivo1.txt archivo2.txt
  python comparador.py --requirements  # Mostrar dependencias
        '''
    )
    
    parser.add_argument('file1', nargs='?', help='Primer documento a comparar')
    parser.add_argument('file2', nargs='?', help='Segundo documento a comparar')
    parser.add_argument('-o', '--output', help='Archivo de salida HTML')
    parser.add_argument('--requirements', action='store_true', 
                       help='Mostrar dependencias requeridas')
    
    args = parser.parse_args()
    
    if args.requirements:
        print_requirements()
        return
    
    if not args.file1 or not args.file2:
        parser.print_help()
        return
    
    # Verificar que los archivos existen
    for filepath in [args.file1, args.file2]:
        if not os.path.exists(filepath):
            print(f"❌ Error: El archivo '{filepath}' no existe")
            return
    
    try:
        comparator = DocumentComparator()
        output_file = comparator.compare_documents(args.file1, args.file2, args.output)
        
        print(f"\n✅ Comparación completada exitosamente!")
        print(f"📄 Reporte generado: {output_file}")
        print(f"🌐 Abre el archivo HTML en tu navegador para ver los resultados")
        
    except Exception as e:
        print(f"❌ Error durante la comparación: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
