Title: Corutines
Date: 2022-07-03 22:00
Modified: 2022-07-03 22:00
Category: Computer Science
Tags: hosting
Slug: coroutines-i
Authors: Thomas A Caswell
Summary: Understanding co-routines with an object analog
Status: draft

Co-routines are a concept that is hard to explain in part because the analogies
and language we have in (modern) software development makes it near impossible
to express.  Going back to Dijkstra's [goto considered
harmful](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) essay
we have been trained to think of functions as black boxes that have exactly one
entry point and exactly one (external) exit point.  In contrast co-routines,
which have many entry and exit points, cut directly against our trained
intuition of how functions (sub-routines) "should" work.


Internal, a function may have `return` statements, but from the outside we can
not tell but there is always only one entry point (the top) and any internal
state of a function (leaving aside global side-effects) does not survive from
call-to-call.  The intuition that you can not (and should not) know what is on
the other side of a function call is deeply baked into how we think about
software.

On the other hand, a co-routine generalizes the concept of function to have
_multiple_ entry points, _multiple_ exit points and the internal state of a
co-routine _does_ survive between calls!

This violates almost every expectation we have about how a function "should"
behave and leaves us bereft of good analogies.



Although I have been productively working with co-routines in Python (as
generators, generator co-routines, and async co-routines) for about 7 years, I
have only had a pragmatic understanding (I know the rules, can get them to do
what I want) rather than a fundamental understanding of what and why they are.
I recently had an ah-ha moment reading Knuth's description of them in [The Art
of Computer Programming Vol
1](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).  He introduced the
concept in the context of an Assembly language where there is not strict
concept of a "function call", only sub-routines than know how to return to
where they were called from when they finish.  This is a world where goto is
not only not harmful, it is the only game in town!

If we consider this proxcimily of an assembly program we can see that there is an
infinite loop.

```assembly

A cmd
  ...
  ...
  goto B
  ...
  ...
B cmd
  ...
  ...
  goto A
  ...
```

However we end up at `A`, we run through the sub-routine and then jump to `B`,
run through the next sub-routine, and then jump back to A restarting the cycle.
Note that we could have started at `B` and gone to `A`, the sub-routines are
symmetric with no clear "caller" or "callee" or notion of "stack depth" as we
have in Python.  The rest of this post is going to try to elucidate this concept by
deforming an Object-oriented example to be a generator co-routine and justify why
the co-routines in Python are a close approximation of the original concept.


**Example 1: A scoreboard**


```python
Player = NewType("Player", str)
Score = NewType("Score", int)


def print_leader_board(scores: dict[Player, Score], *, name_length=15):
    print("+------+-" + "-" * name_length + "-+-------+")
    print("+ rank + Name" + " " * (name_length - 4) + " + score +")
    print("+------+-" + "-" * name_length + "-+-------+")
    for j, (player, score) in enumerate(
        sorted(scores.items(), key=lambda x: x[1]), start=1
    ):
        print(f"| {j:<4} | {player[:name_length]:<{name_length}} | {score:>5} |")
    print("+------+-" + "-" * name_length + "-+-------+")


class ScoreBoard:
    def __init__(self, players: list[Player]):
        self._scores = {p: 0 for p in players}

    def update(self, increments: dict[Player, Score]) -> dict[Player, Score]:
        for player, increment in increments.values():
            self._scores[player] += increment

        return dict(self._scores)


SB = ScoreBoard(["Alice", "Bob", "Carter", "Dave"])
# update with no values
print_leader_board(SB.update({}))

```
