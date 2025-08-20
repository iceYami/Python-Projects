import random
import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class CreatureType(Enum):
    DRAGON = "Dragón"
    PHOENIX = "Fénix"
    SHADOWBEAST = "Bestia de las Sombras"
    CRYSTALWOLF = "Lobo de Cristal"
    VOIDSPIRIT = "Espíritu del Vacío"

class Faction(Enum):
    LIGHT = "Orden de la Luz"
    SHADOW = "Culto de las Sombras"
    CHAOS = "Legión del Caos"
    NATURE = "Círculo Natural"
    VOID = "Hermandad del Vacío"

class BattleType(Enum):
    ARENA = "Arena de Gladiadores"
    RITUAL = "Combate Ritual"
    TERRITORY = "Disputa Territorial"
    DIVINE = "Prueba Divina"

@dataclass
class Stats:
    health: int = 100
    mana: int = 50
    strength: int = 10
    agility: int = 10
    intelligence: int = 10
    willpower: int = 10
    corruption: int = 0
    divine_favor: int = 0

@dataclass
class Ability:
    name: str
    damage: int
    mana_cost: int
    special_effect: str

class MagicalCreature:
    def __init__(self, name: str, creature_type: CreatureType):
        self.name = name
        self.type = creature_type
        self.level = 1
        self.experience = 0
        self.stats = Stats()
        self.faction = None
        self.abilities = []
        self.inventory = []
        self.bonds = {}  # Relaciones con otras criaturas
        self.trauma = 0
        self.loyalty = 50
        self.fear = 0
        self.hunger = 100
        self.happiness = 50
        self.last_fed = time.time()
        self.battle_wins = 0
        self.battle_losses = 0
        self.scars = []
        self.alive = True
        
        self._initialize_creature()
    
    def _initialize_creature(self):
        """Inicializa las características basadas en el tipo de criatura"""
        base_abilities = {
            CreatureType.DRAGON: [
                Ability("Aliento de Fuego", 25, 15, "Quema al enemigo"),
                Ability("Garra Devastadora", 20, 10, "Causa sangrado"),
                Ability("Rugido Aterrador", 5, 8, "Reduce moral enemiga")
            ],
            CreatureType.PHOENIX: [
                Ability("Llamas Purificadoras", 22, 12, "Cura al usuario"),
                Ability("Renacimiento", 0, 30, "Revive con 50% HP"),
                Ability("Vuelo Solar", 18, 15, "Ataque desde las alturas")
            ],
            CreatureType.SHADOWBEAST: [
                Ability("Garras Sombrias", 28, 10, "Drena vida"),
                Ability("Invisibilidad", 0, 20, "Evade próximo ataque"),
                Ability("Miedo Primordial", 15, 12, "Paraliza al enemigo")
            ],
            CreatureType.CRYSTALWOLF: [
                Ability("Aullido Resonante", 20, 8, "Daño en área"),
                Ability("Piel de Cristal", 0, 15, "Refleja daño"),
                Ability("Mordida Perforante", 24, 12, "Ignora armadura")
            ],
            CreatureType.VOIDSPIRIT: [
                Ability("Toque del Vacío", 30, 18, "Drena maná"),
                Ability("Forma Etérea", 0, 25, "Inmune a ataques físicos"),
                Ability("Susurros de Locura", 12, 10, "Confunde al enemigo")
            ]
        }
        
        self.abilities = base_abilities[self.type].copy()
        
        # Ajustar stats según tipo
        if self.type == CreatureType.DRAGON:
            self.stats.strength += 8
            self.stats.health += 30
        elif self.type == CreatureType.PHOENIX:
            self.stats.intelligence += 6
            self.stats.mana += 20
        elif self.type == CreatureType.SHADOWBEAST:
            self.stats.agility += 7
            self.stats.corruption += 15
        elif self.type == CreatureType.CRYSTALWOLF:
            self.stats.willpower += 5
            self.stats.health += 20
        elif self.type == CreatureType.VOIDSPIRIT:
            self.stats.intelligence += 10
            self.stats.mana += 30
            self.stats.corruption += 20

class God:
    def __init__(self, name: str, domain: str, alignment: str):
        self.name = name
        self.domain = domain
        self.alignment = alignment
        self.followers = []
        self.power = random.randint(800, 1200)
        self.favor_given = {}
    
    def grant_blessing(self, creature: MagicalCreature):
        """Otorga bendición a una criatura"""
        blessing_power = random.randint(5, 15)
        creature.stats.divine_favor += blessing_power
        print(f"{self.name} otorga una bendición a {creature.name}!")
        return blessing_power
    
    def demand_sacrifice(self, creature: MagicalCreature):
        """Demanda sacrificio de la criatura"""
        sacrifice_cost = random.randint(10, 25)
        creature.stats.health -= sacrifice_cost
        creature.trauma += 5
        print(f"{self.name} demanda sacrificio de {creature.name}...")
        return sacrifice_cost

class GameWorld:
    def __init__(self):
        self.creatures = {}
        self.gods = self._create_gods()
        self.factions = {faction: [] for faction in Faction}
        self.arena_champions = []
        self.day = 1
        self.world_event = None
        self.dark_rituals_performed = 0
        self.total_battles = 0
        
    def _create_gods(self):
        """Crea los dioses del mundo"""
        return [
            God("Solarius", "Luz y Orden", "Lawful Good"),
            God("Umbrath", "Sombras y Secretos", "Chaotic Evil"),
            God("Bloodfang", "Guerra y Poder", "Chaotic Neutral"),
            God("Whisperwind", "Naturaleza y Vida", "Neutral Good"),
            God("Voidmother", "Vacío y Muerte", "Neutral Evil")
        ]

