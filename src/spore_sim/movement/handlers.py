from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from spore_sim.domain.creature import CreatureProtocol
from spore_sim.domain.enums import MovementType


@dataclass(frozen=True, slots=True)
class MovementOption:
    movement_type: MovementType
    speed: int
    stamina_cost: int


class MovementHandler(ABC):
    def __init__(self, option: MovementOption) -> None:
        self._option = option
        self._next_handler: MovementHandler | None = None

    def set_next(self, handler: MovementHandler) -> MovementHandler:
        self._next_handler = handler
        return handler

    def collect_options(self, creature: CreatureProtocol) -> list[MovementOption]:
        options: list[MovementOption] = []
        if self._can_perform(creature):
            options.append(self._option)
        if self._next_handler is not None:
            options.extend(self._next_handler.collect_options(creature))
        return options

    @abstractmethod
    def _can_perform(self, creature: CreatureProtocol) -> bool:
        """Check if it has stamina for this"""


class FlyHandler(MovementHandler):
    def __init__(self) -> None:
        super().__init__(
            MovementOption(
                movement_type=MovementType.FLYING,
                speed=8,
                stamina_cost=4,
            )
        )

    def _can_perform(self, creature: CreatureProtocol) -> bool:
        return creature.wings >= 2 and creature.stamina >= 80


class WalkHandler(MovementHandler):
    def __init__(self) -> None:
        super().__init__(
            MovementOption(
                movement_type=MovementType.WALKING,
                speed=4,
                stamina_cost=2,
            )
        )

    def _can_perform(self, creature: CreatureProtocol) -> bool:
        return creature.legs >= 2 and creature.stamina >= 40


class RunHandler(MovementHandler):
    def __init__(self) -> None:
        super().__init__(
            MovementOption(
                movement_type=MovementType.RUNNING,
                speed=6,
                stamina_cost=4,
            )
        )

    def _can_perform(self, creature: CreatureProtocol) -> bool:
        return creature.legs >= 2 and creature.stamina >= 60


class HopHandler(MovementHandler):
    def __init__(self) -> None:
        super().__init__(
            MovementOption(
                movement_type=MovementType.HOPPING,
                speed=3,
                stamina_cost=2,
            )
        )

    def _can_perform(self, creature: CreatureProtocol) -> bool:
        return creature.legs >= 1 and creature.stamina >= 20


class CrawlHandler(MovementHandler):
    def __init__(self) -> None:
        super().__init__(
            MovementOption(
                movement_type=MovementType.CRAWLING,
                speed=1,
                stamina_cost=1,
            )
        )

    def _can_perform(self, creature: CreatureProtocol) -> bool:
        return creature.stamina >= 1


def build_default_movement_chain() -> MovementHandler:
    fly = FlyHandler()
    run = RunHandler()
    walk = WalkHandler()
    hop = HopHandler()
    crawl = CrawlHandler()

    fly.set_next(run).set_next(walk).set_next(hop).set_next(crawl)
    return fly
