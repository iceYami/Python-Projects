import random
import time
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class CombatStyle(Enum):
    AGGRESSIVE = "agresivo"
    DEFENSIVE = "defensivo"
    BALANCED = "equilibrado"
    BERSERKER = "berserker"

class SpecialAbility(Enum):
    CRITICAL_HIT = "golpe_critico"
    HEAL = "curacion"
    DODGE = "esquivar"
    COUNTER_ATTACK = "contraataque"
    RAGE = "furia"
    SHIELD = "escudo"

@dataclass
class CombatStats:
    total_damage_dealt: int = 0
    total_damage_received: int = 0
    critical_hits: int = 0
    dodges: int = 0
    special_abilities_used: int = 0
    turns_survived: int = 0

class Fighter:
    def __init__(self, name: str, health: int, damage_per_attack: int, 
                 combat_style: CombatStyle = CombatStyle.BALANCED,
                 special_abilities: Optional[List[SpecialAbility]] = None):
        self.name = name
        self.max_health = health
        self.health = health
        self.base_damage = damage_per_attack
        self.damage_per_attack = damage_per_attack
        self.combat_style = combat_style
        self.special_abilities = special_abilities or []
        self.stats = CombatStats()
        
        # Atributos avanzados
        self.defense = 0
        self.accuracy = 85  # Precisión base del 85%
        self.critical_chance = 10  # 10% de probabilidad de crítico
        self.dodge_chance = 5  # 5% de probabilidad de esquivar
        self.stamina = 100
        self.max_stamina = 100
        self.experience = 0
        self.level = 1
        self.status_effects = {}  # Para efectos como veneno, regeneración, etc.
        
        # Aplicar modificadores según el estilo de combate
        self._apply_combat_style_modifiers()
    
    def _apply_combat_style_modifiers(self):
        """Aplica modificadores según el estilo de combate"""
        if self.combat_style == CombatStyle.AGGRESSIVE:
            self.damage_per_attack = int(self.base_damage * 1.2)
            self.critical_chance += 5
            self.defense -= 2
        elif self.combat_style == CombatStyle.DEFENSIVE:
            self.defense += 3
            self.dodge_chance += 10
            self.damage_per_attack = int(self.base_damage * 0.9)
        elif self.combat_style == CombatStyle.BERSERKER:
            self.critical_chance += 15
            self.accuracy -= 10
            self.dodge_chance -= 5
        # BALANCED no tiene modificadores
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def calculate_damage(self, base_damage: int) -> int:
        """Calcula el daño final considerando críticos y variaciones"""
        damage = base_damage
        
        # Variación aleatoria del daño (±15%)
        variation = random.uniform(0.85, 1.15)
        damage = int(damage * variation)
        
        # Crítico
        if random.randint(1, 100) <= self.critical_chance:
            damage = int(damage * 1.5)
            self.stats.critical_hits += 1
            return damage, True
        
        return damage, False
    
    def attack(self, target: 'Fighter') -> Dict:
        """Realiza un ataque contra el objetivo"""
        self.stamina = max(0, self.stamina - 10)
        
        # Verificar si el ataque acierta
        hit_chance = self.accuracy
        if self.stamina < 20:  # Penalización por cansancio
            hit_chance -= 15
        
        if random.randint(1, 100) > hit_chance:
            return {
                'hit': False,
                'damage': 0,
                'critical': False,
                'dodged': False,
                'message': f"{self.name} falla su ataque!"
            }
        
        # Verificar si el objetivo esquiva
        if random.randint(1, 100) <= target.dodge_chance:
            target.stats.dodges += 1
            return {
                'hit': False,
                'damage': 0,
                'critical': False,
                'dodged': True,
                'message': f"{target.name} esquiva el ataque de {self.name}!"
            }
        
        # Calcular daño
        damage, is_critical = self.calculate_damage(self.damage_per_attack)
        
        # Aplicar defensa del objetivo
        final_damage = max(1, damage - target.defense)
        
        # Aplicar daño
        target.receive_damage(final_damage)
        self.stats.total_damage_dealt += final_damage
        
        message = f"{self.name} ataca a {target.name} causando {final_damage} de daño"
        if is_critical:
            message += " ¡CRÍTICO!"
        
        return {
            'hit': True,
            'damage': final_damage,
            'critical': is_critical,
            'dodged': False,
            'message': message
        }
    
    def receive_damage(self, damage: int):
        """Recibe daño y actualiza estadísticas"""
        self.health = max(0, self.health - damage)
        self.stats.total_damage_received += damage
    
    def use_special_ability(self, ability: SpecialAbility, target: Optional['Fighter'] = None) -> Dict:
        """Usa una habilidad especial"""
        if ability not in self.special_abilities or self.stamina < 20:
            return {'success': False, 'message': "No se puede usar la habilidad especial"}
        
        self.stamina -= 20
        self.stats.special_abilities_used += 1
        
        if ability == SpecialAbility.HEAL:
            heal_amount = int(self.max_health * 0.2)
            self.health = min(self.max_health, self.health + heal_amount)
            return {'success': True, 'message': f"{self.name} se cura {heal_amount} puntos de vida!"}
        
        elif ability == SpecialAbility.RAGE:
            self.damage_per_attack = int(self.base_damage * 1.5)
            self.status_effects['rage'] = 3  # Dura 3 turnos
            return {'success': True, 'message': f"{self.name} entra en FURIA! Su daño aumenta!"}
        
        elif ability == SpecialAbility.SHIELD:
            self.defense += 5
            self.status_effects['shield'] = 3
            return {'success': True, 'message': f"{self.name} se protege con un escudo mágico!"}
        
        return {'success': False, 'message': "Habilidad no implementada"}
    
    def rest(self):
        """Recupera stamina"""
        self.stamina = min(self.max_stamina, self.stamina + 25)
    
    def process_status_effects(self):
        """Procesa efectos de estado como veneno, regeneración, etc."""
        effects_to_remove = []
        
        for effect, duration in self.status_effects.items():
            if effect == 'rage' and duration <= 0:
                self.damage_per_attack = self.base_damage
                effects_to_remove.append(effect)
            elif effect == 'shield' and duration <= 0:
                self.defense -= 5
                effects_to_remove.append(effect)
            
            self.status_effects[effect] = duration - 1
        
        for effect in effects_to_remove:
            del self.status_effects[effect]
    
    def get_health_percentage(self) -> float:
        return (self.health / self.max_health) * 100
    
    def get_status_description(self) -> str:
        """Devuelve una descripción del estado actual del luchador"""
        health_pct = self.get_health_percentage()
        
        if health_pct > 80:
            condition = "excelente estado"
        elif health_pct > 60:
            condition = "buen estado"
        elif health_pct > 40:
            condition = "herido"
        elif health_pct > 20:
            condition = "gravemente herido"
        else:
            condition = "al borde de la muerte"
        
        stamina_status = "energético" if self.stamina > 70 else "cansado" if self.stamina > 30 else "exhausto"
        
        return f"{self.name} ({self.health}/{self.max_health} HP) - {condition}, {stamina_status}"

