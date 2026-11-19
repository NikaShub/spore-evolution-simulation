from collections.abc import Callable
from typing import Protocol

from spore_sim.domain.creature import CreatureProtocol
from spore_sim.domain.enums import OutcomeMessage

class SimulationReporter(Protocol):
    def report_simulation_start(self, simulation_index: int) -> None: ...

    def report_creature_evolved(self, creature: CreatureProtocol) -> None: ...

    def report_outcome(self, outcome: OutcomeMessage) -> None: ...


class ConsoleReporterAdapter:
    def __init__(self, output_fn: Callable[[str], None] = print) -> None:
        self._output = output_fn

    def report_simulation_start(self, simulation_index: int) -> None:
        self._output(f"Simulation #{simulation_index}")

    def report_creature_evolved(self, creature: CreatureProtocol) -> None:
        traits_text = ", ".join(creature.traits) if creature.traits else "None"
        self._output(
            f"[{creature.role.value}] "
            f"pos={creature.position}, "
            f"health={creature.health}, "
            f"stamina={creature.stamina}, "
            f"power={creature.attack_power}, "
            f"legs={creature.legs}, "
            f"wings={creature.wings}, "
            f"traits=[{traits_text}]"
        )

    def report_outcome(self, outcome: OutcomeMessage) -> None:
        self._output(outcome.value)

class MemoryReporterAdapter:
    def __init__(self) -> None:
        self.started_simulations: list[int] = []
        self.evolved_creatures: list[CreatureProtocol] = []
        self.outcomes: list[OutcomeMessage] = []

    def report_simulation_start(self, simulation_index: int) -> None:
        self.started_simulations.append(simulation_index)

    def report_creature_evolved(self, creature: CreatureProtocol) -> None:
        self.evolved_creatures.append(creature)

    def report_outcome(self, outcome: OutcomeMessage) -> None:
        self.outcomes.append(outcome)
