from typing import TypeAlias

ScoreBoard: TypeAlias = dict[str, int]


def print_leader_board(scores: ScoreBoard, *, name_length=15, turn=None):
    """Pretty-print a scoreboard."""
    if turn is not None:
        print(f"\nRound {turn}")

    print("+------+-" + "-" * name_length + "-+-------+")
    print("+ rank + Name" + " " * (name_length - 4) + " + score +")
    print("+------+-" + "-" * name_length + "-+-------+")
    for j, (player, score) in enumerate(
        sorted(scores.items(), key=lambda x: x[1], reverse=True), start=1
    ):
        print(f"| {j:<4} | {player[:name_length]:<{name_length}} | {score:>5} |")
    print("+------+-" + "-" * name_length + "-+-------+")


def pick_winner(scores: ScoreBoard) -> tuple[str, int]:
    max_score = -1
    winner = ""
    for player, score in scores.items():
        if score > max_score:
            max_score = score
            winner = player
    return (winner, max_score)


def print_final(scores: ScoreBoard, turn) -> tuple[str, int]:
    winner, score = pick_winner(scores)
    print("=" * 25)
    print(f"The Winner in {turn} rounds is {winner} with a score of {score}!")
    print_leader_board(scores)

    return winner, score


def print_welcome(*, max_turns: int | None, max_score: int | None) -> None:
    if max_score is None and max_turns is None:
        raise ValueError(
            "Game must be bounded, both *max_turns* and *max_score* can not be None"
        )
    print("Game start!")
    print(
        f"  {max_turns if max_turns is not None else 'unlimited'} turns to "
        f"{max_score if max_score is not None else 'most'} points."
    )


def game_over(scores, cycle, max_turns, max_score):
    return (max_score is not None and max(scores.values()) >= max_score) or (
        max_turns is not None and cycle >= max_turns
    )
