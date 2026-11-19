from collections.abc import Sequence
from typing import Protocol

from spore_sim.movement.handlers import MovementOption


class MovementStrategy(Protocol):
    def choose_movement(
        self,
        options: Sequence[MovementOption],
    ) -> MovementOption | None: ...


class GreedyMovementStrategy:
    def choose_movement(
        self,
        options: Sequence[MovementOption],
    ) -> MovementOption | None:
        if not options:
            return None
        return max(options, key=lambda option: option.speed)


class StaminaMovementStrategy:
    def choose_movement(
        self,
        options: Sequence[MovementOption],
    ) -> MovementOption | None:
        if not options:
            return None
        return max(
            options,
            key=lambda option: (
                option.speed / option.stamina_cost,
                -option.stamina_cost,
            ),
        )
