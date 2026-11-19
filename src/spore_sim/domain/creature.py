from __future__ import annotations

from typing import Protocol

from spore_sim.domain.enums import CreatureRole


class CreatureProtocol(Protocol):
    @property
    def role(self) -> CreatureRole: ...

    @property
    def position(self) -> int: ...

    @property
    def health(self) -> int: ...

    @property
    def stamina(self) -> int: ...

    @property
    def legs(self) -> int: ...

    @property
    def wings(self) -> int: ...

    @property
    def attack_power(self) -> int: ...

    @property
    def traits(self) -> tuple[str, ...]: ...

    @property
    def is_alive(self) -> bool: ...

    def move_by(self, distance: int, stamina_cost: int) -> None: ...

    def take_damage(self, amount: int) -> None: ...

    def attack(self, target: CreatureProtocol) -> int: ...


class BaseCreature:
    def __init__(
        self,
        role: CreatureRole,
        position: int,
        health: int,
        stamina: int,
        base_power: int,
        legs: int = 0,
        wings: int = 0,
    ) -> None:
        self._role = role
        self._position = position
        self._health = health
        self._stamina = stamina
        self._base_power = base_power
        self._legs = legs
        self._wings = wings

    @property
    def role(self) -> CreatureRole:
        return self._role

    @property
    def position(self) -> int:
        return self._position

    @property
    def health(self) -> int:
        return self._health

    @property
    def stamina(self) -> int:
        return self._stamina

    @property
    def legs(self) -> int:
        return self._legs

    @property
    def wings(self) -> int:
        return self._wings

    @property
    def attack_power(self) -> int:
        return self._base_power

    @property
    def traits(self) -> tuple[str, ...]:
        return ()

    @property
    def is_alive(self) -> bool:
        return self._health > 0

    def move_by(self, distance: int, stamina_cost: int) -> None:
        self._position += distance
        self._stamina = max(0, self._stamina - stamina_cost)

    def take_damage(self, amount: int) -> None:
        self._health = max(0, self._health - amount)

    def attack(self, target: CreatureProtocol) -> int:
        damage = self.attack_power
        target.take_damage(damage)
        return damage
