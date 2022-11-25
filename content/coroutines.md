Title: Corutines (philosophical)
Date: 2022-07-03 22:00
Modified: 2022-07-03 22:00
Category: Computer Science
Tags: generator coroutine
Slug: coroutines-ii
Authors: Thomas A Caswell
Summary: Understanding co-routines with an object analog
Status: draft

[Coroutines](https://en.wikipedia.org/wiki/Coroutine), as a concept, are hard
to explain because the analogies and language we have in (modern) software
development makes it nearly impossible to express.  Going back to Dijkstra's
[goto considered
harmful](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) essay
we have been trained to think of functions (sub-routine) as black boxes that
have exactly one entry point, one (external) exit point, there is always a very
clear caller / callee relationship and to quote [Rich
Hickey](https://www.infoq.com/presentations/Simple-Made-Easy/), we "don't know,
don't want to know" what is going on inside of the function body.  In contrast,
co-routines have _many_ entry and exit points, the distinction between caller
and callee is blurred, and due to the cooperative nature means that state will
persist between entry into the coroutine.  Taken together these aspect cut
directly against our trained intuition of how functions "should" work.


Although I have made effective use of coroutines in Python (as generators,
generator co-routines, and async co-routines) it was only very recently that I
had more than a pragmatic understanding of what they are.  The "ah-ha" moment
was reading Knuth's description of coroutines in [The Art of Computer
Programming Vol 1](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).
Knuth introduced the concept in the context of an Assembly language where there
is not a real concept of a "function call", only sub-routines that know to
return to where they were called from when they finish.  This is a world where
goto is not only not harmful, it is the only game in town!

If we consider this facsimile of an assembly program:

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

we can see th at there is an infinite loop.  If we end up on the line labeled
`A` we will run until we jump to `B` which will then run until we jump back to
`A`.  Note that we could have started at `B` and gone to `A`, the sub-routines
are symmetric with no clear "caller" or "callee".

In this case

The rest of this post is going to try to elucidate this concept by deforming
Object-oriented examples in Python to co-routines.


**Example 1: A scoreboard**


```python
{! coroutines_src/example1.py[ln:2,4,18-35] !}
```


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


```python
{! coroutines_src/example1.py[ln:7-16] !}
```
