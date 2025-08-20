import random
import json
import os

class Soldado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nivel = 1
        self.exp = 0
        self.exp_siguiente = 100
        self.hp = 100
        self.hp_max = 100
        self.energia = 100
        self.energia_max = 100
        self.dinero = 500
        
        # Atributos
        self.fuerza = 10
        self.agilidad = 10
        self.resistencia = 10
        self.punteria = 10
        self.carisma = 10
        self.puntos_habilidad = 0
        
        # Inventario y equipamiento
        self.arma_actual = None
        self.armadura_actual = None
        self.inventario = []
        self.armas = []
        self.regalos = []
        
        # Relaciones
        self.novia = None
        self.nivel_relacion = 0
        
        # Mascota
        self.mascota = None
        
        # Misiones
        self.misiones_completadas = 0
        self.reputacion = 0

class Mascota:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo  # "Perro", "Gato", "Halcón"
        self.nivel = 1
        self.hp = 50
        self.hp_max = 50
        self.lealtad = 50
        self.habilidades = []
        
        if tipo == "Perro":
            self.habilidades = ["Rastreo", "Ataque", "Guardia"]
            self.bonus_combate = 5
        elif tipo == "Gato":
            self.habilidades = ["Sigilo", "Agilidad", "Detección"]
            self.bonus_sigilo = 5
        elif tipo == "Halcón":
            self.habilidades = ["Reconocimiento", "Vigilancia", "Mensaje"]
            self.bonus_intel = 5

