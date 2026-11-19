import pytest

from spore_sim.domain.enums import MovementType
from spore_sim.movement.handlers import (
    CrawlHandler,
    FlyHandler,
    HopHandler,
    MovementHandler,
    MovementOption,
    RunHandler,
    WalkHandler,
)
from spore_sim.movement.strategies import (
    GreedyMovementStrategy,
    StaminaMovementStrategy,
)
from tests.conftest import CreatureBuilder


@pytest.mark.parametrize(
    ("wings", "stamina", "expected"),
    [
        (2, 80, True),
        (2, 120, True),
        (2, 79, False),
        (1, 100, False),
    ],
)
def test_fly_handler(
    make_creature: CreatureBuilder,
    wings: int,
    stamina: int,
    expected: bool,
) -> None:
    creature = make_creature(wings=wings, stamina=stamina)
    options = FlyHandler().collect_options(creature)
    assert (len(options) == 1) is expected


@pytest.mark.parametrize(
    ("legs", "stamina", "expected"),
    [
        (2, 60, True),
        (2, 59, False),
        (1, 100, False),
    ],
)
def test_run_handler(
    make_creature: CreatureBuilder,
    legs: int,
    stamina: int,
    expected: bool,
) -> None:
    creature = make_creature(legs=legs, stamina=stamina)
    options = RunHandler().collect_options(creature)
    assert (len(options) == 1) is expected


@pytest.mark.parametrize(
    ("legs", "stamina", "expected"),
    [
        (2, 40, True),
        (2, 39, False),
        (1, 80, False),
    ],
)
def test_walk_handler(
    make_creature: CreatureBuilder,
    legs: int,
    stamina: int,
    expected: bool,
) -> None:
    creature = make_creature(legs=legs, stamina=stamina)
    options = WalkHandler().collect_options(creature)
    assert (len(options) == 1) is expected


@pytest.mark.parametrize(
    ("legs", "stamina", "expected"),
    [
        (1, 20, True),
        (1, 19, False),
        (0, 100, False),
    ],
)
def test_hop_handler(
    make_creature: CreatureBuilder,
    legs: int,
    stamina: int,
    expected: bool,
) -> None:
    creature = make_creature(legs=legs, stamina=stamina)
    options = HopHandler().collect_options(creature)
    assert (len(options) == 1) is expected


def test_crawl_handler(
    make_creature: CreatureBuilder,
) -> None:
    assert len(CrawlHandler().collect_options(make_creature(stamina=1))) == 1
    assert len(CrawlHandler().collect_options(make_creature(stamina=0))) == 0

def test_full_chain_collects_all_valid_options_fully_evolved_creature(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
) -> None:
    creature = make_creature(legs=2, wings=2, stamina=100)
    options = movement_chain.collect_options(creature)

    assert [(opt.movement_type, opt.speed, opt.stamina_cost) for opt in options] == [
        (MovementType.FLYING, 8, 4),
        (MovementType.RUNNING, 6, 4),
        (MovementType.WALKING, 4, 2),
        (MovementType.HOPPING, 3, 2),
        (MovementType.CRAWLING, 1, 1),
    ]


def test_limbless_creature_can_only_crawl(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
) -> None:
    creature = make_creature(legs=0, wings=0, stamina=300)
    options = movement_chain.collect_options(creature)

    assert len(options) == 1
    assert options[0].movement_type is MovementType.CRAWLING


def test_legged_creature_degrades(
    make_creature: CreatureBuilder,
    movement_chain: MovementHandler,
) -> None:
    # 70 stamina -> Run, Walk, Hop, Crawl
    assert [
        o.movement_type
        for o in movement_chain.collect_options(make_creature(legs=2, stamina=70))
    ] == [
        MovementType.RUNNING,
        MovementType.WALKING,
        MovementType.HOPPING,
        MovementType.CRAWLING,
    ]

    # 45 stamina -> Walk, Hop, Crawl
    assert [
        o.movement_type
        for o in movement_chain.collect_options(make_creature(legs=2, stamina=45))
    ] == [
        MovementType.WALKING,
        MovementType.HOPPING,
        MovementType.CRAWLING,
    ]

    # 25 stamina -> Hop, Crawl
    assert [
        o.movement_type
        for o in movement_chain.collect_options(make_creature(legs=2, stamina=25))
    ] == [
        MovementType.HOPPING,
        MovementType.CRAWLING,
    ]

    # 10 stamina -> Crawl only
    assert [
        o.movement_type
        for o in movement_chain.collect_options(make_creature(legs=2, stamina=10))
    ] == [MovementType.CRAWLING]

    # 0 stamina -> None
    assert (
        movement_chain.collect_options(make_creature(legs=2, wings=2, stamina=0)) == []
    )

def test_strategies_handle_empty_options(
    greedy_strategy: GreedyMovementStrategy,
    saver_strategy: StaminaMovementStrategy,
) -> None:
    assert greedy_strategy.choose_movement([]) is None
    assert saver_strategy.choose_movement([]) is None


def test_greedy_strategy(
    greedy_strategy: GreedyMovementStrategy,
) -> None:
    options = [
        MovementOption(MovementType.CRAWLING, speed=1, stamina_cost=1),
        MovementOption(MovementType.FLYING, speed=8, stamina_cost=4),
        MovementOption(MovementType.WALKING, speed=4, stamina_cost=2),
    ]
    chosen = greedy_strategy.choose_movement(options)
    assert chosen is not None
    assert chosen.movement_type is MovementType.FLYING


def test_stamina_saver_strategy(
    saver_strategy: StaminaMovementStrategy,
) -> None:
    options = [
        MovementOption(MovementType.FLYING, speed=8, stamina_cost=4),
        MovementOption(MovementType.RUNNING, speed=6, stamina_cost=4),
        MovementOption(MovementType.WALKING, speed=4, stamina_cost=2),
    ]
    chosen = saver_strategy.choose_movement(options)
    assert chosen is not None
    assert chosen.movement_type is MovementType.WALKING