class CombatSimulator:
    def __init__(self, verbose: bool = True, delay: float = 0.5):
        self.verbose = verbose
        self.delay = delay
        self.combat_log = []
    
    def log(self, message: str, important: bool = False):
        """Registra un mensaje en el log de combate"""
        self.combat_log.append(message)
        if self.verbose:
            if important:
                print(f"\n>>> {message} <<<")
            else:
                print(f"    {message}")
            if self.delay > 0:
                time.sleep(self.delay)
    
    def display_fighter_status(self, fighter: Fighter):
        """Muestra el estado detallado de un luchador"""
        status = fighter.get_status_description()
        self.log(f"📊 {status}")
        
        if fighter.status_effects:
            effects = ", ".join([f"{effect}({duration})" for effect, duration in fighter.status_effects.items()])
            self.log(f"   Efectos activos: {effects}")
    
    def simulate_turn(self, attacker: Fighter, defender: Fighter) -> bool:
        """Simula un turno de combate"""
        self.log(f"\n--- Turno de {attacker.name} ---")
        
        # Procesar efectos de estado
        attacker.process_status_effects()
        defender.process_status_effects()
        
        # Decidir acción (ataque normal o habilidad especial)
        action_choice = random.randint(1, 100)
        
        if action_choice <= 15 and attacker.special_abilities and attacker.stamina >= 20:
            # Usar habilidad especial
            ability = random.choice(attacker.special_abilities)
            result = attacker.use_special_ability(ability, defender)
            self.log(f"✨ {result['message']}")
        else:
            # Ataque normal
            result = attacker.attack(defender)
            if result['hit']:
                self.log(f"⚔️  {result['message']}")
                if result['critical']:
                    self.log("💥 ¡GOLPE CRÍTICO!")
            else:
                self.log(f"❌ {result['message']}")
        
        # Regenerar stamina
        attacker.rest()
        attacker.stats.turns_survived += 1
        
        return defender.is_alive()
    
    def declare_winner(self, fighter1: Fighter, fighter2: Fighter, first_attacker: str) -> str:
        """Función principal que simula el combate completo"""
        self.log("🥊 ¡COMIENZA EL COMBATE!", important=True)
        self.log(f"Luchador 1: {fighter1.name} ({fighter1.combat_style.value})")
        self.log(f"Luchador 2: {fighter2.name} ({fighter2.combat_style.value})")
        self.log(f"Primer atacante: {first_attacker}\n")
        
        # Determinar quién ataca primero
        if fighter1.name == first_attacker:
            current_attacker, current_defender = fighter1, fighter2
        else:
            current_attacker, current_defender = fighter2, fighter1
        
        round_number = 1
        
        while current_attacker.is_alive() and current_defender.is_alive():
            self.log(f"\n🔥 ROUND {round_number} 🔥", important=True)
            
            # Mostrar estado de ambos luchadores
            self.display_fighter_status(current_attacker)
            self.display_fighter_status(current_defender)
            
            # Simular el turno
            defender_survives = self.simulate_turn(current_attacker, current_defender)
            
            if not defender_survives:
                break
            
            # Cambiar roles para el siguiente turno
            current_attacker, current_defender = current_defender, current_attacker
            round_number += 1
        
        # Determinar ganador
        winner = current_attacker if current_attacker.is_alive() else current_defender
        loser = current_defender if current_attacker.is_alive() else current_attacker
        
        self.log(f"\n🏆 ¡{winner.name} GANA EL COMBATE! 🏆", important=True)
        self.log(f"💀 {loser.name} ha sido derrotado")
        
        # Mostrar estadísticas finales
        self.show_final_stats(winner, loser, round_number)
        
        return winner.name
    
    def show_final_stats(self, winner: Fighter, loser: Fighter, rounds: int):
        """Muestra las estadísticas finales del combate"""
        self.log("\n📈 ESTADÍSTICAS FINALES:", important=True)
        self.log(f"Duración del combate: {rounds} rounds")
        
        for fighter in [winner, loser]:
            self.log(f"\n{fighter.name}:")
            self.log(f"  💪 Daño total infligido: {fighter.stats.total_damage_dealt}")
            self.log(f"  🛡️  Daño total recibido: {fighter.stats.total_damage_received}")
            self.log(f"  💥 Golpes críticos: {fighter.stats.critical_hits}")
            self.log(f"  🌪️  Esquivas exitosas: {fighter.stats.dodges}")
            self.log(f"  ✨ Habilidades especiales usadas: {fighter.stats.special_abilities_used}")
            self.log(f"  ⏱️  Turnos sobrevividos: {fighter.stats.turns_survived}")

