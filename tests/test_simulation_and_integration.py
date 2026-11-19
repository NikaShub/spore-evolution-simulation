import pytest

from spore_sim.config import SimulationConfig
from spore_sim.domain.enums import CreatureRole, OutcomeMessage
from spore_sim.evolution.factories import PresetEvolutionFactory
from spore_sim.main import build_simulation_batch
from spore_sim.movement.handlers import MovementHandler
from spore_sim.movement.strategies import GreedyMovementStrategy
from spore_sim.reporting.adapters import MemoryReporterAdapter
from spore_sim.simulation.engine import SingleSimulationRunner
from spore_sim.simulation.iterators import SimulationIterator
from spore_sim.simulation.phases import ChasePhase, FightPhase
from tests.conftest import CreatureBuilder



def test_chase_phase_catches_slower_prey(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    predator = make_creature(
        role=CreatureRole.PREDATOR,
        position=0,
        stamina=100,
        wings=2,
    )
    prey = make_creature(
        role=CreatureRole.PREY,
        position=14,
        stamina=100,
        legs=0,
        wings=0,
    )
    chase = ChasePhase(movement_chain, greedy_strategy, greedy_strategy)
    assert chase.execute(predator, prey) is True
    assert predator.position == 16
    assert prey.position == 16
    assert predator.stamina == 92
    assert prey.stamina == 98


def test_chase_phase_prey_at_zero_still_moves_before_catch_check(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    predator = make_creature(
        role=CreatureRole.PREDATOR,
        position=0,
        stamina=1,
        legs=0,
    )
    prey = make_creature(
        role=CreatureRole.PREY,
        position=0,
        stamina=100,
        legs=2,
    )
    chase = ChasePhase(movement_chain, greedy_strategy, greedy_strategy)

    assert chase.execute(predator, prey) is False
    assert predator.position == 1
    assert prey.position == 6
    assert predator.stamina == 0


def test_chase_phase_predator_catches_no_stamina_prey(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    predator = make_creature(
        role=CreatureRole.PREDATOR,
        position=0,
        stamina=20,
        legs=0,
    )
    prey = make_creature(
        role=CreatureRole.PREY,
        position=4,
        stamina=1,
        legs=0,
    )
    chase = ChasePhase(movement_chain, greedy_strategy, greedy_strategy)

    assert chase.execute(predator, prey) is True
    assert prey.stamina == 0
    assert predator.position >= prey.position


def test_fight_phase_predator_wins(make_creature: CreatureBuilder) -> None:
    predator = make_creature(role=CreatureRole.PREDATOR, health=100, base_power=30)
    prey = make_creature(role=CreatureRole.PREY, health=80, base_power=10)

    outcome = FightPhase().execute(predator, prey)
    assert outcome is OutcomeMessage.PREDATOR_WON
    assert predator.health == 70
    assert prey.health == 0


def test_fight_phase_prey_wins_predator_dies_first(
    make_creature: CreatureBuilder,
) -> None:
    predator = make_creature(role=CreatureRole.PREDATOR, health=25, base_power=10)
    prey = make_creature(role=CreatureRole.PREY, health=100, base_power=15)

    outcome = FightPhase().execute(predator, prey)
    assert outcome is OutcomeMessage.PREY_ESCAPED
    assert predator.health == 0
    assert prey.health == 80


def test_fight_phase_simultaneous_death(
    make_creature: CreatureBuilder,
) -> None:
    predator = make_creature(role=CreatureRole.PREDATOR, health=20, base_power=20)
    prey = make_creature(role=CreatureRole.PREY, health=20, base_power=20)

    outcome = FightPhase().execute(predator, prey)
    assert outcome is OutcomeMessage.PREDATOR_WON
    assert predator.is_alive is False
    assert prey.is_alive is False

def test_single_runner_skips_fight_when_prey_escapes_chase(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    predator = make_creature(
        role=CreatureRole.PREDATOR,
        position=0,
        health=100,
        stamina=2,
        base_power=50,
    )
    prey = make_creature(
        role=CreatureRole.PREY,
        position=100,
        health=10,
        stamina=100,
        base_power=50,
    )
    reporter = MemoryReporterAdapter()
    runner = SingleSimulationRunner(
        factory=PresetEvolutionFactory(predator, prey),
        chase_phase=ChasePhase(movement_chain, greedy_strategy, greedy_strategy),
        fight_phase=FightPhase(),
        reporter=reporter,
    )

    outcome = runner.run()
    assert outcome is OutcomeMessage.PREY_ESCAPED
    assert predator.health == 100
    assert prey.health == 10
    assert reporter.outcomes == [OutcomeMessage.PREY_ESCAPED]


def test_simulation_iterator_yields_exact_runs_and_stops(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    predator = make_creature(
        role=CreatureRole.PREDATOR,
        position=0,
        health=100,
        stamina=100,
        base_power=25,
    )
    prey = make_creature(
        role=CreatureRole.PREY,
        position=0,
        health=20,
        stamina=100,
        base_power=1,
    )
    reporter = MemoryReporterAdapter()
    runner = SingleSimulationRunner(
        factory=PresetEvolutionFactory(predator, prey),
        chase_phase=ChasePhase(movement_chain, greedy_strategy, greedy_strategy),
        fight_phase=FightPhase(),
        reporter=reporter,
    )
    iterator = SimulationIterator(runner=runner, reporter=reporter, total_runs=4)

    results = list(iterator)
    assert len(results) == 4
    assert reporter.started_simulations == [1, 2, 3, 4]
    with pytest.raises(StopIteration):
        next(iterator)


def test_end_to_end_100_simulations_batch() -> None:
    config = SimulationConfig(simulations_count=100)
    batch = build_simulation_batch(config)
    outcomes = list(batch)

    assert len(outcomes) == 100
    assert all(
        outcome in {OutcomeMessage.PREDATOR_WON, OutcomeMessage.PREY_ESCAPED}
        for outcome in outcomes
    )