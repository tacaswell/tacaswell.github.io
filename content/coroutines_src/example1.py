from collections.abc import Generator
from typing import TypeAlias

ScoreBoard: TypeAlias = dict[str, int]


def print_leader_board(scores: ScoreBoard, *, name_length=15):
    """Pretty-print a scoreboard."""
    print("+------+-" + "-" * name_length + "-+-------+")
    print("+ rank + Name" + " " * (name_length - 4) + " + score +")
    print("+------+-" + "-" * name_length + "-+-------+")
    for j, (player, score) in enumerate(
        sorted(scores.items(), key=lambda x: x[1], reverse=True), start=1
    ):
        print(f"| {j:<4} | {player[:name_length]:<{name_length}} | {score:>5} |")
    print("+------+-" + "-" * name_length + "-+-------+")


class ScoreBoardManager:
    _scores: ScoreBoard

    def __init__(self, players: list[str]):
        """A class to manage a scoreboard."""
        self._scores = {p: int(0) for p in players}

    def update(self, increments: ScoreBoard) -> ScoreBoard:
        """Update the scoreboard."""
        for player, increment in increments.items():
            self._scores[player] += increment

        return dict(self._scores)

    @property
    def scores(self) -> ScoreBoard:
        return dict(self._scores)


def scoreboard_coro(players: list[str]) -> Generator[ScoreBoard, ScoreBoard, None]:
    """Update the scoreboard."""
    scores = {p: int(0) for p in players}
    while True:
        increments = yield dict(scores)
        for player, increment in increments.items():
            scores[player] += increment
    return None


if __name__ == "__main__":
    SB = ScoreBoardManager(["Alice", "Bob", "Carter", "Dave"])
    # update with no values
    print_leader_board(SB.update({}))
    print_leader_board(SB.update({"Alice": 1}))
    print_leader_board(SB.update({"Bob": 2, "Dave": 3}))
    print_leader_board(SB.update({"Carter": 5}))

    cr = scoreboard_coro(["Alice", "Bob", "Carter", "Dave"])
    # prime the pump
    cr.send(None)  # type: ignore
    print_leader_board(cr.send({}))
    print_leader_board(cr.send({"Alice": 1}))
    print_leader_board(cr.send({"Bob": 2, "Dave": 3}))
    print_leader_board(cr.send({"Carter": 5}))
