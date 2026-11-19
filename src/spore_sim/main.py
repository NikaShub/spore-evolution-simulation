from spore_sim.config import SimulationConfig
from spore_sim.evolution.factories import RandomEvolutionFactory
from spore_sim.movement.handlers import build_default_movement_chain
from spore_sim.movement.strategies import GreedyMovementStrategy
from spore_sim.reporting.adapters import ConsoleReporterAdapter
from spore_sim.simulation.engine import SingleSimulationRunner
from spore_sim.simulation.iterators import SimulationIterator
from spore_sim.simulation.phases import ChasePhase, FightPhase


def build_simulation_batch(
    config: SimulationConfig | None = None,
) -> SimulationIterator:
    active_config = config if config is not None else SimulationConfig()
    reporter = ConsoleReporterAdapter()
    factory = RandomEvolutionFactory(active_config)
    movement_chain = build_default_movement_chain()
    strategy = GreedyMovementStrategy()

    chase_phase = ChasePhase(
        movement_chain=movement_chain,
        predator_strategy=strategy,
        prey_strategy=strategy,
    )

    fight_phase = FightPhase()

    runner = SingleSimulationRunner(
        factory=factory,
        chase_phase=chase_phase,
        fight_phase=fight_phase,
        reporter=reporter,
    )

    return SimulationIterator(
        runner=runner,
        reporter=reporter,
        total_runs=active_config.simulations_count,
    )


def main() -> None:
    batch = build_simulation_batch()
    for _outcome in batch:
        pass

    if __name__ == "__main__":
        main()
