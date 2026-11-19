from typing import Protocol

import pytest

from spore_sim.domain.creature import BaseCreature
from spore_sim.domain.enums import CreatureRole
from spore_sim.movement.handlers import MovementHandler, build_default_movement_chain
from spore_sim.movement.strategies import (
    GreedyMovementStrategy,
    StaminaMovementStrategy,
)


class CreatureBuilder(Protocol):
    def __call__(
        self,
        role: CreatureRole = CreatureRole.PREDATOR,
        position: int = 0,
        health: int = 100,
        stamina: int = 200,
        base_power: int = 10,
        legs: int = 0,
        wings: int = 0,
    ) -> BaseCreature: ...


@pytest.fixture
def make_creature() -> CreatureBuilder:
    def _builder(
        role: CreatureRole = CreatureRole.PREDATOR,
        position: int = 0,
        health: int = 100,
        stamina: int = 200,
        base_power: int = 10,
        legs: int = 0,
        wings: int = 0,
    ) -> BaseCreature:
        return BaseCreature(
            role=role,
            position=position,
            health=health,
            stamina=stamina,
            base_power=base_power,
            legs=legs,
            wings=wings,
        )

    return _builder


@pytest.fixture
def movement_chain() -> MovementHandler:
    return build_default_movement_chain()


@pytest.fixture
def greedy_strategy() -> GreedyMovementStrategy:
    return GreedyMovementStrategy()


@pytest.fixture
def saver_strategy() -> StaminaMovementStrategy:
    return StaminaMovementStrategy()