# Función de conveniencia para crear luchadores predefinidos
def create_warrior(name: str) -> Fighter:
    """Crea un guerrero equilibrado"""
    return Fighter(
        name=name,
        health=120,
        damage_per_attack=18,
        combat_style=CombatStyle.BALANCED,
        special_abilities=[SpecialAbility.SHIELD, SpecialAbility.COUNTER_ATTACK]
    )

def create_berserker(name: str) -> Fighter:
    """Crea un berserker agresivo"""
    return Fighter(
        name=name,
        health=100,
        damage_per_attack=25,
        combat_style=CombatStyle.BERSERKER,
        special_abilities=[SpecialAbility.RAGE, SpecialAbility.CRITICAL_HIT]
    )

def create_paladin(name: str) -> Fighter:
    """Crea un paladín defensivo con curación"""
    return Fighter(
        name=name,
        health=140,
        damage_per_attack=15,
        combat_style=CombatStyle.DEFENSIVE,
        special_abilities=[SpecialAbility.HEAL, SpecialAbility.SHIELD]
    )

def create_assassin(name: str) -> Fighter:
    """Crea un asesino ágil"""
    return Fighter(
        name=name,
        health=80,
        damage_per_attack=22,
        combat_style=CombatStyle.AGGRESSIVE,
        special_abilities=[SpecialAbility.CRITICAL_HIT, SpecialAbility.DODGE]
    )

# Ejemplo
if __name__ == "__main__":
    # Crear luchadores con diferentes estilos
    thor = create_warrior("Thor el Martillo")
    ragnar = create_berserker("Ragnar el Salvaje")
    
    # Crear el simulador
    simulator = CombatSimulator(verbose=True, delay=0.8)
    
    # Ejecutar el combate
    winner = simulator.declare_winner(thor, ragnar, "Thor el Martillo")
    
    print(f"\n🎯 El ganador final es: {winner}")
    
    # Ejemplo con luchadores personalizados
    print("\n" + "="*50)
    print("COMBATE PERSONALIZADO")
    print("="*50)
    
    # Luchador personalizado
    custom_fighter = Fighter(
        name="Arthas el Caído",
        health=150,
        damage_per_attack=20,
        combat_style=CombatStyle.AGGRESSIVE,
        special_abilities=[SpecialAbility.HEAL, SpecialAbility.RAGE, SpecialAbility.CRITICAL_HIT]
    )
    
    elena = create_paladin("Elena la Luz")
    
    simulator2 = CombatSimulator(verbose=True, delay=0.3)
    winner2 = simulator2.declare_winner(custom_fighter, elena, "Elena la Luz")