class CreatureSimulator:
    def __init__(self):
        self.world = GameWorld()
        self.player_creature = None
        self.running = True
        self.moral_choices = []
        
    def create_creature(self):
        """Crea una nueva criatura"""
        print("=== CREACIÓN DE CRIATURA ===")
        print("Tu alma ha sido vinculada a una criatura mágica en un mundo brutal...")
        
        name = input("Nombre de tu criatura: ")
        
        print("\nTipos de criatura disponibles:")
        for i, ctype in enumerate(CreatureType, 1):
            print(f"{i}. {ctype.value}")
        
        while True:
            try:
                choice = int(input("Elige el tipo (1-5): "))
                if 1 <= choice <= 5:
                    creature_type = list(CreatureType)[choice - 1]
                    break
                else:
                    print("Opción inválida. Elige entre 1 y 5.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
        
        self.player_creature = MagicalCreature(name, creature_type)
        self.world.creatures[name] = self.player_creature
        
        print(f"\n{name} el {creature_type.value} ha despertado en este mundo oscuro...")
        print(f"HP: {self.player_creature.stats.health}")
        print(f"Maná: {self.player_creature.stats.mana}")
        print(f"Fuerza: {self.player_creature.stats.strength}")
        print(f"Agilidad: {self.player_creature.stats.agility}")
        print(f"Inteligencia: {self.player_creature.stats.intelligence}")
        print(f"Voluntad: {self.player_creature.stats.willpower}")
        
        self.choose_faction()
    
    def choose_faction(self):
        """Permite elegir facción"""
        print("\n=== ELECCIÓN DE FACCIÓN ===")
        print("Las facciones del mundo te observan. Tu elección determinará tu destino...")
        
        factions_info = {
            Faction.LIGHT: "Buscan purificar el mundo, pero sus métodos pueden ser despiadados",
            Faction.SHADOW: "Abrazan la oscuridad y el poder prohibido",
            Faction.CHAOS: "Viven para la batalla y el conflicto constante",
            Faction.NATURE: "Protegen el equilibrio natural, sin importar el coste",
            Faction.VOID: "Buscan el fin de toda existencia"
        }
        
        for i, (faction, description) in enumerate(factions_info.items(), 1):
            print(f"{i}. {faction.value}: {description}")
        
        while True:
            try:
                choice = int(input("Elige tu facción (1-5): "))
                if 1 <= choice <= 5:
                    chosen_faction = list(Faction)[choice - 1]
                    self.player_creature.faction = chosen_faction
                    self.world.factions[chosen_faction].append(self.player_creature)
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
        
        print(f"\n{self.player_creature.name} se ha unido a {chosen_faction.value}!")
        
        # Consecuencias de la elección
        if chosen_faction == Faction.SHADOW:
            self.player_creature.stats.corruption += 10
            print("La oscuridad comienza a corromper tu alma...")
        elif chosen_faction == Faction.LIGHT:
            self.player_creature.stats.divine_favor += 10
            print("La luz divina te bendice, pero también te juzga...")
        elif chosen_faction == Faction.CHAOS:
            self.player_creature.stats.strength += 5
            self.player_creature.trauma += 5
            print("El caos te fortalece, pero también te marca...")
    
    def daily_care(self):
        """Cuidado diario de la criatura"""
        print(f"\n=== DÍA {self.world.day} ===")
        print(f"Estado de {self.player_creature.name}:")
        print(f"HP: {self.player_creature.stats.health}/100")
        print(f"Hambre: {self.player_creature.hunger}/100")
        print(f"Felicidad: {self.player_creature.happiness}/100")
        print(f"Lealtad: {self.player_creature.loyalty}/100")
        print(f"Miedo: {self.player_creature.fear}/100")
        print(f"Trauma: {self.player_creature.trauma}/100")
        print(f"Corrupción: {self.player_creature.stats.corruption}/100")
        
        if self.player_creature.scars:
            print(f"Cicatrices: {', '.join(self.player_creature.scars)}")
        
        # Degradación natural
        self.player_creature.hunger -= random.randint(15, 25)
        self.player_creature.happiness -= random.randint(5, 15)
        
        if self.player_creature.hunger <= 0:
            self.player_creature.stats.health -= 20
            self.player_creature.fear += 10
            print("¡Tu criatura se está muriendo de hambre!")
        
        if self.player_creature.happiness <= 20:
            self.player_creature.loyalty -= 10
            print("Tu criatura está perdiendo la lealtad...")
        
        if self.player_creature.trauma >= 80:
            print("Tu criatura está al borde del colapso mental...")
            if random.random() < 0.3:
                print("¡Tu criatura ha sufrido un episodio psicótico!")
                self.player_creature.stats.health -= 30
                self.player_creature.loyalty -= 20
    
    def feed_creature(self):
        """Alimenta a la criatura"""
        print("\n=== ALIMENTACIÓN ===")
        print("¿Qué le darás de comer?")
        print("1. Comida normal (Hambre +30)")
        print("2. Carne fresca (Hambre +50, Fuerza +2)")
        print("3. Poción mágica (Hambre +20, Maná +10)")
        print("4. Comida corrompida (Hambre +40, Corrupción +15)")
        print("5. Sacrificio ritual (Hambre +60, Trauma +20, Poder +5)")
        
        choice = input("Elige (1-5): ")
        
        if choice == "1":
            self.player_creature.hunger = min(100, self.player_creature.hunger + 30)
            print("Tu criatura come tranquilamente.")
        elif choice == "2":
            self.player_creature.hunger = min(100, self.player_creature.hunger + 50)
            self.player_creature.stats.strength += 2
            print("El sabor de la carne fresca excita a tu criatura.")
        elif choice == "3":
            self.player_creature.hunger = min(100, self.player_creature.hunger + 20)
            self.player_creature.stats.mana += 10
            print("La poción mágica restaura las energías místicas.")
        elif choice == "4":
            self.player_creature.hunger = min(100, self.player_creature.hunger + 40)
            self.player_creature.stats.corruption += 15
            print("La comida corrompida fortalece a tu criatura, pero mancha su alma.")
            self.moral_choices.append("Alimentó con comida corrompida")
        elif choice == "5":
            self.player_creature.hunger = min(100, self.player_creature.hunger + 60)
            self.player_creature.trauma += 20
            self.player_creature.stats.strength += 5
            print("El ritual de sacrificio llena de poder a tu criatura, pero la marca para siempre.")
            self.moral_choices.append("Realizó sacrificio ritual para alimentar")
        
        self.player_creature.last_fed = time.time()
    
    def train_creature(self):
        """Entrena a la criatura"""
        print("\n=== ENTRENAMIENTO ===")
        print("¿Qué tipo de entrenamiento realizarás?")
        print("1. Entrenamiento básico (Mejora stats moderadamente)")
        print("2. Entrenamiento intensivo (Mejora stats mucho, +Trauma)")
        print("3. Entrenamiento con dolor (Mejora stats extremo, +Trauma alto)")
        print("4. Meditación (Reduce trauma, mejora voluntad)")
        print("5. Ritual oscuro (Mejora poder, +Corrupción)")
        
        choice = input("Elige (1-5): ")
        
        if choice == "1":
            stat_gain = random.randint(1, 3)
            self.player_creature.stats.strength += stat_gain
            self.player_creature.stats.agility += stat_gain
            self.player_creature.happiness += 5
            print(f"Entrenamiento completado. Stats mejoradas en {stat_gain}.")
        
        elif choice == "2":
            stat_gain = random.randint(3, 6)
            self.player_creature.stats.strength += stat_gain
            self.player_creature.stats.agility += stat_gain
            self.player_creature.trauma += 10
            self.player_creature.happiness -= 10
            print(f"Entrenamiento intensivo completado. Stats mejoradas en {stat_gain}.")
            print("Tu criatura está exhausta y traumatizada.")
        
        elif choice == "3":
            stat_gain = random.randint(5, 10)
            self.player_creature.stats.strength += stat_gain
            self.player_creature.stats.agility += stat_gain
            self.player_creature.trauma += 25
            self.player_creature.fear += 15
            self.player_creature.loyalty -= 10
            print(f"Entrenamiento brutal completado. Stats mejoradas en {stat_gain}.")
            print("Tu criatura te mira con miedo y resentimiento.")
            self.moral_choices.append("Usó entrenamiento con dolor")
        
        elif choice == "4":
            self.player_creature.trauma = max(0, self.player_creature.trauma - 15)
            self.player_creature.stats.willpower += 3
            self.player_creature.happiness += 10
            print("La meditación calma la mente de tu criatura.")
        
        elif choice == "5":
            self.player_creature.stats.strength += 8
            self.player_creature.stats.intelligence += 5
            self.player_creature.stats.corruption += 25
            self.player_creature.trauma += 15
            print("El ritual oscuro infunde poder prohibido en tu criatura.")
            print("Algo fundamental ha cambiado en su esencia...")
            self.moral_choices.append("Realizó ritual oscuro de entrenamiento")
    
    def battle_system(self):
        """Sistema de combate"""
        print("\n=== ARENA DE COMBATE ===")
        print("¿Dónde quieres que luche tu criatura?")
        print("1. Arena de gladiadores (Recompensas altas, riesgo alto)")
        print("2. Combate ritual (Moderado, favorece divino)")
        print("3. Pelea callejera (Riesgo bajo, recompensas bajas)")
        print("4. Combate a muerte (Máximo riesgo y recompensa)")
        
        choice = input("Elige (1-4): ")
        
        # Crear enemigo
        enemy_types = list(CreatureType)
        enemy_type = random.choice(enemy_types)
        enemy = MagicalCreature(f"Enemigo {enemy_type.value}", enemy_type)
        enemy.level = self.player_creature.level + random.randint(-1, 2)
        
        # Ajustar stats del enemigo según nivel
        stat_bonus = (enemy.level - 1) * 5
        enemy.stats.health += stat_bonus
        enemy.stats.strength += stat_bonus // 2
        enemy.stats.agility += stat_bonus // 2
        
        print(f"\nTu oponente: {enemy.name} (Nivel {enemy.level})")
        print(f"HP: {enemy.stats.health}")
        
        # Determinar tipo de combate
        if choice == "1":
            battle_type = BattleType.ARENA
            crowd_pressure = True
        elif choice == "2":
            battle_type = BattleType.RITUAL
            crowd_pressure = False
        elif choice == "3":
            battle_type = BattleType.TERRITORY
            crowd_pressure = False
        elif choice == "4":
            battle_type = BattleType.ARENA
            crowd_pressure = True
            enemy.stats.health += 50  # Combate a muerte es más difícil
        
        # Combate
        player_hp = self.player_creature.stats.health
        enemy_hp = enemy.stats.health
        turn = 1
        
        while player_hp > 0 and enemy_hp > 0:
            print(f"\n--- Turno {turn} ---")
            print(f"Tu HP: {player_hp}/{self.player_creature.stats.health}")
            print(f"Enemigo HP: {enemy_hp}/{enemy.stats.health}")
            
            print("\nTus habilidades:")
            for i, ability in enumerate(self.player_creature.abilities, 1):
                print(f"{i}. {ability.name} (Daño: {ability.damage}, Maná: {ability.mana_cost})")
            
            if crowd_pressure and random.random() < 0.3:
                print("¡La multitud grita pidiendo sangre!")
                self.player_creature.fear += 5
            
            # Turno del jugador
            try:
                ability_choice = int(input("Elige habilidad (1-3): ")) - 1
                if 0 <= ability_choice < len(self.player_creature.abilities):
                    ability = self.player_creature.abilities[ability_choice]
                    
                    if self.player_creature.stats.mana >= ability.mana_cost:
                        self.player_creature.stats.mana -= ability.mana_cost
                        
                        # Calcular daño
                        base_damage = ability.damage
                        stat_bonus = self.player_creature.stats.strength // 2
                        total_damage = base_damage + stat_bonus + random.randint(-5, 5)
                        
                        enemy_hp -= total_damage
                        print(f"¡{ability.name} inflige {total_damage} puntos de daño!")
                        
                        # Efectos especiales
                        if "Quema" in ability.special_effect:
                            print("¡El enemigo está ardiendo!")
                        elif "Drena" in ability.special_effect:
                            heal = total_damage // 3
                            player_hp = min(self.player_creature.stats.health, player_hp + heal)
                            print(f"Drenas {heal} puntos de vida!")
                    else:
                        print("¡No tienes suficiente maná!")
                        continue
                else:
                    print("Habilidad inválida!")
                    continue
            except ValueError:
                print("Entrada inválida!")
                continue
            
            # Turno del enemigo
            if enemy_hp > 0:
                enemy_ability = random.choice(enemy.abilities)
                enemy_damage = enemy_ability.damage + random.randint(-3, 3)
                player_hp -= enemy_damage
                print(f"¡El enemigo usa {enemy_ability.name} y te inflige {enemy_damage} puntos de daño!")
            
            turn += 1
        
        # Resolución del combate
        if player_hp > 0:
            print(f"\n¡{self.player_creature.name} ha vencido!")
            self.player_creature.battle_wins += 1
            self.player_creature.experience += 50
            
            # Recompensas según tipo de combate
            if choice == "1":  # Arena
                print("¡La multitud rughe tu nombre!")
                self.player_creature.happiness += 20
                reward = random.randint(100, 200)
                print(f"Recibes {reward} monedas de oro!")
            elif choice == "4":  # Combate a muerte
                print("Has sobrevivido al combate más brutal...")
                self.player_creature.trauma += 30
                self.player_creature.stats.strength += 5
                scar = random.choice(["Cicatriz en el rostro", "Garra perdida", "Ojo dañado", "Cojera permanente"])
                self.player_creature.scars.append(scar)
                print(f"Tu criatura queda marcada: {scar}")
                
                # Elección moral después del combate
                print("\nEl enemigo yace herido pero vivo. ¿Qué haces?")
                print("1. Darle muerte (Finalizar su sufrimiento)")
                print("2. Dejarlo vivir (Mostrar misericordia)")
                print("3. Torturarlo (Mandar un mensaje)")
                
                mercy_choice = input("Elige (1-3): ")
                if mercy_choice == "1":
                    print("Das el golpe final. Una muerte rápida.")
                    self.player_creature.stats.corruption += 10
                elif mercy_choice == "2":
                    print("Muestras misericordia. La multitud está dividida.")
                    self.player_creature.stats.divine_favor += 10
                elif mercy_choice == "3":
                    print("Prolongas su agonía. La multitud grita enloquecida.")
                    self.player_creature.stats.corruption += 25
                    self.player_creature.trauma += 10
                    self.moral_choices.append("Torturó al enemigo derrotado")
            
            # Subir de nivel
            if self.player_creature.experience >= 100 * self.player_creature.level:
                self.level_up()
                
        else:
            print(f"\n{self.player_creature.name} ha sido derrotado...")
            self.player_creature.battle_losses += 1
            self.player_creature.trauma += 20
            self.player_creature.fear += 15
            self.player_creature.loyalty -= 10
            self.player_creature.stats.health = max(1, self.player_creature.stats.health - 30)
            
            # Consecuencias de la derrota
            if choice == "4":  # Combate a muerte
                print("¡Tu criatura está al borde de la muerte!")
                if random.random() < 0.3:
                    print("¡Tu criatura ha muerto en el combate!")
                    self.player_creature.alive = False
                    return False
        
        self.world.total_battles += 1
        return True
    
    def level_up(self):
        """Subir de nivel"""
        self.player_creature.level += 1
        self.player_creature.experience = 0
        
        print(f"\n¡{self.player_creature.name} ha subido al nivel {self.player_creature.level}!")
        print("Elige qué estadística mejorar:")
        print("1. Salud (+20 HP)")
        print("2. Fuerza (+5)")
        print("3. Agilidad (+5)")
        print("4. Inteligencia (+5)")
        print("5. Voluntad (+5)")
        
        choice = input("Elige (1-5): ")
        
        if choice == "1":
            self.player_creature.stats.health += 20
            print("¡Salud mejorada!")
        elif choice == "2":
            self.player_creature.stats.strength += 5
            print("¡Fuerza mejorada!")
        elif choice == "3":
            self.player_creature.stats.agility += 5
            print("¡Agilidad mejorada!")
        elif choice == "4":
            self.player_creature.stats.intelligence += 5
            print("¡Inteligencia mejorada!")
        elif choice == "5":
            self.player_creature.stats.willpower += 5
            print("¡Voluntad mejorada!")
    
    def divine_intervention(self):
        """Intervención divina"""
        print("\n=== INTERVENCIÓN DIVINA ===")
        god = random.choice(self.world.gods)
        
        print(f"¡{god.name}, {god.domain}, se manifiesta!")
        
        if god.alignment == "Lawful Good":
            print(f"{god.name} observa tus acciones con juicio divino.")
            if self.player_creature.stats.corruption > 50:
                print("¡Tu corrupción no pasa desapercibida!")
                punishment = random.randint(15, 30)
                self.player_creature.stats.health -= punishment
                print(f"Recibes {punishment} puntos de daño divino.")
            else:
                blessing = god.grant_blessing(self.player_creature)
                self.player_creature.stats.health += blessing
        
        elif god.alignment == "Chaotic Evil":
            print(f"{god.name} se deleita con tu oscuridad.")
            if self.player_creature.stats.corruption > 30:
                print("¡Tu corrupción es recompensada!")
                self.player_creature.stats.strength += 5
                self.player_creature.stats.corruption += 10
            else:
                print("¡Tu pureza es repugnante!")
                god.demand_sacrifice(self.player_creature)
        
        elif god.alignment == "Neutral Evil":
            print(f"{god.name} exige un precio por su atención.")
            print("¿Aceptas hacer un trato con esta entidad?")
            print("1. Aceptar (Ganar poder, perder alma)")
            print("2. Rechazar (Mantener integridad)")
            
            choice = input("Elige (1-2): ")
            if choice == "1":
                print("¡Haces un pacto con la oscuridad!")
                self.player_creature.stats.strength += 10
                self.player_creature.stats.intelligence += 5
                self.player_creature.stats.corruption += 40
                self.player_creature.trauma += 20
                print("El poder fluye por ti, pero algo se pierde para siempre...")
                self.moral_choices.append("Hizo pacto con entidad maligna")
            else:
                print("Rechazas el trato. Tu alma permanece intacta.")
                self.player_creature.stats.divine_favor += 15
    
    def world_event(self):
        """Eventos del mundo"""
        events = [
            "plague", "war", "divine_wrath", "corruption_surge", 
            "arena_tournament", "ritual_sacrifice", "faction_war"
        ]
        
        event = random.choice(events)
        print(f"\n=== EVENTO MUNDIAL ===")
        
        if event == "plague":
            print("¡Una plaga mística se extiende por el mundo!")
            if random.random() < 0.4:
                print("¡Tu criatura ha sido infectada!")
                self.player_creature.stats.health -= 30
                self.player_creature.trauma += 15
                print("La enfermedad la debilita y aterroriza...")
        
        elif event == "war":
            print("¡Ha estallado una guerra entre facciones!")
            if self.player_creature.faction:
                print(f"¡{self.player_creature.faction.value} está en guerra!")
                print("¿Participarás en la batalla?")
                print("1. Luchar valientemente (Riesgo alto, honor)")
                print("2. Evitar el combate (Seguridad, deshonor)")
                print("3. Cambiar de bando (Traición)")
                
                choice = input("Elige (1-3): ")
                if choice == "1":
                    print("¡Tu criatura marcha a la guerra!")
                    if random.random() < 0.6:
                        print("¡Sobrevive a la batalla!")
                        self.player_creature.experience += 100
                        self.player_creature.trauma += 25
                        self.player_creature.loyalty += 15
                        war_scar = random.choice(["Cicatriz de guerra", "Herida de batalla", "Marca de honor"])
                        self.player_creature.scars.append(war_scar)
                    else:
                        print("¡Tu criatura es gravemente herida!")
                        self.player_creature.stats.health -= 50
                        self.player_creature.trauma += 40
                elif choice == "2":
                    print("Tu criatura se oculta durante la guerra...")
                    self.player_creature.loyalty -= 20
                    self.player_creature.fear += 10
                elif choice == "3":
                    print("¡Tu criatura traiciona a su facción!")
                    old_faction = self.player_creature.faction
                    new_faction = random.choice([f for f in Faction if f != old_faction])
                    self.player_creature.faction = new_faction
                    self.player_creature.stats.corruption += 30
                    self.player_creature.trauma += 20
                    print(f"Ahora pertenece a {new_faction.value}")
                    self.moral_choices.append("Traicionó a su facción en guerra")
        
        elif event == "divine_wrath":
            print("¡La ira divina se desata sobre el mundo!")
            self.divine_intervention()
        
        elif event == "corruption_surge":
            print("¡Una oleada de corrupción arrasa la tierra!")
            self.player_creature.stats.corruption += random.randint(15, 30)
            print("La corrupción impregna a tu criatura...")
            if self.player_creature.stats.corruption > 80:
                print("¡Tu criatura está completamente corrompida!")
                self.player_creature.type = CreatureType.SHADOWBEAST
                print("Su naturaleza ha cambiado para siempre...")
        
        elif event == "arena_tournament":
            print("¡Se anuncia un gran torneo en la arena!")
            print("¿Participarás en el torneo de gladiadores?")
            print("1. Participar (Múltiples combates, gran recompensa)")
            print("2. Declinar (Perder oportunidad)")
            
            choice = input("Elige (1-2): ")
            if choice == "1":
                self.tournament_mode()
        
        elif event == "ritual_sacrifice":
            print("¡Los dioses demandan un gran sacrificio!")
            print("¿Participarás en el ritual?")
            print("1. Sacrificar parte de tu esencia (Perder stats, ganar favor)")
            print("2. Ofrecer a otra criatura (Ganar poder, perder moralidad)")
            print("3. Rechazar participar (Mantener integridad)")
            
            choice = input("Elige (1-3): ")
            if choice == "1":
                self.player_creature.stats.health -= 30
                self.player_creature.stats.strength -= 5
                self.player_creature.stats.divine_favor += 25
                print("Tu sacrificio es aceptado...")
            elif choice == "2":
                print("¡Ofreces a otra criatura al altar!")
                self.player_creature.stats.strength += 10
                self.player_creature.stats.corruption += 35
                self.player_creature.trauma += 25
                print("El poder fluye hacia ti mientras otra alma se desvanece...")
                self.moral_choices.append("Sacrificó otra criatura")
            elif choice == "3":
                print("Rechazas participar en el ritual.")
                self.player_creature.stats.divine_favor += 5
        
        elif event == "faction_war":
            print("¡Las facciones se enfrentan en una guerra total!")
            if self.player_creature.faction:
                print(f"¡{self.player_creature.faction.value} necesita tu ayuda!")
                self.faction_war_event()
    
    def tournament_mode(self):
        """Modo torneo de gladiadores"""
        print("\n=== TORNEO DE GLADIADORES ===")
        print("¡Bienvenido al torneo más brutal del mundo!")
        
        victories = 0
        total_rounds = 5
        
        for round_num in range(1, total_rounds + 1):
            print(f"\n--- RONDA {round_num} ---")
            
            # Enemigos más fuertes cada ronda
            enemy_type = random.choice(list(CreatureType))
            enemy = MagicalCreature(f"Campeón {enemy_type.value}", enemy_type)
            enemy.level = self.player_creature.level + round_num
            
            # Hacer enemigo más fuerte
            enemy.stats.health += round_num * 20
            enemy.stats.strength += round_num * 3
            enemy.stats.agility += round_num * 2
            
            print(f"Oponente: {enemy.name} (Nivel {enemy.level})")
            print(f"HP: {enemy.stats.health}")
            
            # Efectos especiales por ronda
            if round_num == 3:
                print("¡La multitud está enloquecida! +Presión")
                self.player_creature.fear += 10
            elif round_num == 4:
                print("¡Llueven armas desde las gradas!")
                weapon_bonus = random.randint(5, 15)
                self.player_creature.stats.strength += weapon_bonus
                print(f"Bonificación temporal de fuerza: +{weapon_bonus}")
            elif round_num == 5:
                print("¡COMBATE FINAL! ¡Todo o nada!")
                enemy.stats.health += 50
                enemy.stats.strength += 10
            
            # Combate simplificado para torneo
            if not self.quick_battle(enemy):
                print(f"¡Derrotado en la ronda {round_num}!")
                self.player_creature.trauma += 30
                self.player_creature.loyalty -= 15
                return False
            
            victories += 1
            print(f"¡Victoria en la ronda {round_num}!")
            
            # Curación entre rondas (limitada)
            heal_amount = random.randint(10, 25)
            self.player_creature.stats.health = min(100, self.player_creature.stats.health + heal_amount)
            
            # Oportunidad de retirarse
            if round_num < total_rounds:
                print("\n¿Continuar al siguiente round?")
                print("1. Continuar luchando")
                print("2. Retirarse con las ganancias")
                
                choice = input("Elige (1-2): ")
                if choice == "2":
                    print("Te retiras del torneo.")
                    break
        
        # Recompensas finales
        print(f"\n¡Torneo completado con {victories} victorias!")
        
        if victories == total_rounds:
            print("¡CAMPEÓN ABSOLUTO!")
            self.player_creature.experience += 500
            self.player_creature.stats.strength += 15
            self.player_creature.stats.agility += 10
            self.player_creature.happiness += 50
            print("Tu criatura es ahora una leyenda viviente!")
            self.player_creature.scars.append("Cicatriz del Campeón")
        elif victories >= 3:
            print("¡Excelente desempeño!")
            self.player_creature.experience += 200
            self.player_creature.stats.strength += 8
        else:
            print("Un esfuerzo valiente, pero no suficiente.")
            self.player_creature.experience += 50
        
        self.player_creature.trauma += victories * 5
        return True
    
    def quick_battle(self, enemy):
        """Combate rápido para eventos especiales"""
        player_hp = self.player_creature.stats.health
        enemy_hp = enemy.stats.health
        
        while player_hp > 0 and enemy_hp > 0:
            # Ataque del jugador
            player_damage = self.player_creature.stats.strength + random.randint(5, 15)
            enemy_hp -= player_damage
            
            if enemy_hp <= 0:
                break
            
            # Ataque del enemigo
            enemy_damage = enemy.stats.strength + random.randint(5, 15)
            player_hp -= enemy_damage
        
        # Actualizar HP real
        if player_hp > 0:
            self.player_creature.stats.health = max(1, player_hp)
            return True
        else:
            self.player_creature.stats.health = 1
            return False
    
    def faction_war_event(self):
        """Evento de guerra entre facciones"""
        print("\n=== GUERRA DE FACCIONES ===")
        print("Las facciones se enfrentan en una batalla épica!")
        
        enemy_factions = [f for f in Faction if f != self.player_creature.faction]
        enemy_faction = random.choice(enemy_factions)
        
        print(f"{self.player_creature.faction.value} vs {enemy_faction.value}")
        
        print("\n¿Cuál será tu rol en la guerra?")
        print("1. Liderar un ataque (Alto riesgo, alta recompensa)")
        print("2. Defender tu territorio (Riesgo moderado)")
        print("3. Sabotear al enemigo (Riesgo bajo, métodos cuestionables)")
        print("4. Negociar la paz (Evitar violencia)")
        
        choice = input("Elige (1-4): ")
        
        if choice == "1":
            print("¡Lideras una carga contra el enemigo!")
            success_chance = 0.6
            if random.random() < success_chance:
                print("¡La batalla es un éxito!")
                self.player_creature.experience += 150
                self.player_creature.stats.strength += 8
                self.player_creature.loyalty += 20
                self.player_creature.happiness += 25
                print("¡Tu facción te considera un héroe!")
            else:
                print("¡La batalla es un desastre!")
                self.player_creature.stats.health -= 40
                self.player_creature.trauma += 35
                self.player_creature.loyalty -= 10
                self.player_creature.scars.append("Herida de guerra")
        
        elif choice == "2":
            print("Defiendes tu territorio con honor.")
            self.player_creature.experience += 75
            self.player_creature.trauma += 20
            self.player_creature.loyalty += 10
            print("Una defensa sólida y honorable.")
        
        elif choice == "3":
            print("Usas tácticas de sabotaje...")
            self.player_creature.stats.corruption += 20
            self.player_creature.stats.intelligence += 5
            self.player_creature.trauma += 15
            print("Efectivo, pero moralmente cuestionable.")
            self.moral_choices.append("Usó sabotaje en guerra")
        
        elif choice == "4":
            print("Intentas negociar la paz...")
            if random.random() < 0.3:
                print("¡Logras un alto el fuego!")
                self.player_creature.stats.divine_favor += 25
                self.player_creature.stats.intelligence += 8
                self.player_creature.happiness += 30
                print("Tu diplomacia salva muchas vidas.")
            else:
                print("Las negociaciones fallan.")
                self.player_creature.loyalty -= 15
                print("Algunos te ven como un cobarde.")
    
    def check_relationships(self):
        """Revisa las relaciones de la criatura"""
        print("\n=== RELACIONES ===")
        
        if not self.player_creature.bonds:
            print("Tu criatura no tiene relaciones especiales.")
            return
        
        for creature_name, relationship in self.player_creature.bonds.items():
            print(f"{creature_name}: {relationship}")
    
    def moral_judgment(self):
        """Juicio moral de las acciones"""
        print("\n=== JUICIO MORAL ===")
        
        if not self.moral_choices:
            print("No has tomado decisiones moralmente significativas.")
            return
        
        print("Tus acciones han sido registradas:")
        for choice in self.moral_choices:
            print(f"- {choice}")
        
        corruption_level = self.player_creature.stats.corruption
        
        if corruption_level >= 80:
            print("\n¡Tu criatura está completamente corrompida!")
            print("Su alma está perdida en la oscuridad...")
            print("Los dioses malignos sonríen, mientras que los benevolentes lloran.")
        elif corruption_level >= 60:
            print("\nTu criatura está profundamente corrompida.")
            print("Pocas esperanzas quedan de redención.")
        elif corruption_level >= 40:
            print("\nTu criatura camina por un sendero oscuro.")
            print("Aún hay tiempo para la redención... quizás.")
        elif corruption_level >= 20:
            print("\nTu criatura ha cometido actos cuestionables.")
            print("El camino de la luz aún está abierto.")
        else:
            print("\nTu criatura mantiene su pureza.")
            print("Los dioses benevolentes sonríen sobre ti.")
    
    def creature_death(self):
        """Maneja la muerte de la criatura"""
        print("\n=== FINAL ===")
        print(f"{self.player_creature.name} ha llegado al final de su existencia...")
        
        if self.player_creature.stats.corruption >= 80:
            print("Muere corrompida, su alma perdida en la oscuridad eterna.")
            print("Los dioses malignos reclaman su esencia.")
        elif self.player_creature.stats.divine_favor >= 50:
            print("Muere en paz, su alma purificada por sus acciones.")
            print("Los dioses benevolentes la reciben con brazos abiertos.")
        else:
            print("Muere como vivió, en algún lugar entre la luz y la oscuridad.")
            print("Su destino final permanece incierto...")
        
        print(f"\nEstadísticas finales:")
        print(f"Nivel: {self.player_creature.level}")
        print(f"Batallas ganadas: {self.player_creature.battle_wins}")
        print(f"Batallas perdidas: {self.player_creature.battle_losses}")
        print(f"Corrupción: {self.player_creature.stats.corruption}")
        print(f"Favor divino: {self.player_creature.stats.divine_favor}")
        print(f"Trauma acumulado: {self.player_creature.trauma}")
        
        if self.player_creature.scars:
            print(f"Cicatrices: {', '.join(self.player_creature.scars)}")
        
        self.moral_judgment()
    
    def main_menu(self):
        """Menú principal del juego"""
        while self.running and self.player_creature.alive:
            print(f"\n=== MENÚ PRINCIPAL - DÍA {self.world.day} ===")
            print(f"Criatura: {self.player_creature.name} (Nivel {self.player_creature.level})")
            print(f"HP: {self.player_creature.stats.health}/100")
            print(f"Hambre: {self.player_creature.hunger}/100")
            print(f"Trauma: {self.player_creature.trauma}/100")
            print(f"Corrupción: {self.player_creature.stats.corruption}/100")
            
            print("\n¿Qué deseas hacer?")
            print("1. Alimentar criatura")
            print("2. Entrenar criatura")
            print("3. Combatir en arena")
            print("4. Meditar/Descansar")
            print("5. Ver estadísticas completas")
            print("6. Verificar relaciones")
            print("7. Pasar el día")
            print("8. Salir del juego")
            
            choice = input("Elige una opción (1-8): ")
            
            if choice == "1":
                self.feed_creature()
            elif choice == "2":
                self.train_creature()
            elif choice == "3":
                if not self.battle_system():
                    break
            elif choice == "4":
                self.player_creature.trauma = max(0, self.player_creature.trauma - 10)
                self.player_creature.happiness += 15
                self.player_creature.stats.mana = min(100, self.player_creature.stats.mana + 20)
                print("Tu criatura descansa y se recupera.")
            elif choice == "5":
                self.show_full_stats()
            elif choice == "6":
                self.check_relationships()
            elif choice == "7":
                self.advance_day()
            elif choice == "8":
                self.running = False
                print("Abandonas a tu criatura...")
                self.player_creature.trauma += 50
                self.player_creature.loyalty = 0
                break
            else:
                print("Opción inválida.")
            
            # Verificar condiciones de muerte
            if self.player_creature.stats.health <= 0:
                print(f"\n¡{self.player_creature.name} ha muerto!")
                self.player_creature.alive = False
                break
            
            if self.player_creature.trauma >= 100:
                print(f"\n¡{self.player_creature.name} ha sufrido un colapso mental total!")
                if random.random() < 0.7:
                    print("¡Se ha vuelto completamente salvaje!")
                    self.player_creature.loyalty = 0
                    self.player_creature.stats.corruption += 50
                    self.player_creature.alive = False
                    break
        
        if not self.player_creature.alive:
            self.creature_death()
    
    def show_full_stats(self):
        """Muestra estadísticas completas"""
        print(f"\n=== ESTADÍSTICAS DE {self.player_creature.name.upper()} ===")
        print(f"Tipo: {self.player_creature.type.value}")
        print(f"Nivel: {self.player_creature.level}")
        print(f"Experiencia: {self.player_creature.experience}")
        print(f"Facción: {self.player_creature.faction.value if self.player_creature.faction else 'Ninguna'}")
        
        print(f"\nEstadísticas de combate:")
        print(f"Salud: {self.player_creature.stats.health}/100")
        print(f"Maná: {self.player_creature.stats.mana}/100")
        print(f"Fuerza: {self.player_creature.stats.strength}")
        print(f"Agilidad: {self.player_creature.stats.agility}")
        print(f"Inteligencia: {self.player_creature.stats.intelligence}")
        print(f"Voluntad: {self.player_creature.stats.willpower}")
        
        print(f"\nEstado mental:")
        print(f"Hambre: {self.player_creature.hunger}/100")
        print(f"Felicidad: {self.player_creature.happiness}/100")
        print(f"Lealtad: {self.player_creature.loyalty}/100")
        print(f"Miedo: {self.player_creature.fear}/100")
        print(f"Trauma: {self.player_creature.trauma}/100")
        
        print(f"\nAlineamiento:")
        print(f"Corrupción: {self.player_creature.stats.corruption}/100")
        print(f"Favor divino: {self.player_creature.stats.divine_favor}/100")
        
        print(f"\nCombate:")
        print(f"Victorias: {self.player_creature.battle_wins}")
        print(f"Derrotas: {self.player_creature.battle_losses}")
        
        if self.player_creature.scars:
            print(f"\nCicatrices y marcas:")
            for scar in self.player_creature.scars:
                print(f"- {scar}")
        
        print(f"\nHabilidades:")
        for ability in self.player_creature.abilities:
            print(f"- {ability.name}: {ability.damage} daño, {ability.mana_cost} maná")
            print(f"  Efecto: {ability.special_effect}")
    
    def advance_day(self):
        """Avanza al siguiente día"""
        self.world.day += 1
        self.daily_care()
        
        # Eventos aleatorios
        if random.random() < 0.3:
            self.world_event()
        
        # Intervención divina ocasional
        if random.random() < 0.2:
            self.divine_intervention()
        
        # Recuperación natural mínima
        if self.player_creature.stats.health < 100:
            self.player_creature.stats.health = min(100, self.player_creature.stats.health + 5)
        
        if self.player_creature.stats.mana < 100:
            self.player_creature.stats.mana = min(100, self.player_creature.stats.mana + 10)
    
    def run(self):
        """Ejecuta el juego principal"""
        print("=" * 50)
        print("BIENVENIDO AL SIMULADOR DE CRIATURAS MÁGICAS")
        print("=" * 50)
        print("\nEn este mundo brutal, tu criatura mágica debe sobrevivir")
        print("a través de combates, decisiones morales y la corrupción")
        print("que infecta todo lo que toca...")
        print("\nTus decisiones tendrán consecuencias permanentes.")
        print("¿Mantendrás la pureza de tu criatura o la entregarás")
        print("a la oscuridad por poder?")
        
        input("\nPresiona Enter para comenzar...")
        
        self.create_creature()
        self.main_menu()
        
        print("\nGracias por jugar al Simulador de Criaturas Mágicas.")
        print("Las decisiones que tomaste echarán raíces en tu memoria...")

# Ejecutar el juego
if __name__ == "__main__":
    game = CreatureSimulator()
    game.run()
