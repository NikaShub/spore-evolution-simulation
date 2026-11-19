import random
from typing import Protocol

from spore_sim.config import SimulationConfig
from spore_sim.domain.creature import BaseCreature, CreatureProtocol
from spore_sim.domain.decorators import ClawsDecorator, TeethDecorator
from spore_sim.domain.enums import (
    AttackModifierOrder,
    ClawSize,
    CreatureRole,
    TeethSharpness,
)

class EvolutionFactory(Protocol):
    def create_participants(self) -> tuple[CreatureProtocol, CreatureProtocol]: ...

class RandomEvolutionFactory:
    def __init__(
            self,
            config: SimulationConfig,
            rng: random.Random | None = None,
    ) -> None:
        self._config = config
        self._rng = rng if rng is not None else random.Random()

    def create_participants(self) -> tuple[CreatureProtocol, CreatureProtocol]:
        predator = self._evolve_creature(
            role=CreatureRole.PREDATOR,
            position=self._config.predator_start_pos,
        )
        prey_position = self._rng.randint(*self._config.prey_start_pos_range)
        prey = self._evolve_creature(
            role=CreatureRole.PREY,
            position=prey_position,
        )
        return predator, prey



    def _evolve_creature(self,
        role: CreatureRole,
        position: int,
    ) -> CreatureProtocol:
        base = BaseCreature(
            role=role,
            position=position,
            health=self._rng.randint(*self._config.health_range),
            stamina=self._rng.randint(*self._config.stamina_range),
            base_power=self._rng.randint(*self._config.base_power_range),
            legs=self._rng.randint(0, self._config.max_legs),
            wings=self._rng.randint(0, self._config.max_wings),
        )
        return self._apply_evolution_traits(base)

    def _apply_evolution_traits(self,
        creature: CreatureProtocol,
    ) -> CreatureProtocol:
        teeth = self._roll_teeth()
        claws = self._roll_claws()

        if self._config.modifier_order is AttackModifierOrder.TEETH_THEN_CLAWS:
            decorated = self._wrap_teeth(creature, teeth)
            return self._wrap_claws(decorated, claws)

        decorated = self._wrap_claws(creature, claws)
        return self._wrap_teeth(decorated, teeth)

    def _roll_teeth(self):
        if self._rng.random() >= self._config.teeth_evolution_chance:
            return None
        return self._rng.choice(list(TeethSharpness))

    def _roll_claws(self) -> ClawSize | None:
        if self._rng.random() >= self._config.claws_evolution_chance:
            return None
        return self._rng.choice(list(ClawSize))


    @staticmethod
    def _wrap_teeth(
            creature: CreatureProtocol,
            sharpness: TeethSharpness | None,
    ) -> CreatureProtocol:
        if sharpness is None:
            return creature
        return TeethDecorator(creature, sharpness)


    @staticmethod
    def _wrap_claws(
            creature: CreatureProtocol,
            size: ClawSize | None,
    ) -> CreatureProtocol:
        if size is None:
            return creature
        return ClawsDecorator(creature, size)




class PresetEvolutionFactory:
    """THis is for unit testing purpose"""

    def __init__(
        self,
        predator: CreatureProtocol,
        prey: CreatureProtocol,
    ) -> None:
        self._predator = predator
        self._prey = prey

    def create_participants(self) -> tuple[CreatureProtocol, CreatureProtocol]:
        return self._predator, self._prey

