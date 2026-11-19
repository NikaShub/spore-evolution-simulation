import pytest

from spore_sim.domain.decorators import ClawsDecorator, TeethDecorator
from spore_sim.domain.enums import ClawSize, CreatureRole, TeethSharpness
from tests.conftest import CreatureBuilder

def test_base_creature_initial_state(make_creature: CreatureBuilder) -> None:
    creature = make_creature(
        role=CreatureRole.PREY,
        position=42,
        health=95,
        stamina=250,
        base_power=7,
        legs=2,
        wings=1,
    )
    assert creature.role is CreatureRole.PREY
    assert creature.position == 42
    assert creature.health == 95
    assert creature.stamina == 250
    assert creature.attack_power == 7
    assert creature.legs == 2
    assert creature.wings == 1
    assert creature.traits == ()
    assert creature.is_alive is True

def test_move_by_updates_position__stamina_at_zero(
    make_creature: CreatureBuilder,
) -> None:
    creature = make_creature(position=10, stamina=5)

    creature.move_by(distance=6, stamina_cost=4)
    assert creature.position == 16
    assert creature.stamina == 1

    creature.move_by(distance=6, stamina_cost=4)
    assert creature.position == 22
    assert creature.stamina == 0


def test_take_damage_reduce_health_updates_is_alive(
    make_creature: CreatureBuilder,
) -> None:
    creature = make_creature(health=30)

    creature.take_damage(29)
    assert creature.health == 1
    assert creature.is_alive is True

    creature.take_damage(50)
    assert creature.health == 0
    assert creature.is_alive is False


def test_base_attack_exact_damage(make_creature: CreatureBuilder) -> None:
    attacker = make_creature(role=CreatureRole.PREDATOR, base_power=14)
    target = make_creature(role=CreatureRole.PREY, health=50)

    dealt = attacker.attack(target)
    assert dealt == 14
    assert target.health == 36


@pytest.mark.parametrize("bonus", [3, 6, 9])
def test_teeth_decorator_bonus(
    make_creature: CreatureBuilder,
    bonus: int,
) -> None:
    base = make_creature(base_power=10, position=15, health=80, stamina=120, legs=4)
    decorated = TeethDecorator(base, TeethSharpness(bonus))

    assert decorated.attack_power == 10 + bonus
    assert decorated.traits == (f"Teeth(+{bonus})",)
    assert decorated.position == 15
    assert decorated.health == 80
    assert decorated.stamina == 120
    assert decorated.legs == 4


@pytest.mark.parametrize("multiplier", [2, 3, 4])
def test_claws_decorator_multiplies_power(
    make_creature: CreatureBuilder,
    multiplier: int,
) -> None:
    base = make_creature(base_power=10)
    decorated = ClawsDecorator(base, ClawSize(multiplier))

    assert decorated.attack_power == 10 * multiplier
    assert decorated.traits == (f"Claws(x{multiplier})",)


def test_decorator_stacking_order_changes_final_power(
    make_creature: CreatureBuilder,
) -> None:
    base = make_creature(base_power=5)
    teeth = TeethSharpness(6)
    claws = ClawSize(3)

    # (5 + 6) * 3 = 33
    teeth_then_claws = ClawsDecorator(TeethDecorator(base, teeth), claws)
    assert teeth_then_claws.attack_power == 33
    assert teeth_then_claws.traits == ("Teeth(+6)", "Claws(x3)")

    # (5 * 3) + 6 = 21
    claws_then_teeth = TeethDecorator(ClawsDecorator(base, claws), teeth)
    assert claws_then_teeth.attack_power == 21
    assert claws_then_teeth.traits == ("Claws(x3)", "Teeth(+6)")


def test_decorated_attack_uses_power_and_mutations(
    make_creature: CreatureBuilder,
) -> None:
    predator = ClawsDecorator(
        TeethDecorator(make_creature(base_power=5, stamina=20), TeethSharpness(6)),
        ClawSize(3),
    )
    prey = make_creature(role=CreatureRole.PREY, health=100)

    dealt = predator.attack(prey)
    assert dealt == 33
    assert prey.health == 67

    predator.move_by(distance=8, stamina_cost=4)
    assert predator.position == 8
    assert predator.stamina == 16