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
) -> Generator[ScoreBoard, ScoreBoard, ScoreBoard]:
    """Run a game."""

    scores = {p: int(0) for p in players}
    for cycle in count(1):
        # yield out the current scores (right hand)
        # get back
        increments = yield dict(scores)
        for player, increment in increments.items():
            scores[player] += increment
        # decide if we have a winner
        if game_over(scores, cycle, max_turns, max_score):
            return dict(scores)


def simulate(
    players: list[str], max_turns: int | None, max_score: int | None, *, verbose=True
) -> tuple[str, int]:
    # error checking and welcome message
    print_welcome(max_turns=max_turns, max_score=max_score)
    # set up coroutine
    gm = game(players, max_turns=max_turns, max_score=max_score)
    # prime the pump
    scores = gm.send(None)  # type: ignore
    if verbose:
        print_leader_board(scores)
    # play the game!
    for j in count(1):
        try:
            scores = gm.send({random.choice(players): random.randint(1, 5)})
        except StopIteration as ex:
            return print_final(ex.value, j)
        else:
            if verbose:
                print_leader_board(scores, turn=j)
