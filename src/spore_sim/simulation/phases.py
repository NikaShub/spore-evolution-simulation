from spore_sim.domain.creature import CreatureProtocol
from spore_sim.domain.enums import OutcomeMessage
from spore_sim.movement.handlers import MovementHandler
from spore_sim.movement.strategies import MovementStrategy


class ChasePhase:
    def __init__(
        self,
        movement_chain: MovementHandler,
        predator_strategy: MovementStrategy,
        prey_strategy: MovementStrategy,
    ) -> None:
        self._movement_chain = movement_chain
        self._predator_strategy = predator_strategy
        self._prey_strategy = prey_strategy

    def execute(
        self,
        predator: CreatureProtocol,
        prey: CreatureProtocol,
    ) -> bool:
        while True:
            self._step_creature(predator, self._predator_strategy)
            self._step_creature(prey, self._prey_strategy)

            if predator.position >= prey.position:
                return True
            if predator.stamina <= 0:
                return False

    def _step_creature(
        self,
        creature: CreatureProtocol,
        strategy: MovementStrategy,
    ) -> None:
        options = self._movement_chain.collect_options(creature)
        chosen = strategy.choose_movement(options)
        if chosen is not None:
            creature.move_by(chosen.speed, chosen.stamina_cost)


class FightPhase:
    def execute(
        self,
        predator: CreatureProtocol,
        prey: CreatureProtocol,
    ) -> OutcomeMessage:
        while predator.is_alive and prey.is_alive:
            predator.attack(prey)
            prey.attack(predator)

        if not prey.is_alive:
            return OutcomeMessage.PREDATOR_WON
        return OutcomeMessage.PREY_ESCAPED
