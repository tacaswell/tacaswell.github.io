from collections.abc import Generator
from itertools import count
import random
from game_utils import (
    print_welcome,
    print_leader_board,
    print_final,
    ScoreBoard,
    game_over,
)


def game(
    players: list[str],
    *,
    max_turns: int | None = None,
    max_score: int | None = None,
    verbose=True,
) -> tuple[str, int]:
    """Run a game."""
    print_welcome(max_turns=max_turns, max_score=max_score)

    scores = {p: int(0) for p in players}
    if verbose:
        print_leader_board(scores)
    sim = simulate(players, max_turns=max_turns, max_score=max_score)
    sim.send(None)  # type: ignore
    for cycle in count(1):
        try:
            increments = sim.send(scores)
            for player, increment in increments.items():
                scores[player] += increment
        except StopIteration as ex:
            return print_final(ex.value, cycle)
        else:
            if verbose:
                print_leader_board(scores, turn=cycle)


def simulate(
    players: list[str], max_turns: int | None, max_score: int | None
) -> Generator[ScoreBoard, ScoreBoard, ScoreBoard]:
    scores = yield {}
    for cycle in count(1):
        scores = yield {random.choice(players): random.randint(1, 5)}
        if game_over(scores, cycle, max_turns, max_score):
            return scores
