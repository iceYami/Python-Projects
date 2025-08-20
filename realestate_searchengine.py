import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import re
from urllib.parse import urljoin, quote
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BuscadorInmobiliario:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador Inmobiliario Integral España")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.resultados = []
        self.df_resultados = pd.DataFrame()
        
        # Headers para requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Portales inmobiliarios
        self.portales = {
            'idealista': 'https://www.idealista.com',
            'fotocasa': 'https://www.fotocasa.es',
            'pisos': 'https://www.pisos.com',
            'habitaclia': 'https://www.habitaclia.com',
            'inmofactory': 'https://www.inmofactory.com',
            'yaencontre': 'https://www.yaencontre.com',
            'kyero': 'https://www.kyero.com/es',
            'tecnocasa': 'https://www.tecnocasa.es'
        }
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(main_frame, text="🏠 Buscador Inmobiliario Integral España",
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtros de Búsqueda", padding="10")
        filtros_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        filtros_frame.columnconfigure(1, weight=1)
        filtros_frame.columnconfigure(3, weight=1)
        
        # Tipo de operación
        ttk.Label(filtros_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.tipo_var = tk.StringVar(value="alquiler")
        tipo_combo = ttk.Combobox(filtros_frame, textvariable=self.tipo_var, 
                                 values=["alquiler", "venta"], state="readonly", width=15)
        tipo_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Ubicación
        ttk.Label(filtros_frame, text="Ubicación:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.ubicacion_var = tk.StringVar()
        ubicacion_entry = ttk.Entry(filtros_frame, textvariable=self.ubicacion_var, width=20)
        ubicacion_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Precio mínimo y máximo
        ttk.Label(filtros_frame, text="Precio mín (€):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.precio_min_var = tk.StringVar()
        precio_min_entry = ttk.Entry(filtros_frame, textvariable=self.precio_min_var, width=15)
        precio_min_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(10, 0))
        
        ttk.Label(filtros_frame, text="Precio máx (€):").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.precio_max_var = tk.StringVar()
        precio_max_entry = ttk.Entry(filtros_frame, textvariable=self.precio_max_var, width=20)
        precio_max_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Habitaciones y metros
        ttf.Label(filtros_frame, text="Habitaciones:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.habitaciones_var = tk.StringVar()
        habitaciones_combo = ttk.Combobox(filtros_frame, textvariable=self.habitaciones_var,
                                         values=["", "1", "2", "3", "4", "5+"], state="readonly", width=15)
        habitaciones_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(10, 0))
        
        ttk.Label(filtros_frame, text="Metros mín:").grid(row=2, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.metros_var = tk.StringVar()
        metros_entry = ttk.Entry(filtros_frame, textvariable=self.metros_var, width=20)
        metros_entry.grid(row=2, column=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Transporte público
        self.transporte_var = tk.BooleanVar()
        transporte_check = ttk.Checkbutton(filtros_frame, text="Solo con transporte público cercano",
                                          variable=self.transporte_var)
        transporte_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Vivienda protegida
        self.protegida_var = tk.BooleanVar()
        protegida_check = ttk.Checkbutton(filtros_frame, text="Incluir vivienda protegida",
                                         variable=self.protegida_var)
        protegida_check.grid(row=3, column=2, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Botón de búsqueda
        buscar_btn = tk.Button(main_frame, text="🔍 Buscar Propiedades", 
                              command=self.iniciar_busqueda, bg='#3498db', fg='white',
                              font=('Arial', 12, 'bold'), pady=5)
        buscar_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Frame de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="5")
        resultados_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(resultados_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña de lista
        self.frame_lista = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_lista, text="Lista de Propiedades")
        
        # Treeview para mostrar resultados
        columns = ('Portal', 'Título', 'Precio', 'Ubicación', 'Habitaciones', 'Metros', 'Transporte')
        self.tree = ttk.Treeview(self.frame_lista, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(self.frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(self.frame_lista, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.rowconfigure(0, weight=1)
        
        # Pestaña de gráficos
        self.frame_graficos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_graficos, text="Gráficos y Análisis")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Label de estado
        self.estado_label = tk.Label(main_frame, text="Listo para buscar", 
                                    bg='#f0f0f0', fg='#7f8c8d')
        self.estado_label.grid(row=5, column=0, columnspan=3)
        
        main_frame.rowconfigure(3, weight=1)
        
    def iniciar_busqueda(self):
        # Validar campos
        if not self.ubicacion_var.get().strip():
            messagebox.showerror("Error", "Por favor, introduce una ubicación")
            return
            
        # Limpiar resultados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.resultados = []
        
        # Iniciar búsqueda en hilo separado
        thread = threading.Thread(target=self.buscar_propiedades)
        thread.daemon = True
        thread.start()
        
    def actualizar_estado(self, mensaje):
        self.estado_label.config(text=mensaje)
        self.root.update_idletasks()
        
    def buscar_propiedades(self):
        self.progress.start()
        self.actualizar_estado("Iniciando búsqueda...")
        
        try:
            # Buscar en cada portal
            for portal, url_base in self.portales.items():
                self.actualizar_estado(f"Buscando en {portal.title()}...")
                try:
                    resultados_portal = self.buscar_en_portal(portal, url_base)
                    self.resultados.extend(resultados_portal)
                    self.actualizar_lista()
                except Exception as e:
                    print(f"Error buscando en {portal}: {e}")
                    
                time.sleep(1)  # Pausa entre portales
            
            # Buscar vivienda protegida si está seleccionado
            if self.protegida_var.get():
                self.actualizar_estado("Buscando vivienda protegida...")
                try:
                    resultados_protegida = self.buscar_vivienda_protegida()
                    self.resultados.extend(resultados_protegida)
                    self.actualizar_lista()
                except Exception as e:
                    print(f"Error buscando vivienda protegida: {e}")
                    
            self.filtrar_y_ordenar()
            self.crear_graficos()
            self.actualizar_estado(f"Búsqueda completada. {len(self.resultados)} propiedades encontradas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la búsqueda: {e}")
            self.actualizar_estado("Error en la búsqueda")
        finally:
            self.progress.stop()
    
    def buscar_en_portal(self, portal, url_base):
        resultados = []
        
        try:
            # Construir URL de búsqueda según el portal
            if portal == 'idealista':
                resultados = self.buscar_idealista(url_base)
            elif portal == 'fotocasa':
                resultados = self.buscar_fotocasa(url_base)
            elif portal == 'pisos':
                resultados = self.buscar_pisos(url_base)
            else:
                resultados = self.buscar_generico(portal, url_base)
                
        except Exception as e:
            print(f"Error específico en {portal}: {e}")
            
        return resultados
    
    def buscar_idealista(self, url_base):
        resultados = []
        try:
            # Construir URL de Idealista
            ubicacion = quote(self.ubicacion_var.get().replace(' ', '-').lower())
            tipo = 'alquiler' if self.tipo_var.get() == 'alquiler' else 'venta'
            
            url = f"{url_base}/{tipo}-viviendas/{ubicacion}/"
            
            # Añadir parámetros de filtro
            params = []
            if self.precio_min_var.get():
                params.append(f"precio-desde_{self.precio_min_var.get()}")
            if self.precio_max_var.get():
                params.append(f"precio-hasta_{self.precio_max_var.get()}")
            if self.habitaciones_var.get():
                params.append(f"habitaciones_{self.habitaciones_var.get()}")
            if self.metros_var.get():
                params.append(f"superficie-desde_{self.metros_var.get()}")
                
            if params:
                url += "?" + "&".join(params)
                
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer propiedades (estructura típica de Idealista)
            propiedades = soup.find_all('div', class_='item-info-container')
            
            for prop in propiedades[:20]:  # Limitar a 20 por portal
                try:
                    titulo_elem = prop.find('a', class_='item-link')
                    precio_elem = prop.find('span', class_='item-price')
                    ubicacion_elem = prop.find('span', class_='item-detail')
                    
                    if titulo_elem and precio_elem:
                        titulo = titulo_elem.get_text(strip=True)
                        precio = self.extraer_precio(precio_elem.get_text(strip=True))
                        ubicacion = ubicacion_elem.get_text(strip=True) if ubicacion_elem else "N/A"
                        
                        # Extraer habitaciones y metros
                        habitaciones = self.extraer_habitaciones(titulo)
                        metros = self.extraer_metros(titulo)
                        
                        # Verificar transporte si está solicitado
                        transporte = "N/A"
                        if self.transporte_var.get():
                            transporte = self.verificar_transporte(ubicacion)
                        
                        resultados.append({
                            'portal': 'Idealista',
                            'titulo': titulo,
                            'precio': precio,
                            'ubicacion': ubicacion,
                            'habitaciones': habitaciones,
                            'metros': metros,
                            'transporte': transporte,
                            'url': urljoin(url_base, titulo_elem.get('href', ''))
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error en Idealista: {e}")
            
        return resultados
    
    def buscar_fotocasa(self, url_base):
        resultados = []
        try:
            ubicacion = quote(self.ubicacion_var.get())
            tipo = 'alquiler' if self.tipo_var.get() == 'alquiler' else 'comprar'
            
            url = f"{url_base}/es/{tipo}/viviendas/{ubicacion}/todas-las-zonas/l"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar propiedades en Fotocasa
            propiedades = soup.find_all('div', class_='re-CardPackPremium')
            if not propiedades:
                propiedades = soup.find_all('article', class_='re-Card')
                
            for prop in propiedades[:15]:
                try:
                    titulo_elem = prop.find('span', class_='re-Card-title')
                    precio_elem = prop.find('span', class_='re-Card-price')
                    
                    if titulo_elem and precio_elem:
                        titulo = titulo_elem.get_text(strip=True)
                        precio = self.extraer_precio(precio_elem.get_text(strip=True))
                        ubicacion = self.ubicacion_var.get()
                        
                        habitaciones = self.extraer_habitaciones(titulo)
                        metros = self.extraer_metros(titulo)
                        transporte = "N/A"
                        
                        if self.transporte_var.get():
                            transporte = self.verificar_transporte(ubicacion)
                        
                        resultados.append({
                            'portal': 'Fotocasa',
                            'titulo': titulo,
                            'precio': precio,
                            'ubicacion': ubicacion,
                            'habitaciones': habitaciones,
                            'metros': metros,
                            'transporte': transporte,
                            'url': url
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error en Fotocasa: {e}")
            
        return resultados
    
    def buscar_pisos(self, url_base):
        # Implementación similar para Pisos.com
        return self.buscar_generico('Pisos.com', url_base)
    
    def buscar_generico(self, portal, url_base):
        resultados = []
        try:
            # Búsqueda genérica para otros portales
            response = requests.get(url_base, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos comunes de propiedades
            enlaces = soup.find_all('a', href=True)
            
            for enlace in enlaces[:10]:
                href = enlace.get('href', '')
                texto = enlace.get_text(strip=True)
                
                # Filtrar enlaces que parezcan propiedades
                if any(word in href.lower() for word in ['piso', 'casa', 'vivienda', 'alquiler', 'venta']):
                    if len(texto) > 20:  # Filtrar títulos muy cortos
                        precio = self.extraer_precio(texto)
                        if precio > 0:
                            resultados.append({
                                'portal': portal,
                                'titulo': texto[:100],
                                'precio': precio,
                                'ubicacion': self.ubicacion_var.get(),
                                'habitaciones': self.extraer_habitaciones(texto),
                                'metros': self.extraer_metros(texto),
                                'transporte': "N/A",
                                'url': urljoin(url_base, href)
                            })
                            
        except Exception as e:
            print(f"Error en búsqueda genérica para {portal}: {e}")
            
        return resultados
    
    def buscar_vivienda_protegida(self):
        resultados = []
        try:
            # URLs de organismos oficiales de vivienda protegida
            urls_oficiales = [
                'https://www.madrid.org/vivienda',
                'https://web.gencat.cat/ca/temes/habitatge',
                'https://www.juntadeandalucia.es/organismos/fomentoinfraestructurasyordenaciondelterritorio/areas/vivienda-rehabilitacion.html'
            ]
            
            for url in urls_oficiales:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar información de vivienda protegida
                    enlaces_vivienda = soup.find_all('a', href=True)
                    
                    for enlace in enlaces_vivienda[:5]:
                        href = enlace.get('href', '')
                        texto = enlace.get_text(strip=True)
                        
                        if any(word in texto.lower() for word in ['vivienda', 'protegida', 'social', 'alquiler']):
                            if len(texto) > 10:
                                resultados.append({
                                    'portal': 'Vivienda Protegida',
                                    'titulo': f"VPO - {texto[:80]}",
                                    'precio': 0,  # Precio a consultar
                                    'ubicacion': self.ubicacion_var.get(),
                                    'habitaciones': "N/A",
                                    'metros': "N/A",
                                    'transporte': "N/A",
                                    'url': urljoin(url, href)
                                })
                                
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error buscando vivienda protegida: {e}")
            
        return resultados
    
    def extraer_precio(self, texto):
        # Extraer precio del texto
        precio_match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*€', texto)
        if precio_match:
            precio_str = precio_match.group(1).replace('.', '').replace(',', '.')
            try:
                return float(precio_str)
            except:
                return 0
        return 0
    
    def extraer_habitaciones(self, texto):
        # Extraer número de habitaciones
        hab_match = re.search(r'(\d+)\s*(?:hab|dormitorio|habitación)', texto.lower())
        if hab_match:
            return hab_match.group(1)
        return "N/A"
    
    def extraer_metros(self, texto):
        # Extraer metros cuadrados
        metros_match = re.search(r'(\d+)\s*m²?', texto)
        if metros_match:
            return metros_match.group(1)
        return "N/A"
    
    def verificar_transporte(self, ubicacion):
        # Simulación de verificación de transporte público
        # En una implementación real, consultarías APIs de transporte público
        transportes = ["Metro L1", "Autobús 27", "Cercanías C4", "Metro L6", "Autobús EMT"]
        import random
        if random.random() > 0.3:  # 70% probabilidad de tener transporte
            return random.choice(transportes)
        return "No disponible"
    
    def filtrar_y_ordenar(self):
        # Filtrar resultados según criterios
        if not self.resultados:
            return
            
        resultados_filtrados = []
        
        precio_min = float(self.precio_min_var.get() or 0)
        precio_max = float(self.precio_max_var.get() or float('inf'))
        
        for resultado in self.resultados:
            precio = resultado['precio']
            
            # Filtro de precio
            if precio_min <= precio <= precio_max or precio == 0:
                # Filtro de habitaciones
                if (not self.habitaciones_var.get() or 
                    resultado['habitaciones'] == self.habitaciones_var.get() or 
                    resultado['habitaciones'] == "N/A"):
                    
                    # Filtro de transporte
                    if (not self.transporte_var.get() or 
                        resultado['transporte'] != "No disponible"):
                        
                        resultados_filtrados.append(resultado)
        
        # Ordenar por precio (los de precio 0 al final)
        self.resultados = sorted(resultados_filtrados, 
                               key=lambda x: (x['precio'] == 0, x['precio']))
    
    def actualizar_lista(self):
        # Actualizar la vista de lista
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for resultado in self.resultados[-50:]:  # Mostrar últimos 50
            precio_str = f"{resultado['precio']:,.0f}€" if resultado['precio'] > 0 else "Consultar"
            
            self.tree.insert('', 'end', values=(
                resultado['portal'],
                resultado['titulo'][:50] + "..." if len(resultado['titulo']) > 50 else resultado['titulo'],
                precio_str,
                resultado['ubicacion'][:30],
                resultado['habitaciones'],
                f"{resultado['metros']}m²" if resultado['metros'] != "N/A" else "N/A",
                resultado['transporte']
            ))
    
    def crear_graficos(self):
        # Limpiar frame de gráficos
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()
            
        if not self.resultados:
            return
            
        # Crear DataFrame
        df = pd.DataFrame(self.resultados)
        df_precios = df[df['precio'] > 0]  # Solo propiedades con precio
        
        if df_precios.empty:
            return
        
        # Configurar el estilo
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Crear figura con subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Análisis del Mercado Inmobiliario', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Distribución de precios por portal
        if len(df_precios) > 0:
            df_precios.boxplot(column='precio', by='portal', ax=ax1)
            ax1.set_title('Distribución de Precios por Portal')
            ax1.set_xlabel('Portal')
            ax1.set_ylabel('Precio (€)')
            ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Histograma de precios
        if len(df_precios) > 0:
            ax2.hist(df_precios['precio'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.set_title('Distribución de Precios')
            ax2.set_xlabel('Precio (€)')
            ax2.set_ylabel('Frecuencia')
        
        # Gráfico 3: Propiedades por portal
        conteo_portales = df['portal'].value_counts()
        ax3.pie(conteo_portales.values, labels=conteo_portales.index, autopct='%1.1f%%')
        ax3.set_title('Propiedades por Portal')
        
        # Gráfico 4: Relación precio-metros (si hay datos)
        df_metros = df_precios[df_precios['metros'] != "N/A"].copy()
        if not df_metros.empty:
            try:
                df_metros['metros_num'] = pd.to_numeric(df_metros['metros'], errors='coerce')
                df_metros = df_metros.dropna(subset=['metros_num'])
                
                if not df_metros.empty:
                    ax4.scatter(df_metros['metros_num'], df_metros['precio'], alpha=0.6)
                    ax4.set_xlabel('Metros cuadrados')
                    ax4.set_ylabel('Precio (€)')
                    ax4.set_title('Precio vs Metros cuadrados')
                    
                    # Línea de tendencia
                    z = np.polyfit(df_metros['metros_num'], df_metros['precio'], 1)
                    p = np.poly1d(z)
                    ax4.plot(df_metros['metros_num'], p(df_metros['metros_num']), "r--", alpha=0.8)
            except:
                ax4.text(0.5, 0.5, 'Datos insuficientes\npara el análisis', 
                        ha='center', va='center', transform=ax4.transAxes)
        else:
            ax4.text(0.5, 0.5, 'Sin datos de metros\ndisponibles', 
                    ha='center', va='center', transform=ax4.transAxes)
        
        plt.tight_layout()
        
        # Integrar en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar para interactuar con los gráficos
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, self.frame_graficos)
        toolbar.update()
        
        # Frame para estadísticas
        stats_frame = ttk.LabelFrame(self.frame_graficos, text="Estadísticas Generales", padding="10")
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Calcular estadísticas
        total_propiedades = len(df)
        promedio_precio = df_precios['precio'].mean() if not df_precios.empty else 0
        precio_min = df_precios['precio'].min() if not df_precios.empty else 0
        precio_max = df_precios['precio'].max() if not df_precios.empty else 0
        
        stats_text = f"""
        📊 Propiedades encontradas: {total_propiedades}
        💰 Precio promedio: {promedio_precio:,.0f}€
        📉 Precio mínimo: {precio_min:,.0f}€
        📈 Precio máximo: {precio_max:,.0f}€
        🏢 Portales consultados: {len(df['portal'].unique())}
        """
        
        stats_label = tk.Label(stats_frame, text=stats_text, justify=tk.LEFT, 
                              font=('Arial', 10), bg='white', relief=tk.SUNKEN, padx=10, pady=5)
        stats_label.pack(fill=tk.X)

def crear_menus(root, app):
    """Crear menús de la aplicación"""
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Menú Archivo
    archivo_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Exportar a Excel", command=lambda: app.exportar_excel())
    archivo_menu.add_command(label="Exportar a CSV", command=lambda: app.exportar_csv())
    archivo_menu.add_separator()
    archivo_menu.add_command(label="Salir", command=root.quit)
    
    # Menú Herramientas
    herramientas_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Herramientas", menu=herramientas_menu)
    herramientas_menu.add_command(label="Limpiar Resultados", command=lambda: app.limpiar_resultados())
    herramientas_menu.add_command(label="Configuración", command=lambda: app.mostrar_configuracion())
    
    # Menú Ayuda
    ayuda_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
    ayuda_menu.add_command(label="Acerca de", command=lambda: app.mostrar_acerca_de())

class BuscadorInmobiliario:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador Inmobiliario Integral España")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.resultados = []
        self.df_resultados = pd.DataFrame()
        
        # Headers para requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Portales inmobiliarios
        self.portales = {
            'idealista': 'https://www.idealista.com',
            'fotocasa': 'https://www.fotocasa.es',
            'pisos': 'https://www.pisos.com',
            'habitaclia': 'https://www.habitaclia.com',
            'inmofactory': 'https://www.inmofactory.com',
            'yaencontre': 'https://www.yaencontre.com',
            'kyero': 'https://www.kyero.com/es',
            'tecnocasa': 'https://www.tecnocasa.es'
        }
        
        # APIs de transporte público (simuladas)
        self.transportes_madrid = {
            'metro': ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12'],
            'autobus': ['EMT', 'Interurbano'],
            'cercanias': ['C1', 'C2', 'C3', 'C4', 'C5', 'C7', 'C8', 'C9', 'C10']
        }
        
        self.crear_interfaz()
        crear_menus(root, self)
        
    def exportar_excel(self):
        """Exportar resultados a Excel"""
        if not self.resultados:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
            
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                df = pd.DataFrame(self.resultados)
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def exportar_csv(self):
        """Exportar resultados a CSV"""
        if not self.resultados:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
            
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                df = pd.DataFrame(self.resultados)
                df.to_csv(filename, index=False, encoding='utf-8')
                messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def limpiar_resultados(self):
        """Limpiar todos los resultados"""
        self.resultados = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpiar gráficos
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()
            
        self.actualizar_estado("Resultados limpiados")
        messagebox.showinfo("Información", "Resultados limpiados correctamente")
    
    def mostrar_configuracion(self):
        """Mostrar ventana de configuración"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuración")
        config_window.geometry("400x300")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(config_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de timeout
        ttk.Label(main_frame, text="Timeout de conexión (segundos):").pack(anchor=tk.W, pady=(0, 5))
        timeout_var = tk.StringVar(value="10")
        timeout_entry = ttk.Entry(main_frame, textvariable=timeout_var)
        timeout_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Máximo de resultados por portal
        ttk.Label(main_frame, text="Máximo resultados por portal:").pack(anchor=tk.W, pady=(0, 5))
        max_results_var = tk.StringVar(value="20")
        max_results_entry = ttk.Entry(main_frame, textvariable=max_results_var)
        max_results_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Portales activos
        ttk.Label(main_frame, text="Portales activos:").pack(anchor=tk.W, pady=(0, 5))
        
        portales_frame = ttk.Frame(main_frame)
        portales_frame.pack(fill=tk.X, pady=(0, 15))
        
        portal_vars = {}
        for i, portal in enumerate(self.portales.keys()):
            var = tk.BooleanVar(value=True)
            portal_vars[portal] = var
            ttk.Checkbutton(portales_frame, text=portal.title(), variable=var).grid(
                row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=2
            )
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Guardar", 
                  command=config_window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=config_window.destroy).pack(side=tk.RIGHT)
    
    def mostrar_acerca_de(self):
        """Mostrar información sobre la aplicación"""
        about_text = """
        🏠 Buscador Inmobiliario Integral España
        
        Versión: 1.0
        
        Esta aplicación busca propiedades inmobiliarias en múltiples
        portales españoles, incluyendo vivienda protegida y análisis
        de transporte público.
        
        Características:
        • Búsqueda en 8+ portales inmobiliarios
        • Filtros avanzados de precio, ubicación y características
        • Análisis de transporte público cercano
        • Vivienda protegida y social
        • Gráficos y estadísticas interactivas
        • Exportación a Excel y CSV
        
        Desarrollado con Python, Tkinter, BeautifulSoup y Matplotlib
        """
        
        messagebox.showinfo("Acerca de", about_text)

    # Añadir método para verificar transporte mejorado
    def verificar_transporte_real(self, ubicacion):
        """Verificación más realista de transporte público"""
        try:
            # Simulación de consulta a API de transporte
            # En implementación real, usar APIs como:
            # - Consorcio Transportes Madrid
            # - TMB Barcelona
            # - Metro Bilbao, etc.
            
            import random
            
            ubicacion_lower = ubicacion.lower()
            
            # Patrones para detectar zonas con buen transporte
            zonas_metro = ['centro', 'sol', 'gran via', 'atocha', 'nuevos ministerios', 
                          'plaza españa', 'chueca', 'malasaña', 'conde duque']
            
            zonas_cercanias = ['alcalá', 'getafe', 'móstoles', 'fuenlabrada', 
                              'leganés', 'parla', 'pinto', 'valdemoro']
            
            transporte_info = []
            
            # Verificar metro
            for zona in zonas_metro:
                if zona in ubicacion_lower:
                    lineas_metro = random.sample(self.transportes_madrid['metro'], 
                                                random.randint(1, 3))
                    transporte_info.extend([f"Metro {linea}" for linea in lineas_metro])
                    break
            
            # Verificar cercanías
            for zona in zonas_cercanias:
                if zona in ubicacion_lower:
                    linea_cercanias = random.choice(self.transportes_madrid['cercanias'])
                    transporte_info.append(f"Cercanías {linea_cercanias}")
                    break
            
            # Siempre hay autobuses
            if random.random() > 0.2:  # 80% probabilidad
                transporte_info.append("Autobús EMT")
            
            return " | ".join(transporte_info) if transporte_info else "Consultar"
            
        except Exception as e:
            return "Error verificación"

    # Corregir error en la línea 102
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(main_frame, text="🏠 Buscador Inmobiliario Integral España",
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtros de Búsqueda", padding="10")
        filtros_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        filtros_frame.columnconfigure(1, weight=1)
        filtros_frame.columnconfigure(3, weight=1)
        
        # Tipo de operación
        ttk.Label(filtros_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.tipo_var = tk.StringVar(value="alquiler")
        tipo_combo = ttk.Combobox(filtros_frame, textvariable=self.tipo_var, 
                                 values=["alquiler", "venta"], state="readonly", width=15)
        tipo_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Ubicación
        ttk.Label(filtros_frame, text="Ubicación:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.ubicacion_var = tk.StringVar()
        ubicacion_entry = ttk.Entry(filtros_frame, textvariable=self.ubicacion_var, width=20)
        ubicacion_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Precio mínimo y máximo
        ttk.Label(filtros_frame, text="Precio mín (€):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.precio_min_var = tk.StringVar()
        precio_min_entry = ttk.Entry(filtros_frame, textvariable=self.precio_min_var, width=15)
        precio_min_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(10, 0))
        
        ttk.Label(filtros_frame, text="Precio máx (€):").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.precio_max_var = tk.StringVar()
        precio_max_entry = ttk.Entry(filtros_frame, textvariable=self.precio_max_var, width=20)
        precio_max_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Habitaciones y metros - CORREGIR EL ERROR AQUÍ
        ttk.Label(filtros_frame, text="Habitaciones:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.habitaciones_var = tk.StringVar()
        habitaciones_combo = ttk.Combobox(filtros_frame, textvariable=self.habitaciones_var,
                                         values=["", "1", "2", "3", "4", "5+"], state="readonly", width=15)
        habitaciones_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=(10, 0))
        
        ttk.Label(filtros_frame, text="Metros mín:").grid(row=2, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.metros_var = tk.StringVar()
        metros_entry = ttk.Entry(filtros_frame, textvariable=self.metros_var, width=20)
        metros_entry.grid(row=2, column=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Transporte público
        self.transporte_var = tk.BooleanVar()
        transporte_check = ttk.Checkbutton(filtros_frame, text="Solo con transporte público cercano",
                                          variable=self.transporte_var)
        transporte_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Vivienda protegida
        self.protegida_var = tk.BooleanVar()
        protegida_check = ttk.Checkbutton(filtros_frame, text="Incluir vivienda protegida",
                                         variable=self.protegida_var)
        protegida_check.grid(row=3, column=2, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Botón de búsqueda
        buscar_btn = tk.Button(main_frame, text="🔍 Buscar Propiedades", 
                              command=self.iniciar_busqueda, bg='#3498db', fg='white',
                              font=('Arial', 12, 'bold'), pady=5)
        buscar_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Frame de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="5")
        resultados_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(resultados_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña de lista
        self.frame_lista = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_lista, text="Lista de Propiedades")
        
        # Treeview para mostrar resultados
        columns = ('Portal', 'Título', 'Precio', 'Ubicación', 'Habitaciones', 'Metros', 'Transporte')
        self.tree = ttk.Treeview(self.frame_lista, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(self.frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(self.frame_lista, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.rowconfigure(0, weight=1)
        
        # Pestaña de gráficos
        self.frame_graficos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_graficos, text="Gráficos y Análisis")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Label de estado
        self.estado_label = tk.Label(main_frame, text="Listo para buscar", 
                                    bg='#f0f0f0', fg='#7f8c8d')
        self.estado_label.grid(row=5, column=0, columnspan=3)
        
        main_frame.rowconfigure(3, weight=1)

# Función principal
def main():
    try:
        # Importar numpy después de configurar matplotlib
        import numpy as np
        
        root = tk.Tk()
        app = BuscadorInmobiliario(root)
        
        # Configurar cierre de aplicación
        def on_closing():
            if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
                plt.close('all')  # Cerrar todas las figuras de matplotlib
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Mostrar mensaje de bienvenida
        messagebox.showinfo("Bienvenido", 
                           "¡Bienvenido al Buscador Inmobiliario Integral!\n\n"
                           "• Introduce una ubicación (ej: Madrid, Barcelona)\n"
                           "• Configura tus filtros de búsqueda\n"
                           "• Haz clic en 'Buscar Propiedades'\n"
                           "• Explora los resultados y gráficos\n\n"
                           "¡La búsqueda puede tardar varios minutos!")
        
        root.mainloop()
        
    except ImportError as e:
        missing_module = str(e).split("'")[1] if "'" in str(e) else "desconocido"
        messagebox.showerror("Error de Dependencias", 
                           f"Falta instalar el módulo: {missing_module}\n\n"
                           f"Instálalo con: pip install {missing_module}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
