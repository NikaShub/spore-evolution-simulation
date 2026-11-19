from typing import Self

from spore_sim.domain.enums import OutcomeMessage
from spore_sim.reporting.adapters import SimulationReporter
from spore_sim.simulation.engine import SingleSimulationRunner


class SimulationIterator:
    def __init__(
        self,
        runner: SingleSimulationRunner,
        reporter: SimulationReporter,
        total_runs: int,
    ) -> None:
        self._runner = runner
        self._reporter = reporter
        self._total_runs = total_runs
        self._current_run = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> OutcomeMessage:
        if self._current_run >= self._total_runs:
            raise StopIteration
        self._current_run += 1
        self._reporter.report_simulation_start(self._current_run)
        return self._runner.run()