class Arma:
    def __init__(self, nombre, tipo, daño, precisión, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.daño = daño
        self.precisión = precisión
        self.precio = precio
        self.nivel_mejora = 0
        self.modificadores = []

class Novia:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hp = 80
        self.hp_max = 80
        self.amor = 50
        self.en_peligro = False
        self.regalos_recibidos = []

class Mision:
    def __init__(self, nombre, descripcion, tipo, dificultad, recompensa_exp, recompensa_dinero):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo  # "Combate", "Sigilo", "Rescate", "Intel"
        self.dificultad = dificultad
        self.recompensa_exp = recompensa_exp
        self.recompensa_dinero = recompensa_dinero
        self.completada = False

class JuegoRPG:
    def __init__(self):
        self.soldado = None
        self.tienda_armas = self.crear_tienda_armas()
        self.tienda_regalos = self.crear_tienda_regalos()
        self.enemigos = self.crear_enemigos()
        self.misiones_disponibles = self.crear_misiones()
        
    def crear_tienda_armas(self):
        return [
            Arma("Pistola M9", "Pistola", 25, 85, 200),
            Arma("Rifle M4", "Rifle", 45, 90, 800),
            Arma("Sniper Barrett", "Francotirador", 120, 95, 2000),
            Arma("Escopeta", "Escopeta", 60, 70, 600),
            Arma("SMG", "Subfusil", 35, 80, 400),
            Arma("Cuchillo Táctico", "Cuerpo a cuerpo", 20, 100, 100)
        ]
    
    def crear_tienda_regalos(self):
        return [
            {"nombre": "Flores", "precio": 50, "amor": 10},
            {"nombre": "Chocolate", "precio": 30, "amor": 8},
            {"nombre": "Joya", "precio": 300, "amor": 25},
            {"nombre": "Peluche", "precio": 80, "amor": 12},
            {"nombre": "Perfume", "precio": 150, "amor": 18},
            {"nombre": "Libro", "precio": 40, "amor": 9}
        ]
    
    def crear_enemigos(self):
        return [
            {"nombre": "Terrorista", "hp": 60, "daño": 20, "exp": 30, "dinero": 100},
            {"nombre": "Francotirador Enemigo", "hp": 80, "daño": 35, "exp": 50, "dinero": 200},
            {"nombre": "Líder Terrorista", "hp": 150, "daño": 45, "exp": 100, "dinero": 500},
            {"nombre": "Soldado Enemigo", "hp": 90, "daño": 30, "exp": 60, "dinero": 250},
            {"nombre": "Mercenario", "hp": 120, "daño": 40, "exp": 80, "dinero": 400}
        ]
    
    def crear_misiones(self):
        return [
            Mision("Rescate de Rehenes", "Rescata a los civiles del edificio ocupado", "Rescate", 3, 150, 800),
            Mision("Eliminar Célula Terrorista", "Infiltra y elimina a los terroristas", "Combate", 4, 200, 1000),
            Mision("Reconocimiento", "Obtén información sobre el enemigo", "Intel", 2, 80, 400),
            Mision("Emboscada", "Tiende una emboscada al convoy enemigo", "Sigilo", 3, 120, 600),
            Mision("Proteger VIP", "Escolta y protege al dignatario", "Protección", 5, 250, 1200)
        ]
    
    def iniciar_juego(self):
        print("=" * 50)
        print("🎮 BIENVENIDA AL RPG SOLDADO ELITE 🎮")
        print("=" * 50)
        nombre = input("Ingresa el nombre de tu soldado: ")
        self.soldado = Soldado(nombre)
        
        print(f"\n¡Bienvenida, soldado {nombre}!")
        print("Has sido asignada a operaciones especiales.")
        
        # Elegir mascota
        self.elegir_mascota()
        
        # Elegir novia
        self.elegir_novia()
        
        # Bucle principal del juego
        self.bucle_principal()
    
    def elegir_mascota(self):
        print("\n🐕 SELECCIONA TU MASCOTA COMPAÑERA:")
        print("1. Perro (Bonus combate +5)")
        print("2. Gato (Bonus sigilo +5)")
        print("3. Halcón (Bonus intel +5)")
        
        while True:
            try:
                opcion = int(input("Elige (1-3): "))
                if opcion == 1:
                    nombre = input("Nombre de tu perro: ")
                    self.soldado.mascota = Mascota(nombre, "Perro")
                    break
                elif opcion == 2:
                    nombre = input("Nombre de tu gato: ")
                    self.soldado.mascota = Mascota(nombre, "Gato")
                    break
                elif opcion == 3:
                    nombre = input("Nombre de tu halcón: ")
                    self.soldado.mascota = Mascota(nombre, "Halcón")
                    break
            except ValueError:
                print("Opción inválida.")
        
        print(f"\n¡{self.soldado.mascota.nombre} se une a tu equipo!")
    
    def elegir_novia(self):
        print("\n💕 CONFIGURAR RELACIÓN:")
        nombres = ["Ana", "Sofia", "Carmen", "Laura", "Isabel"]
        nombre = random.choice(nombres)
        respuesta = input(f"¿Quieres que {nombre} sea tu novia? (s/n): ")
        
        if respuesta.lower() == 's':
            self.soldado.novia = Novia(nombre)
            print(f"\n¡{nombre} es ahora tu novia! Cuídala bien.")
        else:
            print("Decides mantenerte soltera por ahora.")
    
    def bucle_principal(self):
        while True:
            self.mostrar_menu_principal()
            try:
                opcion = int(input("Selecciona una opción: "))
                
                if opcion == 1:
                    self.mostrar_estado()
                elif opcion == 2:
                    self.menu_misiones()
                elif opcion == 3:
                    self.menu_tienda()
                elif opcion == 4:
                    self.menu_mejoras()
                elif opcion == 5:
                    self.menu_relaciones()
                elif opcion == 6:
                    self.menu_mascota()
                elif opcion == 7:
                    self.menu_inventario()
                elif opcion == 8:
                    self.entrenar()
                elif opcion == 9:
                    self.descansar()
                elif opcion == 10:
                    self.guardar_juego()
                elif opcion == 11:
                    print("¡Hasta luego, soldado!")
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
    
    def mostrar_menu_principal(self):
        print("\n" + "=" * 50)
        print(f"🎯 SOLDADO {self.soldado.nombre.upper()} - NIVEL {self.soldado.nivel}")
        print("=" * 50)
        print("1. 📊 Ver Estado")
        print("2. ⚔️  Misiones")
        print("3. 🏪 Tienda")
        print("4. ⬆️  Mejoras")
        print("5. 💕 Relaciones")
        print("6. 🐾 Mascota")
        print("7. 🎒 Inventario")
        print("8. 🏋️  Entrenar")
        print("9. 😴 Descansar")
        print("10. 💾 Guardar")
        print("11. 🚪 Salir")
        print("=" * 50)
    
    def mostrar_estado(self):
        print("\n📊 ESTADO DEL SOLDADO:")
        print(f"Nombre: {self.soldado.nombre}")
        print(f"Nivel: {self.soldado.nivel}")
        print(f"HP: {self.soldado.hp}/{self.soldado.hp_max}")
        print(f"Energía: {self.soldado.energia}/{self.soldado.energia_max}")
        print(f"Experiencia: {self.soldado.exp}/{self.soldado.exp_siguiente}")
        print(f"Dinero: ${self.soldado.dinero}")
        print(f"Misiones completadas: {self.soldado.misiones_completadas}")
        print(f"Reputación: {self.soldado.reputacion}")
        
        print("\n⚔️ ATRIBUTOS:")
        print(f"Fuerza: {self.soldado.fuerza}")
        print(f"Agilidad: {self.soldado.agilidad}")
        print(f"Resistencia: {self.soldado.resistencia}")
        print(f"Puntería: {self.soldado.punteria}")
        print(f"Carisma: {self.soldado.carisma}")
        
        if self.soldado.arma_actual:
            print(f"\nArma equipada: {self.soldado.arma_actual.nombre}")
        
        if self.soldado.mascota:
            print(f"\nMascota: {self.soldado.mascota.nombre} ({self.soldado.mascota.tipo})")
            print(f"Nivel mascota: {self.soldado.mascota.nivel}")
            print(f"Lealtad: {self.soldado.mascota.lealtad}/100")
        
        if self.soldado.novia:
            print(f"\nNovia: {self.soldado.novia.nombre}")
            print(f"Nivel de amor: {self.soldado.novia.amor}/100")
    
    def menu_misiones(self):
        print("\n⚔️ MISIONES DISPONIBLES:")
        for i, mision in enumerate(self.misiones_disponibles, 1):
            if not mision.completada:
                print(f"{i}. {mision.nombre}")
                print(f"   Tipo: {mision.tipo} | Dificultad: {'⭐' * mision.dificultad}")
                print(f"   Recompensa: {mision.recompensa_exp} EXP, ${mision.recompensa_dinero}")
                print(f"   {mision.descripcion}")
                print()
        
        print("0. Volver al menú")
        
        try:
            opcion = int(input("Selecciona una misión: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= len(self.misiones_disponibles):
                mision = self.misiones_disponibles[opcion - 1]
                if not mision.completada:
                    self.ejecutar_mision(mision)
        except ValueError:
            print("Opción inválida.")
    
    def ejecutar_mision(self, mision):
        print(f"\n🎯 INICIANDO MISIÓN: {mision.nombre}")
        print(f"📋 {mision.descripcion}")
        
        if mision.tipo == "Combate":
            exito = self.mision_combate(mision)
        elif mision.tipo == "Sigilo":
            exito = self.mision_sigilo(mision)
        elif mision.tipo == "Rescate":
            exito = self.mision_rescate(mision)
        elif mision.tipo == "Intel":
            exito = self.mision_intel(mision)
        elif mision.tipo == "Protección":
            exito = self.mision_proteccion(mision)
        else:
            exito = self.mision_generica(mision)
        
        if exito:
            print(f"\n✅ ¡MISIÓN COMPLETADA CON ÉXITO!")
            self.soldado.exp += mision.recompensa_exp
            self.soldado.dinero += mision.recompensa_dinero
            self.soldado.misiones_completadas += 1
            self.soldado.reputacion += 10
            mision.completada = True
            
            # Posible loot
            if random.random() < 0.3:
                loot = self.generar_loot()
                print(f"🎁 Has encontrado: {loot['nombre']}")
                self.soldado.inventario.append(loot)
            
            self.verificar_subida_nivel()
        else:
            print(f"\n❌ Misión fallida. Pierdes energía.")
            self.soldado.energia -= 20
    
    def mision_combate(self, mision):
        print("\n⚔️ ENTRANDO EN COMBATE...")
        enemigos = random.randint(1, 3)
        
        for i in range(enemigos):
            enemigo = random.choice(self.enemigos).copy()
            print(f"\n🎯 Enemigo {i+1}: {enemigo['nombre']}")
            
            if not self.combate(enemigo):
                return False
        
        return True
    
    def mision_sigilo(self, mision):
        print("\n🤫 MISIÓN DE SIGILO...")
        probabilidad = 0.7
        
        # Bonus por agilidad y mascota
        if self.soldado.agilidad > 15:
            probabilidad += 0.1
        if self.soldado.mascota and self.soldado.mascota.tipo == "Gato":
            probabilidad += 0.15
        
        if random.random() < probabilidad:
            print("✅ Te infiltras exitosamente sin ser detectada")
            return True
        else:
            print("❌ ¡Te han detectado! Iniciando combate...")
            return self.mision_combate(mision)
    
    def mision_rescate(self, mision):
        print("\n🚁 MISIÓN DE RESCATE...")
        print("Localizas a los rehenes...")
        
        # Proteger a los rehenes durante el combate
        rehenes_hp = 100
        enemigos = 2
        
        for i in range(enemigos):
            enemigo = random.choice(self.enemigos).copy()
            print(f"\n🎯 Protegiendo rehenes de: {enemigo['nombre']}")
            
            # Los rehenes pueden ser heridos
            if random.random() < 0.3:
                daño_rehenes = random.randint(10, 20)
                rehenes_hp -= daño_rehenes
                print(f"💔 Los rehenes reciben {daño_rehenes} de daño")
            
            if not self.combate(enemigo):
                return False
        
        if rehenes_hp > 0:
            print(f"✅ Rehenes rescatados con éxito (HP: {rehenes_hp}/100)")
            return True
        else:
            print("❌ Los rehenes no sobrevivieron")
            return False
    
    def mision_intel(self, mision):
        print("\n🔍 MISIÓN DE INTELIGENCIA...")
        
        # Bonus por mascota halcón
        probabilidad = 0.8
        if self.soldado.mascota and self.soldado.mascota.tipo == "Halcón":
            probabilidad += 0.15
            print(f"🦅 {self.soldado.mascota.nombre} proporciona reconocimiento aéreo")
        
        if random.random() < probabilidad:
            print("✅ Información valiosa obtenida")
            return True
        else:
            print("❌ No se pudo obtener la información")
            return False
    
    def mision_proteccion(self, mision):
        print("\n🛡️ MISIÓN DE PROTECCIÓN...")
        vip_hp = 100
        oleadas = 3
        
        for i in range(oleadas):
            print(f"\n🌊 Oleada {i+1} de enemigos")
            enemigo = random.choice(self.enemigos).copy()
            
            # El VIP puede ser atacado
            if random.random() < 0.4:
                daño_vip = random.randint(15, 25)
                vip_hp -= daño_vip
                print(f"💔 El VIP recibe {daño_vip} de daño")
            
            if not self.combate(enemigo):
                return False
            
            if vip_hp <= 0:
                print("❌ El VIP ha muerto")
                return False
        
        print(f"✅ VIP protegido exitosamente (HP: {vip_hp}/100)")
        return True
    
    def mision_generica(self, mision):
        probabilidad = 0.6 + (self.soldado.nivel * 0.05)
        return random.random() < probabilidad
    
    def combate(self, enemigo):
        print(f"\n⚔️ COMBATE CONTRA {enemigo['nombre']}")
        enemigo_hp = enemigo['hp']
        
        while enemigo_hp > 0 and self.soldado.hp > 0:
            print(f"\n{self.soldado.nombre}: {self.soldado.hp}/{self.soldado.hp_max} HP")
            print(f"{enemigo['nombre']}: {enemigo_hp}/{enemigo['hp']} HP")
            
            print("\n1. Atacar")
            print("2. Habilidad especial")
            print("3. Usar mascota")
            print("4. Huir")
            
            try:
                accion = int(input("Elige tu acción: "))
                
                if accion == 1:
                    daño = self.calcular_daño()
                    enemigo_hp -= daño
                    print(f"💥 Infliges {daño} de daño")
                
                elif accion == 2:
                    if self.soldado.energia >= 20:
                        daño = self.calcular_daño() * 1.5
                        enemigo_hp -= int(daño)
                        self.soldado.energia -= 20
                        print(f"💥 Habilidad especial: {int(daño)} de daño")
                    else:
                        print("❌ No tienes suficiente energía")
                        continue
                
                elif accion == 3:
                    if self.soldado.mascota and self.soldado.mascota.hp > 0:
                        daño_mascota = 15 + self.soldado.mascota.nivel * 5
                        enemigo_hp -= daño_mascota
                        print(f"🐾 {self.soldado.mascota.nombre} ataca por {daño_mascota} de daño")
                    else:
                        print("❌ Tu mascota no puede atacar")
                        continue
                
                elif accion == 4:
                    print("🏃 Huyes del combate")
                    return False
                
                # Ataque del enemigo
                if enemigo_hp > 0:
                    daño_enemigo = random.randint(enemigo['daño'] - 5, enemigo['daño'] + 5)
                    # Reducir daño por armadura/resistencia
                    daño_reducido = max(1, daño_enemigo - self.soldado.resistencia // 2)
                    self.soldado.hp -= daño_reducido
                    print(f"💔 {enemigo['nombre']} te ataca por {daño_reducido} de daño")
                    
                    if self.soldado.hp <= 0:
                        print("💀 Has sido derrotada...")
                        self.soldado.hp = 1
                        return False
                        
            except ValueError:
                print("Opción inválida")
        
        if enemigo_hp <= 0:
            print(f"✅ ¡Has derrotado a {enemigo['nombre']}!")
            self.soldado.exp += enemigo['exp']
            self.soldado.dinero += enemigo['dinero']
            return True
        
        return False
    
    def calcular_daño(self):
        daño_base = self.soldado.fuerza + random.randint(5, 15)
        
        if self.soldado.arma_actual:
            daño_arma = self.soldado.arma_actual.daño
            # Precisión afecta la probabilidad de daño máximo
            if random.randint(1, 100) <= self.soldado.arma_actual.precisión:
                daño_total = daño_base + daño_arma
            else:
                daño_total = daño_base + (daño_arma // 2)
        else:
            daño_total = daño_base
        
        return max(1, daño_total)
    
    def menu_tienda(self):
        print("\n🏪 TIENDA MILITAR")
        print("1. Armas")
        print("2. Regalos")
        print("3. Vender loot")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona: "))
            if opcion == 1:
                self.tienda_armas()
            elif opcion == 2:
                self.tienda_regalos()
            elif opcion == 3:
                self.vender_loot()
        except ValueError:
            print("Opción inválida")
    
    def tienda_armas(self):
        print("\n🔫 TIENDA DE ARMAS:")
        for i, arma in enumerate(self.tienda_armas, 1):
            print(f"{i}. {arma.nombre} - ${arma.precio}")
            print(f"   Daño: {arma.daño} | Precisión: {arma.precisión}%")
        
        print("0. Volver")
        
        try:
            opcion = int(input("Comprar arma: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= len(self.tienda_armas):
                arma = self.tienda_armas[opcion - 1]
                if self.soldado.dinero >= arma.precio:
                    self.soldado.dinero -= arma.precio
                    self.soldado.armas.append(arma)
                    print(f"✅ Has comprado {arma.nombre}")
                else:
                    print("❌ No tienes suficiente dinero")
        except ValueError:
            print("Opción inválida")
    
    def tienda_regalos(self):
        if not self.soldado.novia:
            print("❌ Necesitas una novia para comprar regalos")
            return
        
        print("\n💝 TIENDA DE REGALOS:")
        for i, regalo in enumerate(self.tienda_regalos, 1):
            print(f"{i}. {regalo['nombre']} - ${regalo['precio']} (+{regalo['amor']} amor)")
        
        print("0. Volver")
        
        try:
            opcion = int(input("Comprar regalo: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= len(self.tienda_regalos):
                regalo = self.tienda_regalos[opcion - 1]
                if self.soldado.dinero >= regalo['precio']:
                    self.soldado.dinero -= regalo['precio']
                    self.soldado.regalos.append(regalo)
                    print(f"✅ Has comprado {regalo['nombre']}")
                else:
                    print("❌ No tienes suficiente dinero")
        except ValueError:
            print("Opción inválida")
    
    def vender_loot(self):
        if not self.soldado.inventario:
            print("❌ No tienes objetos para vender")
            return
        
        print("\n💰 VENDER LOOT:")
        for i, item in enumerate(self.soldado.inventario, 1):
            print(f"{i}. {item['nombre']} - ${item['precio']}")
        
        print("0. Volver")
        
        try:
            opcion = int(input("Vender objeto: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= len(self.soldado.inventario):
                item = self.soldado.inventario.pop(opcion - 1)
                self.soldado.dinero += item['precio']
                print(f"✅ Has vendido {item['nombre']} por ${item['precio']}")
        except ValueError:
            print("Opción inválida")
    
    def generar_loot(self):
        objetos = [
            {"nombre": "Munición", "precio": 50},
            {"nombre": "Kit médico", "precio": 100},
            {"nombre": "Mira telescópica", "precio": 200},
            {"nombre": "Chaleco antibalas", "precio": 300},
            {"nombre": "Granadas", "precio": 150},
            {"nombre": "Información clasificada", "precio": 500},
            {"nombre": "Componente de arma", "precio": 250}
        ]
        return random.choice(objetos)
    
    def menu_mejoras(self):
        print("\n⬆️ MEJORAS:")
        print(f"Puntos de habilidad disponibles: {self.soldado.puntos_habilidad}")
        print("1. Fuerza (+1) - 1 punto")
        print("2. Agilidad (+1) - 1 punto")
        print("3. Resistencia (+1) - 1 punto")
        print("4. Puntería (+1) - 1 punto")
        print("5. Carisma (+1) - 1 punto")
        print("6. Mejorar arma equipada")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona mejora: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= 5 and self.soldado.puntos_habilidad > 0:
                self.mejorar_atributo(opcion)
            elif opcion == 6:
                self.mejorar_arma()
            else:
                print("❌ No tienes puntos suficientes o opción inválida")
        except ValueError:
            print("Opción inválida")
    
    def mejorar_atributo(self, opcion):
        atributos = ["fuerza", "agilidad", "resistencia", "punteria", "carisma"]
        atributo = atributos[opcion - 1]
        
        setattr(self.soldado, atributo, getattr(self.soldado, atributo) + 1)
        self.soldado.puntos_habilidad -= 1
        print(f"✅ {atributo.capitalize()} mejorado a {getattr(self.soldado, atributo)}")
    
    def mejorar_arma(self):
        if not self.soldado.arma_actual:
            print("❌ No tienes un arma equipada")
            return
        
        costo = (self.soldado.arma_actual.nivel_mejora + 1) * 100
        
        if self.soldado.dinero >= costo:
            self.soldado.dinero -= costo
            self.soldado.arma_actual.nivel_mejora += 1
            self.soldado.arma_actual.daño += 5
            self.soldado.arma_actual.precisión += 2
            print(f"✅ {self.soldado.arma_actual.nombre} mejorado a nivel {self.soldado.arma_actual.nivel_mejora}")
        else:
            print(f"❌ Necesitas ${costo} para mejorar el arma")
    
    def menu_relaciones(self):
        if not self.soldado.novia:
            print("❌ No tienes novia actualmente")
            return
        
        print(f"\n💕 RELACIÓN CON {self.soldado.novia.nombre.upper()}")
        print(f"Nivel de amor: {self.soldado.novia.amor}/100")
        print(f"Estado: {'En peligro' if self.soldado.novia.en_peligro else 'Segura'}")
        print(f"Regalos recibidos: {len(self.soldado.novia.regalos_recibidos)}")
        
        print("\n1. Dar regalo")
        print("2. Pasar tiempo juntas")
        print("3. Misión de protección")
        print("4. Enviar mensaje")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona: "))
            if opcion == 1:
                self.dar_regalo()
            elif opcion == 2:
                self.pasar_tiempo()
            elif opcion == 3:
                self.mision_proteger_novia()
            elif opcion == 4:
                self.enviar_mensaje()
        except ValueError:
            print("Opción inválida")
    
    def dar_regalo(self):
        if not self.soldado.regalos:
            print("❌ No tienes regalos para dar")
            return
        
        print("\n🎁 REGALOS DISPONIBLES:")
        for i, regalo in enumerate(self.soldado.regalos, 1):
            print(f"{i}. {regalo['nombre']} (+{regalo['amor']} amor)")
        
        try:
            opcion = int(input("Dar regalo: ")) - 1
            if 0 <= opcion < len(self.soldado.regalos):
                regalo = self.soldado.regalos.pop(opcion)
                self.soldado.novia.amor += regalo['amor']
                self.soldado.novia.regalos_recibidos.append(regalo)
                print(f"💝 Le has dado {regalo['nombre']} a {self.soldado.novia.nombre}")
                print(f"❤️ Su amor aumentó a {self.soldado.novia.amor}/100")
        except ValueError:
            print("Opción inválida")
    
    def pasar_tiempo(self):
        if self.soldado.energia < 20:
            print("❌ No tienes suficiente energía")
            return
        
        self.soldado.energia -= 20
        amor_ganado = random.randint(5, 15)
        self.soldado.novia.amor += amor_ganado
        
        actividades = [
            "Caminan por el parque",
            "Ven una película juntas",
            "Cocinan una cena romántica",
            "Hablan bajo las estrellas",
            "Van a un café acogedor"
        ]
        
        actividad = random.choice(actividades)
        print(f"💕 {actividad}")
        print(f"❤️ Amor aumentó en {amor_ganado} puntos")
    
    def mision_proteger_novia(self):
        if not self.soldado.novia.en_peligro:
            # Crear situación de peligro
            if random.random() < 0.3:
                self.soldado.novia.en_peligro = True
                print(f"⚠️ ¡{self.soldado.novia.nombre} está en peligro!")
                print("Unos criminales la han amenazado")
            else:
                print("✅ Tu novia está segura por ahora")
                return
        
        print(f"\n🛡️ PROTEGIENDO A {self.soldado.novia.nombre}")
        print("Enfrentas a los criminales que la amenazan")
        
        enemigos = 2
        for i in range(enemigos):
            enemigo = {"nombre": "Criminal", "hp": 40, "daño": 15, "exp": 20, "dinero": 50}
            if not self.combate(enemigo):
                print(f"💔 No pudiste proteger a {self.soldado.novia.nombre}")
                self.soldado.novia.amor -= 20
                return
        
        print(f"✅ ¡Has protegido exitosamente a {self.soldado.novia.nombre}!")
        self.soldado.novia.en_peligro = False
        self.soldado.novia.amor += 25
        print(f"❤️ Su amor aumentó significativamente")
    
    def enviar_mensaje(self):
        if self.soldado.mascota and self.soldado.mascota.tipo == "Halcón":
            print(f"📨 {self.soldado.mascota.nombre} lleva tu mensaje")
            mensaje = input("Escribe tu mensaje: ")
            print(f"💌 Mensaje enviado: '{mensaje}'")
            self.soldado.novia.amor += 5
            self.soldado.mascota.lealtad += 5
        else:
            print("❌ Necesitas un halcón para enviar mensajes")
    
    def menu_mascota(self):
        if not self.soldado.mascota:
            print("❌ No tienes mascota")
            return
        
        mascota = self.soldado.mascota
        print(f"\n🐾 {mascota.nombre.upper()} - {mascota.tipo}")
        print(f"Nivel: {mascota.nivel}")
        print(f"HP: {mascota.hp}/{mascota.hp_max}")
        print(f"Lealtad: {mascota.lealtad}/100")
        print(f"Habilidades: {', '.join(mascota.habilidades)}")
        
        print("\n1. Entrenar mascota")
        print("2. Alimentar mascota")
        print("3. Jugar con mascota")
        print("4. Usar habilidad especial")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona: "))
            if opcion == 1:
                self.entrenar_mascota()
            elif opcion == 2:
                self.alimentar_mascota()
            elif opcion == 3:
                self.jugar_mascota()
            elif opcion == 4:
                self.habilidad_mascota()
        except ValueError:
            print("Opción inválida")
    
    def entrenar_mascota(self):
        if self.soldado.energia < 30:
            print("❌ No tienes suficiente energía")
            return
        
        self.soldado.energia -= 30
        exp_ganada = random.randint(20, 40)
        
        print(f"🎾 Entrenas con {self.soldado.mascota.nombre}")
        print(f"📈 Gana {exp_ganada} puntos de experiencia")
        
        # Subir nivel de mascota
        if exp_ganada > 30:
            self.soldado.mascota.nivel += 1
            self.soldado.mascota.hp_max += 10
            self.soldado.mascota.hp = self.soldado.mascota.hp_max
            print(f"🎉 ¡{self.soldado.mascota.nombre} subió al nivel {self.soldado.mascota.nivel}!")
    
    def alimentar_mascota(self):
        if self.soldado.dinero < 20:
            print("❌ No tienes suficiente dinero para comida")
            return
        
        self.soldado.dinero -= 20
        self.soldado.mascota.hp = self.soldado.mascota.hp_max
        self.soldado.mascota.lealtad += 10
        print(f"🍖 Alimentas a {self.soldado.mascota.nombre}")
        print(f"❤️ Su lealtad aumentó a {self.soldado.mascota.lealtad}/100")
    
    def jugar_mascota(self):
        if self.soldado.energia < 15:
            print("❌ No tienes suficiente energía")
            return
        
        self.soldado.energia -= 15
        self.soldado.mascota.lealtad += 15
        
        juegos = [
            "Juegas a buscar la pelota",
            "Haces trucos juntos",
            "Corres por el campo",
            "Practicas comandos"
        ]
        
        juego = random.choice(juegos)
        print(f"🎮 {juego}")
        print(f"❤️ Lealtad aumentó a {self.soldado.mascota.lealtad}/100")
    
    def habilidad_mascota(self):
        mascota = self.soldado.mascota
        
        if mascota.tipo == "Perro":
            print("🐕 Habilidades de perro:")
            print("1. Rastrear enemigos")
            print("2. Guardar perímetro")
            print("3. Ataque feroz")
        elif mascota.tipo == "Gato":
            print("🐱 Habilidades de gato:")
            print("1. Sigilo mejorado")
            print("2. Detectar trampas")
            print("3. Movimiento silencioso")
        elif mascota.tipo == "Halcón":
            print("🦅 Habilidades de halcón:")
            print("1. Reconocimiento aéreo")
            print("2. Entregar mensajes")
            print("3. Vigilancia elevada")
        
        try:
            opcion = int(input("Usar habilidad: "))
            if 1 <= opcion <= 3:
                habilidad = mascota.habilidades[opcion - 1]
                print(f"✨ {mascota.nombre} usa {habilidad}")
                
                if habilidad == "Rastreo":
                    print("🔍 Encuentra pistas de enemigos cercanos")
                elif habilidad == "Sigilo":
                    print("🤫 Tu próxima misión de sigilo tendrá bonus")
                elif habilidad == "Reconocimiento":
                    print("👁️ Revela información sobre el área")
                
                mascota.lealtad += 5
        except ValueError:
            print("Opción inválida")
    
    def menu_inventario(self):
        print("\n🎒 INVENTARIO:")
        
        print("\n🔫 ARMAS:")
        if self.soldado.armas:
            for i, arma in enumerate(self.soldado.armas, 1):
                estado = "EQUIPADA" if arma == self.soldado.arma_actual else "En inventario"
                print(f"{i}. {arma.nombre} - {estado}")
                print(f"   Daño: {arma.daño} | Precisión: {arma.precisión}% | Nivel: {arma.nivel_mejora}")
        else:
            print("No tienes armas")
        
        print("\n🎁 REGALOS:")
        if self.soldado.regalos:
            for regalo in self.soldado.regalos:
                print(f"- {regalo['nombre']} (+{regalo['amor']} amor)")
        else:
            print("No tienes regalos")
        
        print("\n📦 OBJETOS:")
        if self.soldado.inventario:
            for item in self.soldado.inventario:
                print(f"- {item['nombre']} (${item['precio']})")
        else:
            print("No tienes objetos")
        
        print("\n1. Equipar arma")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona: "))
            if opcion == 1:
                self.equipar_arma()
        except ValueError:
            print("Opción inválida")
    
    def equipar_arma(self):
        if not self.soldado.armas:
            print("❌ No tienes armas")
            return
        
        print("\n🔫 EQUIPAR ARMA:")
        for i, arma in enumerate(self.soldado.armas, 1):
            print(f"{i}. {arma.nombre}")
        
        try:
            opcion = int(input("Equipar arma: ")) - 1
            if 0 <= opcion < len(self.soldado.armas):
                self.soldado.arma_actual = self.soldado.armas[opcion]
                print(f"✅ {self.soldado.arma_actual.nombre} equipada")
        except ValueError:
            print("Opción inválida")
    
    def entrenar(self):
        print("\n🏋️ ENTRENAMIENTO:")
        print("1. Entrenamiento de fuerza (30 energía)")
        print("2. Entrenamiento de agilidad (30 energía)")
        print("3. Entrenamiento de puntería (30 energía)")
        print("4. Entrenamiento de resistencia (30 energía)")
        print("0. Volver")
        
        try:
            opcion = int(input("Selecciona: "))
            if opcion == 0:
                return
            elif 1 <= opcion <= 4:
                if self.soldado.energia >= 30:
                    self.soldado.energia -= 30
                    
                    # Probabilidad de mejorar atributo
                    if random.random() < 0.4:
                        if opcion == 1:
                            self.soldado.fuerza += 1
                            print("💪 ¡Fuerza mejorada!")
                        elif opcion == 2:
                            self.soldado.agilidad += 1
                            print("🏃 ¡Agilidad mejorada!")
                        elif opcion == 3:
                            self.soldado.punteria += 1
                            print("🎯 ¡Puntería mejorada!")
                        elif opcion == 4:
                            self.soldado.resistencia += 1
                            print("🛡️ ¡Resistencia mejorada!")
                    else:
                        print("📈 Buen entrenamiento, sigue así")
                    
                    # Ganar experiencia
                    self.soldado.exp += 10
                    self.verificar_subida_nivel()
                else:
                    print("❌ No tienes suficiente energía")
        except ValueError:
            print("Opción inválida")
    
    def descansar(self):
        print("\n😴 DESCANSANDO...")
        
        # Recuperar HP y energía
        hp_recuperado = min(50, self.soldado.hp_max - self.soldado.hp)
        energia_recuperada = min(80, self.soldado.energia_max - self.soldado.energia)
        
        self.soldado.hp += hp_recuperado
        self.soldado.energia += energia_recuperada
        
        print(f"💚 HP recuperado: +{hp_recuperado}")
        print(f"⚡ Energía recuperada: +{energia_recuperada}")
        
        # Recuperar mascota
        if self.soldado.mascota:
            mascota_hp = min(20, self.soldado.mascota.hp_max - self.soldado.mascota.hp)
            self.soldado.mascota.hp += mascota_hp
            print(f"🐾 {self.soldado.mascota.nombre} también descansó (+{mascota_hp} HP)")
        
        # Eventos aleatorios durante el descanso
        if random.random() < 0.2:
            eventos = [
                "Tienes un sueño inspirador (+5 puntos de experiencia)",
                "Encuentras dinero en tu uniforme (+50 dólares)",
                "Tu mascota encuentra algo interesante"
            ]
            evento = random.choice(eventos)
            print(f"🌙 {evento}")
            
            if "experiencia" in evento:
                self.soldado.exp += 5
            elif "dinero" in evento:
                self.soldado.dinero += 50
            elif "mascota" in evento and self.soldado.mascota:
                objeto = self.generar_loot()
                self.soldado.inventario.append(objeto)
                print(f"🎁 {self.soldado.mascota.nombre} encontró: {objeto['nombre']}")
    
    def verificar_subida_nivel(self):
        if self.soldado.exp >= self.soldado.exp_siguiente:
            self.soldado.nivel += 1
            self.soldado.exp -= self.soldado.exp_siguiente
            self.soldado.exp_siguiente = int(self.soldado.exp_siguiente * 1.5)
            
            # Beneficios por subir nivel
            self.soldado.hp_max += 20
            self.soldado.hp = self.soldado.hp_max
            self.soldado.energia_max += 15
            self.soldado.energia = self.soldado.energia_max
            self.soldado.puntos_habilidad += 2
            
            print(f"\n🎉 ¡NIVEL SUBIDO! Ahora eres nivel {self.soldado.nivel}")
            print(f"💚 HP máximo: {self.soldado.hp_max}")
            print(f"⚡ Energía máxima: {self.soldado.energia_max}")
            print(f"🔧 Puntos de habilidad: +2")
            
            # Bonus especial cada 5 niveles
            if self.soldado.nivel % 5 == 0:
                print("🌟 ¡BONUS ESPECIAL DE NIVEL!")
                self.soldado.dinero += 500
                print("💰 +500 dólares")
    
    def guardar_juego(self):
        try:
            datos = {
                "nombre": self.soldado.nombre,
                "nivel": self.soldado.nivel,
                "exp": self.soldado.exp,
                "hp": self.soldado.hp,
                "dinero": self.soldado.dinero,
                "atributos": {
                    "fuerza": self.soldado.fuerza,
                    "agilidad": self.soldado.agilidad,
                    "resistencia": self.soldado.resistencia,
                    "punteria": self.soldado.punteria,
                    "carisma": self.soldado.carisma
                },
                "misiones_completadas": self.soldado.misiones_completadas,
                "reputacion": self.soldado.reputacion
            }
            
            with open("soldado_save.json", "w") as archivo:
                json.dump(datos, archivo, indent=2)
            
            print("💾 Juego guardado exitosamente")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
    
    def cargar_juego(self):
        try:
            with open("soldado_save.json", "r") as archivo:
                datos = json.load(archivo)
            
            # Restaurar datos del soldado
            self.soldado = Soldado(datos["nombre"])
            self.soldado.nivel = datos["nivel"]
            self.soldado.exp = datos["exp"]
            self.soldado.hp = datos["hp"]
            self.soldado.dinero = datos["dinero"]
            
            # Restaurar atributos
            for attr, valor in datos["atributos"].items():
                setattr(self.soldado, attr, valor)
            
            self.soldado.misiones_completadas = datos["misiones_completadas"]
            self.soldado.reputacion = datos["reputacion"]
            
            print("📂 Juego cargado exitosamente")
            return True
        except FileNotFoundError:
            print("❌ No se encontró archivo de guardado")
            return False
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
            return False

# Función principal para ejecutar el juego
def main():
    juego = JuegoRPG()
    
    print("🎮 RPG SOLDADO ELITE")
    print("1. Nuevo juego")
    print("2. Cargar juego")
    
    try:
        opcion = int(input("Selecciona: "))
        if opcion == 1:
            juego.iniciar_juego()
        elif opcion == 2:
            if juego.cargar_juego():
                juego.bucle_principal()
            else:
                print("Iniciando nuevo juego...")
                juego.iniciar_juego()
    except ValueError:
        print("Iniciando nuevo juego...")
        juego.iniciar_juego()

if __name__ == "__main__":
    main()
