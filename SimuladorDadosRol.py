import random
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DiceRoll:
    """Representa el resultado de una tirada de dados"""
    dice_type: str
    rolls: List[int]
    total: int
    modifier: int = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class DiceRoller:
    def __init__(self):
        self.history = []
        self.common_dice = {
            'd4': 4, 'd6': 6, 'd8': 8, 'd10': 10, 
            'd12': 12, 'd20': 20, 'd100': 100
        }
        self.stats = {'total_rolls': 0, 'crits': 0, 'fumbles': 0}
    
    def roll_dice(self, dice_expr: str) -> DiceRoll:
        """
        Tira dados basándose en expresiones como '2d6+3', '1d20', 'd8-1'
        """
        # Limpiar entrada
        dice_expr = dice_expr.lower().strip().replace(' ', '')
        
        # Patrones para diferentes tipos de tiradas
        patterns = [
            r'^(\d+)?d(\d+)([+-]\d+)?$',  # Ej: 2d6+3, d20, 1d8-1
            r'^(\d+)$'  # Número simple
        ]
        
        match = None
        for pattern in patterns:
            match = re.match(pattern, dice_expr)
            if match:
                break
        
        if not match:
            raise ValueError(f"Formato de dado inválido: {dice_expr}")
        
        # Si es solo un número
        if len(match.groups()) == 1:
            return DiceRoll('fixed', [int(match.group(1))], int(match.group(1)))
        
        # Parsear expresión de dados
        num_dice = int(match.group(1)) if match.group(1) else 1
        dice_sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        # Validaciones
        if num_dice < 1 or num_dice > 20:
            raise ValueError("Número de dados debe estar entre 1 y 20")
        if dice_sides < 2 or dice_sides > 1000:
            raise ValueError("Lados del dado debe estar entre 2 y 1000")
        
        # Tirar dados
        rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        
        # Actualizar estadísticas
        self.stats['total_rolls'] += len(rolls)
        if dice_sides == 20:
            self.stats['crits'] += rolls.count(20)
            self.stats['fumbles'] += rolls.count(1)
        
        # Crear resultado
        dice_type = f"{num_dice}d{dice_sides}"
        if modifier != 0:
            dice_type += f"{modifier:+d}"
        
        result = DiceRoll(dice_type, rolls, total, modifier)
        self.history.append(result)
        
        return result
    
    def roll_advantage(self) -> DiceRoll:
        """Tira 2d20 y toma el mayor (ventaja D&D)"""
        rolls = [random.randint(1, 20) for _ in range(2)]
        best = max(rolls)
        
        result = DiceRoll("2d20 (ventaja)", rolls, best)
        result.rolls = [best]  # Solo mostrar el mejor
        self.history.append(result)
        self.stats['total_rolls'] += 2
        
        return result
    
    def roll_disadvantage(self) -> DiceRoll:
        """Tira 2d20 y toma el menor (desventaja D&D)"""
        rolls = [random.randint(1, 20) for _ in range(2)]
        worst = min(rolls)
        
        result = DiceRoll("2d20 (desventaja)", rolls, worst)
        result.rolls = [worst]  # Solo mostrar el peor
        self.history.append(result)
        self.stats['total_rolls'] += 2
        
        return result
    
    def roll_multiple(self, dice_expr: str, times: int) -> List[DiceRoll]:
        """Tira la misma expresión múltiples veces"""
        if times < 1 or times > 50:
            raise ValueError("Número de tiradas debe estar entre 1 y 50")
        
        return [self.roll_dice(dice_expr) for _ in range(times)]
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de las tiradas"""
        if not self.history:
            return {"message": "No hay tiradas registradas"}
        
        totals = [roll.total for roll in self.history]
        return {
            "tiradas_totales": len(self.history),
            "dados_tirados": self.stats['total_rolls'],
            "promedio": round(sum(totals) / len(totals), 2),
            "mayor": max(totals),
            "menor": min(totals),
            "criticos_d20": self.stats['crits'],
            "pifia_d20": self.stats['fumbles']
        }
    
    def clear_history(self):
        """Limpia el historial y estadísticas"""
        self.history.clear()
        self.stats = {'total_rolls': 0, 'crits': 0, 'fumbles': 0}

def format_result(result: DiceRoll) -> str:
    """Formatea el resultado para mostrar"""
    if len(result.rolls) == 1:
        base = f"🎲 {result.dice_type}: {result.rolls[0]}"
    else:
        rolls_str = ', '.join(map(str, result.rolls))
        base = f"🎲 {result.dice_type}: [{rolls_str}]"
    
    if result.modifier != 0:
        base += f" = {result.total}"
    
    # Destacar resultados especiales
    if result.dice_type.endswith('d20') and len(result.rolls) == 1:
        if result.rolls[0] == 20:
            base += " ⭐ ¡CRÍTICO!"
        elif result.rolls[0] == 1:
            base += " 💥 ¡PIFIA!"
    
    return base

def main():
    roller = DiceRoller()
    
    print("=== SIMULADOR DE DADOS DE ROL ===")
    print("Ejemplos: d20, 2d6+3, 3d8-1, 1d100")
    print("Comandos: ventaja, desventaja, stats, historial, limpiar, salir")
    print("-" * 40)
    
    while True:
        try:
            entrada = input("\n🎯 Ingresa el dado a tirar: ").strip()
            
            if not entrada or entrada.lower() == 'salir':
                break
            
            entrada_lower = entrada.lower()
            
            if entrada_lower in ['ventaja', 'adv']:
                result = roller.roll_advantage()
                print(f"✨ Ventaja: {format_result(result)}")
                
            elif entrada_lower in ['desventaja', 'dis']:
                result = roller.roll_disadvantage()
                print(f"🔻 Desventaja: {format_result(result)}")
                
            elif entrada_lower in ['stats', 'estadisticas']:
                stats = roller.get_stats()
                print("\n📊 ESTADÍSTICAS:")
                for key, value in stats.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
                    
            elif entrada_lower in ['historial', 'history']:
                if not roller.history:
                    print("📝 No hay tiradas en el historial")
                else:
                    print("\n📝 HISTORIAL (últimas 10):")
                    for roll in roller.history[-10:]:
                        time_str = roll.timestamp.strftime("%H:%M:%S")
                        print(f"  [{time_str}] {format_result(roll)}")
                        
            elif entrada_lower in ['limpiar', 'clear']:
                roller.clear_history()
                print("🧹 Historial limpiado")
                
            elif 'x' in entrada_lower:  # Múltiples tiradas: 3x1d6
                parts = entrada_lower.split('x')
                if len(parts) == 2:
                    times = int(parts[0])
                    dice_expr = parts[1]
                    results = roller.roll_multiple(dice_expr, times)
                    print(f"\n🎲 Tirando {times} veces {dice_expr}:")
                    for i, result in enumerate(results, 1):
                        print(f"  {i}. {format_result(result)}")
                    total = sum(r.total for r in results)
                    print(f"💰 Total combinado: {total}")
                else:
                    raise ValueError("Formato incorrecto. Usa: 3x1d6")
            else:
                result = roller.roll_dice(entrada)
                print(format_result(result))
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
