from dataclasses import dataclass

from spore_sim.domain.enums import AttackModifierOrder


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    simulations_count: int = 100
    predator_start_pos: int = 0
    prey_start_pos_range: tuple[int, int] = (0, 1000)

    health_range: tuple[int, int] = (80, 120)
    stamina_range: tuple[int, int] = (200, 400)
    base_power_range: tuple[int, int] = (3, 8)

    max_legs: int = 4
    max_wings: int = 2
    teeth_evolution_chance: float = 0.7
    claws_evolution_chance: float = 0.7

    modifier_order: AttackModifierOrder = AttackModifierOrder.TEETH_THEN_CLAWS
