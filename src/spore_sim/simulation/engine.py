from spore_sim.domain.enums import OutcomeMessage
from spore_sim.evolution.factories import EvolutionFactory
from spore_sim.reporting.adapters import SimulationReporter
from spore_sim.simulation.phases import ChasePhase, FightPhase


class SingleSimulationRunner:
    def __init__(
        self,
        factory: EvolutionFactory,
        chase_phase: ChasePhase,
        fight_phase: FightPhase,
        reporter: SimulationReporter,
    ) -> None:
        self._factory = factory
        self._chase_phase = chase_phase
        self._fight_phase = fight_phase
        self._reporter = reporter

    def run(self) -> OutcomeMessage:
        predator, prey = self._factory.create_participants()
        self._reporter.report_creature_evolved(predator)
        self._reporter.report_creature_evolved(prey)

        caught = self._chase_phase.execute(predator, prey)
        if caught:
            outcome = self._fight_phase.execute(predator, prey)
        else:
            outcome = OutcomeMessage.PREY_ESCAPED
        self._reporter.report_outcome(outcome)
        return outcome
