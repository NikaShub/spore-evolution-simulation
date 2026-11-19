from spore_sim.domain.creature import CreatureProtocol
from spore_sim.domain.enums import ClawSize, CreatureRole, TeethSharpness


class CreatureDecorator:
    def __init__(self, _wrapped: CreatureProtocol) -> None:
        self._wrapped = _wrapped

    @property
    def role(self) -> CreatureRole:
        return self._wrapped.role

    @property
    def position(self) -> int:
        return self._wrapped.position

    @property
    def health(self) -> int:
        return self._wrapped.health

    @property
    def stamina(self) -> int:
        return self._wrapped.stamina

    @property
    def legs(self) -> int:
        return self._wrapped.legs

    @property
    def wings(self) -> int:
        return self._wrapped.wings

    @property
    def attack_power(self) -> int:
        return self._wrapped.attack_power

    @property
    def traits(self) -> tuple[str, ...]:
        return self._wrapped.traits

    @property
    def is_alive(self) -> bool:
        return self._wrapped.is_alive

    def move_by(self, distance: int, stamina_cost: int) -> None:
        self._wrapped.move_by(distance, stamina_cost)

    def take_damage(self, amount: int) -> None:
        self._wrapped.take_damage(amount)

    def attack(self, target: CreatureProtocol) -> int:
        damage = self.attack_power
        target.take_damage(damage)
        return damage


class TeethDecorator(CreatureDecorator):
    def __init__(self, wrapped: CreatureProtocol, sharpness: TeethSharpness):
        super().__init__(wrapped)
        self._sharpness = sharpness

    @property
    def traits(self) -> tuple[str, ...]:
        return *self._wrapped.traits, f"Teeth(+{self._sharpness.value})"

    @property
    def attack_power(self) -> int:
        return self._wrapped.attack_power + self._sharpness.value

class ClawsDecorator(CreatureDecorator):
        def __init__(self, wrapped: CreatureProtocol, size: ClawSize) -> None:
            super().__init__(wrapped)
            self._size = size

        @property
        def attack_power(self) -> int:
            return self._wrapped.attack_power * self._size.value

        @property
        def traits(self) -> tuple[str, ...]:
            return (*self._wrapped.traits, f"Claws(x{self._size.value})")
