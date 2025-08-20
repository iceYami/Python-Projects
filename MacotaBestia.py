import random
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import threading

class Drakonix:
    def __init__(self, nombre: str = "Sombrafuego"):
        self.nombre = nombre
        self.especie = "Dragón Sombra"
        self.edad = 0
        self.nivel = 1
        self.experiencia = 0
        
        # Estados básicos
        self.salud = 100
        self.hambre = 50
        self.sed = 50
        self.energia = 100
        self.felicidad = 75
        self.limpieza = 100
        
        # Atributos avanzados
        self.fuerza = 10
        self.magia = 15
        self.inteligencia = 12
        self.agilidad = 8
        self.carisma = 6
        
        # Estado emocional y personalidad
        self.humor = "neutral"
        self.personalidad = random.choice(["rebelde", "juguetón", "sabio", "feroz", "protector"])
        self.confianza = 50
        self.estres = 0
        
        # Inventario y posesiones
        self.oro = 100
        self.inventario = {
            "carne_fresca": 3,
            "pocion_salud": 1,
            "gema_poder": 0,
            "pergamino_misterioso": 0
        }
        
        # Habilidades especiales
        self.habilidades = {
            "aliento_fuego": 1,
            "vuelo": 0,
            "telepatia": 0,
            "berserker": 0,
            "curacion": 0
        }
        
        # Estado del mundo
        self.ubicacion = "cueva_natal"
        self.enemigos_derrotados = 0
        self.misiones_completadas = 0
        self.relaciones = {}
        
        # Eventos y tiempo
        self.ultimo_cuidado = time.time()
        self.eventos_especiales = []
        self.ciclo_dia = 0
        self.temporada = "primavera"
        
        # Evolución y transformación
        self.forma_actual = "juvenil"
        self.mutaciones = []
        self.cicatrices = []
        
        self.cargar_partida()
        
    def mostrar_estado(self):
        print(f"\n🐉 {self.nombre} - {self.especie} ({self.forma_actual})")
        print(f"📊 Nivel {self.nivel} | Exp: {self.experiencia}/100")
        print(f"💖 Salud: {self.salud}/100 | 🍖 Hambre: {self.hambre}/100")
        print(f"💧 Sed: {self.sed}/100 | ⚡ Energía: {self.energia}/100")
        print(f"😊 Felicidad: {self.felicidad}/100 | 🛁 Limpieza: {self.limpieza}/100")
        print(f"🎭 Humor: {self.humor} | 🤝 Confianza: {self.confianza}/100")
        print(f"💰 Oro: {self.oro} | 📍 Ubicación: {self.ubicacion}")
        
        if self.estres > 30:
            print(f"⚠️  ESTRÉS ALTO: {self.estres}/100")
        
        if self.cicatrices:
            print(f"⚔️  Cicatrices de batalla: {len(self.cicatrices)}")
            
        if self.mutaciones:
            print(f"🧬 Mutaciones: {', '.join(self.mutaciones)}")
    
    def alimentar(self, comida: str = "carne_fresca"):
        if comida not in self.inventario or self.inventario[comida] <= 0:
            print(f"❌ No tienes {comida}")
            return False
            
        self.inventario[comida] -= 1
        
        if comida == "carne_fresca":
            self.hambre = max(0, self.hambre - 30)
            self.felicidad += 10
            print(f"🍖 {self.nombre} devora la carne con ferocidad...")
            
            if self.personalidad == "feroz":
                self.fuerza += 1
                print("💪 Su naturaleza feroz se fortalece...")
                
        elif comida == "fruta_magica":
            self.hambre = max(0, self.hambre - 20)
            self.magia += 2
            print(f"🍎 {self.nombre} absorbe la esencia mágica...")
            
        if self.hambre < 20:
            self.energia += 15
            self.humor = "satisfecho"
            
        self.ganar_experiencia(5)
        return True
    
    def dar_agua(self):
        if self.sed < 20:
            print(f"💧 {self.nombre} no tiene sed ahora")
            return
            
        self.sed = max(0, self.sed - 40)
        self.salud += 5
        print(f"💧 {self.nombre} bebe del manantial cristalino...")
        
        if random.random() < 0.1:
            print("✨ ¡El agua tenía propiedades mágicas!")
            self.magia += 1
            
        self.ganar_experiencia(3)
    
    def jugar(self):
        if self.energia < 20:
            print(f"😴 {self.nombre} está demasiado cansado para jugar")
            return
            
        self.energia -= 20
        self.felicidad += 25
        self.confianza += 5
        self.estres = max(0, self.estres - 10)
        
        actividad = random.choice([
            "perseguir_cola", "cazar_mariposas", "rugir_practica", 
            "volar_circulos", "atacar_sombras", "explorar_cueva"
        ])
        
        print(f"🎮 {self.nombre} está {actividad.replace('_', ' ')}...")
        
        if actividad == "cazar_mariposas":
            self.agilidad += 1
            print("🦋 Su agilidad mejora con la caza")
        elif actividad == "rugir_practica":
            self.carisma += 1
            print("🗣️ Su rugido se vuelve más imponente")
        elif actividad == "volar_circulos":
            if self.habilidades["vuelo"] > 0:
                self.energia += 10
                print("🕊️ Volar le da energía extra")
        elif actividad == "explorar_cueva":
            if random.random() < 0.3:
                tesoro = random.choice(["oro", "gema_poder", "pergamino_misterioso"])
                if tesoro == "oro":
                    oro_encontrado = random.randint(10, 50)
                    self.oro += oro_encontrado
                    print(f"💰 ¡Encontró {oro_encontrado} monedas de oro!")
                else:
                    self.inventario[tesoro] = self.inventario.get(tesoro, 0) + 1
                    print(f"✨ ¡Encontró un {tesoro.replace('_', ' ')}!")
        
        self.ganar_experiencia(8)
    
    def entrenar(self, tipo: str):
        if self.energia < 30:
            print(f"😴 {self.nombre} necesita más energía para entrenar")
            return
            
        self.energia -= 30
        self.hambre += 15
        self.sed += 10
        
        if tipo == "fuerza":
            self.fuerza += 2
            print(f"💪 {self.nombre} entrena con rocas gigantes...")
            if random.random() < 0.2:
                print("⚡ ¡Su entrenamiento despertó una furia interior!")
                self.habilidades["berserker"] += 1
                
        elif tipo == "magia":
            self.magia += 2
            print(f"🔮 {self.nombre} practica conjuros arcanos...")
            if random.random() < 0.3:
                print("🧠 ¡Su mente se expande!")
                self.inteligencia += 1
                
        elif tipo == "agilidad":
            self.agilidad += 2
            print(f"🏃 {self.nombre} practica movimientos rápidos...")
            if self.nivel > 5 and random.random() < 0.15:
                print("🕊️ ¡Ha aprendido a volar!")
                self.habilidades["vuelo"] = 1
                
        elif tipo == "combate":
            self.fuerza += 1
            self.agilidad += 1
            print(f"⚔️ {self.nombre} practica técnicas de combate...")
            
        self.ganar_experiencia(15)
    
    def explorar(self, lugar: str = None):
        if self.energia < 25:
            print(f"😴 {self.nombre} está demasiado cansado para explorar")
            return
            
        lugares = {
            "bosque_encantado": {"peligro": 0.3, "recompensa": "moderada"},
            "montanas_dragones": {"peligro": 0.6, "recompensa": "alta"},
            "ruinas_antiguas": {"peligro": 0.4, "recompensa": "especial"},
            "pantano_maldito": {"peligro": 0.8, "recompensa": "extrema"},
            "ciudad_humana": {"peligro": 0.2, "recompensa": "social"}
        }
        
        if lugar is None:
            lugar = random.choice(list(lugares.keys()))
            
        if lugar not in lugares:
            print(f"❌ {lugar} no es un lugar válido")
            return
            
        self.energia -= 25
        self.ubicacion = lugar
        info = lugares[lugar]
        
        print(f"🗺️ {self.nombre} explora {lugar.replace('_', ' ')}...")
        
        if random.random() < info["peligro"]:
            self.enfrentar_peligro(lugar)
        else:
            self.encontrar_recompensa(info["recompensa"])
            
        self.ganar_experiencia(20)
    
    def enfrentar_peligro(self, lugar: str):
        peligros = {
            "bosque_encantado": ["lobo_sombra", "hada_maligna", "ent_furioso"],
            "montanas_dragones": ["dragon_anciano", "gigante_piedra", "tormenta_magica"],
            "ruinas_antiguas": ["golem_guardian", "espectro_vengativo", "trampa_mortal"],
            "pantano_maldito": ["kraken_pantano", "brujo_oscuro", "gas_toxico"],
            "ciudad_humana": ["cazador_dragones", "mago_hostil", "multitud_enfurecida"]
        }
        
        enemigo = random.choice(peligros[lugar])
        print(f"⚠️ ¡{self.nombre} se enfrenta a {enemigo.replace('_', ' ')}!")
        
        poder_enemigo = random.randint(20, 80)
        poder_dragon = self.fuerza + self.magia + self.agilidad + random.randint(1, 20)
        
        if poder_dragon > poder_enemigo:
            print(f"⚔️ ¡{self.nombre} emerge victorioso!")
            self.enemigos_derrotados += 1
            self.confianza += 10
            self.felicidad += 15
            
            # Recompensas de batalla
            oro_ganado = random.randint(50, 200)
            self.oro += oro_ganado
            print(f"💰 Gana {oro_ganado} oro")
            
            if random.random() < 0.3:
                cicatriz = f"batalla_{enemigo}"
                self.cicatrices.append(cicatriz)
                print(f"⚔️ {self.nombre} lleva una nueva cicatriz como trofeo")
                
            if random.random() < 0.2:
                self.desbloquear_habilidad()
                
        else:
            print(f"💔 {self.nombre} sale herido del combate...")
            self.salud -= random.randint(20, 40)
            self.estres += 20
            self.confianza -= 5
            
            if self.salud < 20:
                print("⚠️ ¡{} necesita curación urgente!".format(self.nombre))
                self.humor = "herido"
    
    def encontrar_recompensa(self, tipo: str):
        if tipo == "moderada":
            oro = random.randint(20, 100)
            self.oro += oro
            print(f"💰 {self.nombre} encuentra {oro} monedas de oro")
            
        elif tipo == "alta":
            if random.random() < 0.4:
                item = random.choice(["gema_poder", "pocion_salud", "pergamino_misterioso"])
                self.inventario[item] = self.inventario.get(item, 0) + 1
                print(f"✨ {self.nombre} encuentra {item.replace('_', ' ')}")
            else:
                oro = random.randint(100, 300)
                self.oro += oro
                print(f"💰 {self.nombre} encuentra un tesoro de {oro} oro")
                
        elif tipo == "especial":
            if random.random() < 0.3:
                mutacion = random.choice(["escamas_doradas", "ojos_cristal", "garras_sombra"])
                if mutacion not in self.mutaciones:
                    self.mutaciones.append(mutacion)
                    print(f"🧬 ¡{self.nombre} desarrolla {mutacion.replace('_', ' ')}!")
                    self.aplicar_mutacion(mutacion)
            else:
                self.encontrar_recompensa("alta")
                
        elif tipo == "extrema":
            if random.random() < 0.5:
                self.desbloquear_habilidad()
            else:
                oro = random.randint(200, 500)
                self.oro += oro
                print(f"💰 {self.nombre} encuentra un tesoro legendario de {oro} oro")
                
        elif tipo == "social":
            npc = random.choice(["mercader", "mago", "noble", "sacerdote"])
            self.relaciones[npc] = self.relaciones.get(npc, 0) + 10
            print(f"🤝 {self.nombre} mejora su relación con {npc}")
    
    def aplicar_mutacion(self, mutacion: str):
        if mutacion == "escamas_doradas":
            self.carisma += 5
            print("✨ Su carisma aumenta considerablemente")
        elif mutacion == "ojos_cristal":
            self.inteligencia += 3
            self.magia += 2
            print("🔮 Su percepción mágica se agudiza")
        elif mutacion == "garras_sombra":
            self.fuerza += 3
            self.agilidad += 2
            print("⚔️ Sus garras se vuelven mortales")
    
    def desbloquear_habilidad(self):
        habilidades_disponibles = []
        
        if self.nivel >= 5 and self.habilidades["vuelo"] == 0:
            habilidades_disponibles.append("vuelo")
        if self.nivel >= 8 and self.habilidades["telepatia"] == 0:
            habilidades_disponibles.append("telepatia")
        if self.nivel >= 10 and self.habilidades["berserker"] == 0:
            habilidades_disponibles.append("berserker")
        if self.nivel >= 12 and self.habilidades["curacion"] == 0:
            habilidades_disponibles.append("curacion")
        
        if habilidades_disponibles:
            nueva_habilidad = random.choice(habilidades_disponibles)
            self.habilidades[nueva_habilidad] = 1
            print(f"🌟 ¡{self.nombre} desbloquea {nueva_habilidad.replace('_', ' ')}!")
    
    def usar_habilidad(self, habilidad: str):
        if habilidad not in self.habilidades or self.habilidades[habilidad] == 0:
            print(f"❌ {self.nombre} no conoce {habilidad}")
            return
            
        if self.energia < 20:
            print(f"😴 {self.nombre} necesita más energía para usar habilidades")
            return
            
        self.energia -= 20
        
        if habilidad == "aliento_fuego":
            print(f"🔥 {self.nombre} lanza un poderoso aliento de fuego")
            self.ganar_experiencia(10)
            
        elif habilidad == "vuelo":
            print(f"🕊️ {self.nombre} vuela majestuosamente por los cielos")
            self.energia += 10  # Volar le da energía
            self.felicidad += 20
            
        elif habilidad == "telepatia":
            print(f"🧠 {self.nombre} conecta su mente con la tuya...")
            self.confianza += 15
            print(f"💭 Puedes sentir sus pensamientos: '{self.generar_pensamiento()}'")
            
        elif habilidad == "berserker":
            print(f"😡 {self.nombre} entra en furia berserker")
            self.fuerza += 10  # Temporal
            self.estres += 30
            
        elif habilidad == "curacion":
            print(f"✨ {self.nombre} canaliza energía curativa")
            self.salud = min(100, self.salud + 30)
            self.estres = max(0, self.estres - 20)
    
    def generar_pensamiento(self):
        if self.felicidad > 80:
            return random.choice([
                "Me siento increíblemente feliz contigo...",
                "Eres el mejor compañero que podría tener",
                "Quiero explorar el mundo a tu lado"
            ])
        elif self.felicidad < 30:
            return random.choice([
                "Me siento triste y abandonado...",
                "¿Por qué no juegas conmigo?",
                "Necesito más atención..."
            ])
        elif self.hambre > 70:
            return random.choice([
                "Tengo mucha hambre...",
                "¿Cuándo vamos a comer?",
                "Sueño con carne fresca..."
            ])
        else:
            return random.choice([
                "Me pregunto qué aventuras nos esperan",
                "Este mundo está lleno de misterios",
                "Siento que me estoy volviendo más fuerte"
            ])
    
    def curar(self):
        if "pocion_salud" not in self.inventario or self.inventario["pocion_salud"] <= 0:
            print("❌ No tienes pociones de salud")
            return
            
        if self.salud >= 100:
            print(f"💖 {self.nombre} ya está completamente sano")
            return
            
        self.inventario["pocion_salud"] -= 1
        self.salud = min(100, self.salud + 50)
        self.humor = "aliviado"
        print(f"💊 {self.nombre} bebe la poción y se siente mucho mejor")
    
    def dormir(self):
        if self.energia > 80:
            print(f"😴 {self.nombre} no tiene sueño ahora")
            return
            
        print(f"🌙 {self.nombre} se acomoda en su lugar favorito para dormir...")
        
        # Simulación de sueño
        self.energia = 100
        self.salud = min(100, self.salud + 10)
        self.estres = max(0, self.estres - 20)
        self.hambre += 20
        self.sed += 15
        
        # Eventos de sueño
        if random.random() < 0.3:
            sueno = random.choice([
                "sueña con volar sobre montañas doradas",
                "tiene pesadillas sobre cazadores de dragones",
                "sueña con un gran tesoro escondido",
                "ve visiones de otros dragones en sus sueños"
            ])
            print(f"💭 {self.nombre} {sueno}")
            
            if "pesadillas" in sueno:
                self.estres += 10
            elif "tesoro" in sueno:
                self.oro += random.randint(10, 50)
                print("💰 ¡Su sueño le reveló la ubicación de oro!")
                
        print(f"☀️ {self.nombre} despierta renovado")
    
    def limpiar(self):
        if self.limpieza > 80:
            print(f"🛁 {self.nombre} ya está bastante limpio")
            return
            
        self.limpieza = min(100, self.limpieza + 40)
        self.felicidad += 15
        self.carisma += 2
        
        print(f"🛁 {self.nombre} se baña en el lago cristalino...")
        
        if random.random() < 0.2:
            print("✨ ¡El agua mágica del lago le da un brillo especial!")
            self.carisma += 5
    
    def ganar_experiencia(self, cantidad: int):
        self.experiencia += cantidad
        
        if self.experiencia >= 100:
            self.experiencia = 0
            self.nivel += 1
            self.salud = 100
            self.fuerza += 2
            self.magia += 2
            self.inteligencia += 1
            
            print(f"🎉 ¡{self.nombre} sube al nivel {self.nivel}!")
            
            # Evolución por niveles
            if self.nivel == 10 and self.forma_actual == "juvenil":
                self.evolucionar("adulto")
            elif self.nivel == 20 and self.forma_actual == "adulto":
                self.evolucionar("ancestral")
    
    def evolucionar(self, nueva_forma: str):
        print(f"🌟 ¡{self.nombre} está evolucionando!")
        self.forma_actual = nueva_forma
        
        if nueva_forma == "adulto":
            self.fuerza += 20
            self.magia += 15
            self.agilidad += 10
            self.carisma += 10
            print(f"🐉 {self.nombre} se ha convertido en un dragón adulto imponente")
            
        elif nueva_forma == "ancestral":
            self.fuerza += 50
            self.magia += 40
            self.inteligencia += 30
            self.carisma += 25
            print(f"👑 {self.nombre} ascendió a Dragón Ancestral - ¡Una leyenda viviente!")
            
        self.felicidad = 100
        self.confianza = 100
    
    def evento_aleatorio(self):
        if random.random() < 0.15:  # 15% de probabilidad
            evento = random.choice([
                "tormenta_magica", "visitante_misterioso", "eclipse_lunar",
                "brote_magico", "invasion_goblins", "mercader_viajero"
            ])
            
            if evento == "tormenta_magica":
                print("⛈️ ¡Una tormenta mágica azota la región!")
                self.magia += 5
                self.estres += 15
                
            elif evento == "visitante_misterioso":
                print("🥷 Un visitante misterioso aparece...")
                if random.random() < 0.5:
                    regalo = random.choice(["gema_poder", "pergamino_misterioso"])
                    self.inventario[regalo] = self.inventario.get(regalo, 0) + 1
                    print(f"🎁 Te deja un {regalo.replace('_', ' ')}")
                else:
                    print("👻 Desaparece sin decir nada...")
                    
            elif evento == "eclipse_lunar":
                print("🌙 Un eclipse lunar baña el mundo en luz plateada")
                self.magia += 10
                self.felicidad += 20
                
            elif evento == "brote_magico":
                print("🌸 Flores mágicas brotan por toda la región")
                self.salud += 20
                self.felicidad += 15
                
            elif evento == "invasion_goblins":
                print("👹 ¡Una banda de goblins invade tu territorio!")
                if self.fuerza > 20:
                    print("⚔️ Los derrotas fácilmente")
                    self.oro += 100
                    self.confianza += 10
                else:
                    print("💔 Te roban algo de oro")
                    self.oro = max(0, self.oro - 50)
                    
            elif evento == "mercader_viajero":
                print("🛒 Un mercader viajero ofrece sus mercancías")
                if self.oro >= 100:
                    print("💰 Compras provisiones (100 oro)")
                    self.oro -= 100
                    self.inventario["carne_fresca"] += 3
                    self.inventario["pocion_salud"] += 1
    
    def actualizar_estado(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.ultimo_cuidado
        
        # Degradación natural por tiempo
        if tiempo_transcurrido > 300:  # 5 minutos
            self.hambre = min(100, self.hambre + 10)
            self.sed = min(100, self.sed + 8)
            self.energia = max(0, self.energia - 5)
            self.limpieza = max(0, self.limpieza - 5)
            self.ultimo_cuidado = tiempo_actual
        
        # Efectos de estados críticos
        if self.hambre > 80:
            self.salud = max(0, self.salud - 2)
            self.humor = "hambriento"
            
        if self.sed > 85:
            self.salud = max(0, self.salud - 3)
            self.energia = max(0, self.energia - 5)
            
        if self.energia < 20:
            self.humor = "cansado"
            
        if self.limpieza < 30:
            self.felicidad = max(0, self.felicidad - 5)
            self.carisma = max(0, self.carisma - 2)
            
        if self.estres > 70:
            self.felicidad = max(0, self.felicidad - 10)
            self.salud = max(0, self.salud - 5)
            
        # Muerte por negligencia
        if self.salud <= 0:
            print(f"💀 {self.nombre} ha muerto por negligencia...")
            return False
            
        return True
    
    def guardar_partida(self):
        datos = {
            'nombre': self.nombre,
            'nivel': self.nivel,
            'experiencia': self.experiencia,
            'salud': self.salud,
            'hambre': self.hambre,
            'sed': self.sed,
            'energia': self.energia,
            'felicidad': self.felicidad,
            'limpieza': self.limpieza,
            'fuerza': self.fuerza,
            'magia': self.magia,
            'inteligencia': self.inteligencia,
            'agilidad': self.agilidad,
            'carisma': self.carisma,
            'oro': self.oro,
            'inventario': self.inventario,
            'habilidades': self.habilidades,
            'forma_actual': self.forma_actual,
            'personalidad': self.personalidad,
            'confianza': self.confianza,
            'estres': self.estres,
            'enemigos_derrotados': self.enemigos_derrotados,
            'mutaciones': self.mutaciones,
            'cicatrices': self.cicatrices,
            'relaciones': self.relaciones,
            'ubicacion': self.ubicacion,
            'ultimo_cuidado': self.ultimo_cuidado
        }
        
        with open('drakonix_save.json', 'w') as f:
            json.dump(datos, f, indent=2)
    
    def cargar_partida(self):
        try:
            with open('drakonix_save.json', 'r') as f:
                datos = json.load(f)
                
            for key, value in datos.items():
                setattr(self, key, value)
                
            print(f"💾 Partida de {self.nombre} cargada exitosamente")
            
        except FileNotFoundError:
            print("🆕 Nueva partida iniciada")
    
    def mostrar_inventario(self):
        print(f"\n🎒 Inventario de {self.nombre}:")
        print(f"💰 Oro: {self.oro}")
        for item, cantidad in self.inventario.items():
            if cantidad > 0:
                print(f"📦 {item.replace('_', ' ').title()}: {cantidad}")
    
    def mostrar_habilidades(self):
        print(f"\n⚡ Habilidades de {self.nombre}:")
        for habilidad, nivel in self.habilidades.items():
            estado = "🟢 Activa" if nivel > 0 else "🔒 Bloqueada"
            print(f"✨ {habilidad.replace('_', ' ').title()}: {estado}")
    
    def mostrar_relaciones(self):
        print(f"\n🤝 Relaciones de {self.nombre}:")
        if not self.relaciones:
            print("😔 No tiene relaciones establecidas aún")
        else:
            for persona, nivel in self.relaciones.items():
                if nivel >= 70:
                    estado = "💖 Aliado leal"
                elif nivel >= 40:
                    estado = "😊 Amigo"
                elif nivel >= 10:
                    estado = "🙂 Conocido"
                else:
                    estado = "😐 Neutral"
                print(f"👤 {persona.title()}: {estado} ({nivel}/100)")

def main():
    print("🐉 ¡Bienvenido al mundo de Drakonix!")
    print("=" * 50)
    
    # Crear o cargar mascota
    nombre = input("¿Cómo quieres llamar a tu dragón? (Enter para 'Sombrafuego'): ").strip()
    if not nombre:
        nombre = "Sombrafuego"
    
    dragon = Drakonix(nombre)
    
    # Hilo para eventos automáticos
    def eventos_automaticos():
        while True:
            time.sleep(180)  # Cada 3 minutos
            if dragon.actualizar_estado():
                dragon.evento_aleatorio()
                dragon.guardar_partida()
            else:
                break
    
    threading.Thread(target=eventos_automaticos, daemon=True).start()
    
    print(f"\n🎮 ¡{dragon.nombre} ha nacido!")
    print(f"🧬 Personalidad: {dragon.personalidad}")
    print("\n📖 Comandos disponibles:")
    print("  ver - Ver estado actual")
    print("  alimentar - Dar comida")
    print("  agua - Dar agua")
    print("  jugar - Jugar con tu dragón")
    print("  entrenar [tipo] - Entrenar (fuerza/magia/agilidad/combate)")
    print("  explorar [lugar] - Explorar lugares")
    print("  habilidad [nombre] - Usar habilidad especial")
    print("  dormir - Hacer que descanse")
    print("  limpiar - Limpiar al dragón")
    print("  curar - Usar poción de salud")
    print("  inventario - Ver inventario")
    print("  habilidades - Ver habilidades")
    print("  relaciones - Ver relaciones")
    print("  tienda - Visitar la tienda")
    print("  mision - Buscar misiones")
    print("  guardar - Guardar partida")
    print("  salir - Salir del juego")
    
    while True:
        try:
            if not dragon.actualizar_estado():
                print("\n💀 GAME OVER")
                print(f"Tu dragón {dragon.nombre} ha muerto...")
                print("¡Cuídalo mejor la próxima vez!")
                break
            
            comando = input(f"\n🎮 ¿Qué quieres hacer con {dragon.nombre}? ").strip().lower()
            
            if comando == "ver":
                dragon.mostrar_estado()
                
            elif comando == "alimentar":
                dragon.alimentar()
                
            elif comando == "agua":
                dragon.dar_agua()
                
            elif comando == "jugar":
                dragon.jugar()
                
            elif comando.startswith("entrenar"):
                partes = comando.split()
                if len(partes) > 1:
                    dragon.entrenar(partes[1])
                else:
                    print("🏋️ Tipos de entrenamiento: fuerza, magia, agilidad, combate")
                    
            elif comando.startswith("explorar"):
                partes = comando.split()
                if len(partes) > 1:
                    lugar = "_".join(partes[1:])
                    dragon.explorar(lugar)
                else:
                    dragon.explorar()
                    
            elif comando.startswith("habilidad"):
                partes = comando.split()
                if len(partes) > 1:
                    habilidad = "_".join(partes[1:])
                    dragon.usar_habilidad(habilidad)
                else:
                    dragon.mostrar_habilidades()
                    
            elif comando == "dormir":
                dragon.dormir()
                
            elif comando == "limpiar":
                dragon.limpiar()
                
            elif comando == "curar":
                dragon.curar()
                
            elif comando == "inventario":
                dragon.mostrar_inventario()
                
            elif comando == "habilidades":
                dragon.mostrar_habilidades()
                
            elif comando == "relaciones":
                dragon.mostrar_relaciones()
                
            elif comando == "tienda":
                visitar_tienda(dragon)
                
            elif comando == "mision":
                buscar_mision(dragon)
                
            elif comando == "guardar":
                dragon.guardar_partida()
                print("💾 Partida guardada")
                
            elif comando == "salir":
                dragon.guardar_partida()
                print(f"👋 ¡Hasta luego! {dragon.nombre} te esperará...")
                break
                
            elif comando == "ayuda":
                print("\n📖 Comandos disponibles:")
                print("  ver, alimentar, agua, jugar, entrenar [tipo]")
                print("  explorar [lugar], habilidad [nombre], dormir")
                print("  limpiar, curar, inventario, habilidades")
                print("  relaciones, tienda, mision, guardar, salir")
                
            else:
                print("❓ Comando no reconocido. Escribe 'ayuda' para ver comandos")
                
        except KeyboardInterrupt:
            dragon.guardar_partida()
            print(f"\n👋 ¡Hasta luego! {dragon.nombre} te esperará...")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

def visitar_tienda(dragon):
    print("\n🏪 Bienvenido a la Tienda del Dragón")
    print("=" * 30)
    
    items_tienda = {
        "carne_fresca": {"precio": 20, "descripcion": "Carne fresca para alimentar"},
        "pocion_salud": {"precio": 50, "descripcion": "Restaura salud"},
        "gema_poder": {"precio": 200, "descripcion": "Aumenta poder mágico"},
        "pergamino_misterioso": {"precio": 150, "descripcion": "Contiene secretos arcanos"},
        "armadura_escamas": {"precio": 500, "descripcion": "Protección extra en combate"},
        "collar_sabiduria": {"precio": 300, "descripcion": "Aumenta inteligencia permanentemente"}
    }
    
    print(f"💰 Tu oro: {dragon.oro}")
    print("\n🛒 Artículos disponibles:")
    
    for item, info in items_tienda.items():
        print(f"  {item.replace('_', ' ').title()}: {info['precio']} oro - {info['descripcion']}")
    
    compra = input("\n¿Qué quieres comprar? (o 'salir'): ").strip().lower().replace(' ', '_')
    
    if compra == "salir":
        return
        
    if compra in items_tienda:
        precio = items_tienda[compra]["precio"]
        if dragon.oro >= precio:
            dragon.oro -= precio
            dragon.inventario[compra] = dragon.inventario.get(compra, 0) + 1
            print(f"✅ Has comprado {compra.replace('_', ' ')}")
            
            # Efectos especiales de algunos items
            if compra == "collar_sabiduria":
                dragon.inteligencia += 5
                print("🧠 ¡Tu dragón se siente más sabio!")
            elif compra == "armadura_escamas":
                dragon.fuerza += 3
                print("⚔️ ¡Tu dragón se siente más protegido!")
        else:
            print(f"❌ No tienes suficiente oro (necesitas {precio})")
    else:
        print("❌ Artículo no disponible")

def buscar_mision(dragon):
    print("\n📋 Tablón de Misiones")
    print("=" * 25)
    
    misiones = [
        {
            "nombre": "Rescate en el Bosque",
            "descripcion": "Una doncella está perdida en el bosque encantado",
            "requerimientos": {"nivel": 3, "carisma": 15},
            "recompensas": {"oro": 200, "experiencia": 50, "relacion": "noble"}
        },
        {
            "nombre": "Cazador de Tesoros",
            "descripcion": "Encuentra el tesoro perdido en las ruinas antiguas",
            "requerimientos": {"nivel": 5, "inteligencia": 20},
            "recompensas": {"oro": 400, "experiencia": 80, "item": "gema_poder"}
        },
        {
            "nombre": "Defensor del Pueblo",
            "descripcion": "Protege la aldea de una invasión de orcos",
            "requerimientos": {"nivel": 8, "fuerza": 25},
            "recompensas": {"oro": 600, "experiencia": 120, "habilidad": "berserker"}
        },
        {
            "nombre": "Maestro Alquimista",
            "descripcion": "Ayuda al mago a recoger ingredientes raros",
            "requerimientos": {"nivel": 6, "magia": 30},
            "recompensas": {"oro": 300, "experiencia": 70, "item": "pergamino_misterioso"}
        }
    ]
    
    print("🎯 Misiones disponibles:")
    for i, mision in enumerate(misiones, 1):
        print(f"\n{i}. {mision['nombre']}")
        print(f"   📖 {mision['descripcion']}")
        
        # Verificar requerimientos
        puede_hacer = True
        reqs = mision['requerimientos']
        
        if dragon.nivel < reqs.get('nivel', 0):
            puede_hacer = False
            print(f"   ❌ Requiere nivel {reqs['nivel']} (tienes {dragon.nivel})")
        
        for stat, valor in reqs.items():
            if stat != 'nivel' and getattr(dragon, stat) < valor:
                puede_hacer = False
                print(f"   ❌ Requiere {stat} {valor} (tienes {getattr(dragon, stat)})")
        
        if puede_hacer:
            print("   ✅ Puedes realizar esta misión")
            
    eleccion = input("\n¿Qué misión quieres realizar? (número o 'salir'): ").strip()
    
    if eleccion == "salir":
        return
        
    try:
        indice = int(eleccion) - 1
        if 0 <= indice < len(misiones):
            mision = misiones[indice]
            realizar_mision(dragon, mision)
        else:
            print("❌ Misión no válida")
    except ValueError:
        print("❌ Introduce un número válido")

def realizar_mision(dragon, mision):
    print(f"\n🎯 Iniciando misión: {mision['nombre']}")
    print(f"📖 {mision['descripcion']}")
    
    # Verificar si cumple requerimientos
    reqs = mision['requerimientos']
    for stat, valor in reqs.items():
        if getattr(dragon, stat) < valor:
            print(f"❌ No cumples los requerimientos para esta misión")
            return
    
    # Simular misión
    print(f"⚡ {dragon.nombre} parte en su misión...")
    dragon.energia -= 40
    dragon.hambre += 30
    dragon.sed += 20
    
    # Probabilidad de éxito basada en stats
    exito = random.random() < 0.7  # 70% base
    
    if dragon.nivel >= reqs.get('nivel', 0) + 3:
        exito = True  # Garantizado si está muy por encima del nivel
    
    if exito:
        print("🎉 ¡Misión completada con éxito!")
        dragon.misiones_completadas += 1
        
        # Dar recompensas
        recompensas = mision['recompensas']
        
        if 'oro' in recompensas:
            dragon.oro += recompensas['oro']
            print(f"💰 Ganas {recompensas['oro']} oro")
            
        if 'experiencia' in recompensas:
            dragon.ganar_experiencia(recompensas['experiencia'])
            
        if 'item' in recompensas:
            item = recompensas['item']
            dragon.inventario[item] = dragon.inventario.get(item, 0) + 1
            print(f"📦 Obtienes {item.replace('_', ' ')}")
            
        if 'habilidad' in recompensas:
            habilidad = recompensas['habilidad']
            dragon.habilidades[habilidad] = 1
            print(f"⚡ Desbloqueas {habilidad}")
            
        if 'relacion' in recompensas:
            persona = recompensas['relacion']
            dragon.relaciones[persona] = dragon.relaciones.get(persona, 0) + 20
            print(f"🤝 Mejoras tu relación con {persona}")
            
        dragon.confianza += 15
        dragon.felicidad += 25
        
    else:
        print("💔 La misión falló...")
        dragon.salud -= 20
        dragon.estres += 25
        dragon.confianza -= 5
        print("😔 Pero ganaste experiencia del intento")
        dragon.ganar_experiencia(10)

if __name__ == "__main__":
    main()
