import random

from spore_sim.config import SimulationConfig
from spore_sim.domain.decorators import ClawsDecorator, TeethDecorator
from spore_sim.domain.enums import (
    AttackModifierOrder,
    ClawSize,
    CreatureRole,
    OutcomeMessage,
    TeethSharpness,
)
from spore_sim.evolution.factories import (
    PresetEvolutionFactory,
    RandomEvolutionFactory,
)
from spore_sim.reporting.adapters import (
    ConsoleReporterAdapter,
    MemoryReporterAdapter,
)
from tests.conftest import CreatureBuilder


def test_preset_factory(
    make_creature: CreatureBuilder,
) -> None:
    pred = make_creature(role=CreatureRole.PREDATOR, position=0)
    prey = make_creature(role=CreatureRole.PREY, position=150)

    factory = PresetEvolutionFactory(pred, prey)
    out_pred, out_prey = factory.create_participants()

    assert out_pred is pred
    assert out_prey is prey


def test_random_factory() -> None:
    config = SimulationConfig(
        predator_start_pos=0,
        prey_start_pos_range=(50, 120),
        health_range=(90, 110),
        stamina_range=(200, 300),
        base_power_range=(5, 10),
        max_legs=4,
        max_wings=2,
        teeth_evolution_chance=0.0,
        claws_evolution_chance=0.0,
    )
    factory = RandomEvolutionFactory(config, rng=random.Random(123))

    for _ in range(25):
        predator, prey = factory.create_participants()

        assert predator.role is CreatureRole.PREDATOR
        assert predator.position == 0
        assert 90 <= predator.health <= 110
        assert 200 <= predator.stamina <= 300
        assert 5 <= predator.attack_power <= 10
        assert 0 <= predator.legs <= 4
        assert 0 <= predator.wings <= 2
        assert predator.traits == ()

        assert prey.role is CreatureRole.PREY
        assert 50 <= prey.position <= 120
        assert 90 <= prey.health <= 110
        assert 200 <= prey.stamina <= 300
        assert 5 <= prey.attack_power <= 10
        assert 0 <= prey.legs <= 4
        assert 0 <= prey.wings <= 2
        assert prey.traits == ()


def test_random_factory_applies_modifier_order() -> None:
    config_teeth_first = SimulationConfig(
        teeth_evolution_chance=1.0,
        claws_evolution_chance=1.0,
        modifier_order=AttackModifierOrder.TEETH_THEN_CLAWS,
    )
    pred_a, _ = RandomEvolutionFactory(
        config_teeth_first,
        rng=random.Random(7),
    ).create_participants()
    assert len(pred_a.traits) == 2
    assert pred_a.traits[0].startswith("Teeth(")
    assert pred_a.traits[1].startswith("Claws(")

    config_claws_first = SimulationConfig(
        teeth_evolution_chance=1.0,
        claws_evolution_chance=1.0,
        modifier_order=AttackModifierOrder.CLAWS_THEN_TEETH,
    )
    pred_b, _ = RandomEvolutionFactory(
        config_claws_first,
        rng=random.Random(7),
    ).create_participants()
    assert len(pred_b.traits) == 2
    assert pred_b.traits[0].startswith("Claws(")
    assert pred_b.traits[1].startswith("Teeth(")


def test_memory_reporter(make_creature: CreatureBuilder) -> None:
    reporter = MemoryReporterAdapter()
    pred = make_creature(role=CreatureRole.PREDATOR)
    prey = make_creature(role=CreatureRole.PREY, position=200)

    reporter.report_simulation_start(1)
    reporter.report_creature_evolved(pred)
    reporter.report_creature_evolved(prey)
    reporter.report_outcome(OutcomeMessage.PREY_ESCAPED)

    assert reporter.started_simulations == [1]
    assert reporter.evolved_creatures == [pred, prey]
    assert reporter.outcomes == [OutcomeMessage.PREY_ESCAPED]


def test_console_reporter(
    make_creature: CreatureBuilder,
) -> None:
    lines: list[str] = []
    reporter = ConsoleReporterAdapter(output_fn=lines.append)

    bare_prey = make_creature(
        role=CreatureRole.PREY,
        position=300,
        health=90,
        stamina=210,
        base_power=4,
        legs=2,
        wings=0,
    )
    decorated_pred = ClawsDecorator(
        TeethDecorator(
            make_creature(
                role=CreatureRole.PREDATOR,
                position=0,
                health=100,
                stamina=250,
                base_power=5,
                legs=2,
                wings=2,
            ),
            TeethSharpness(6),
        ),
        ClawSize(3),
    )

    reporter.report_simulation_start(1)
    reporter.report_creature_evolved(decorated_pred)
    reporter.report_creature_evolved(bare_prey)
    reporter.report_outcome(OutcomeMessage.PREDATOR_WON)

    assert len(lines) == 4
    assert "Simulation #1" in lines[0]
    assert "power=33" in lines[1]
    assert "traits=[Teeth(+6), Claws(x3)]" in lines[1]
    assert "traits=[None]" in lines[2]
    assert lines[3] == OutcomeMessage.PREDATOR_WON.value
