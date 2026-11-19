from enum import IntEnum, StrEnum


class CreatureRole(StrEnum):
    PREDATOR = "Predator"
    PREY = "Pray"


class MovementType(StrEnum):
    CRAWLING = "Crawling"
    HOPPING = "Hopping"
    WALKING = "Walking"
    RUNNING = "Running"
    FLYING = "Flying"
    EXHAUSTED = "Exhausted"


class ClawSize(IntEnum):
    SMALL = 2
    MEDIUM = 3
    BIG = 4


class TeethSharpness(IntEnum):
    LOW = 3
    MEDIUM = 6
    HIGH = 9


class AttackModifierOrder(StrEnum):
    TEETH_THEN_CLAWS = "teeth_then_claws"
    CLAWS_THEN_TEETH = "claws_then_teeth"


class OutcomeMessage(StrEnum):
    PREY_ESCAPED = "Pray ran into infinity"
    PREDATOR_WON = "Predator won"
