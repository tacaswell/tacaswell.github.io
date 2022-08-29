Title: Corutines (practical)
Date: 2022-07-03 22:00
Modified: 2022-07-03 22:00
Category: Computer Science
Tags: hosting
Slug: coroutines-i
Authors: Thomas A Caswell
Summary: So you have been handed a generator co-routine...
Status: draft


This is a explanation of how to practically work with generator coroutines in
Python.  In a future post I intend to dive into the "why", but for now the
pragmatic approach.

Generator coroutines in Python have two bi-directional communication channels

1. data `yield` / `send()`
3. exceptions via `raise` / `throw()`

and two unidirectional channel

1. data via `return`
2. `close()` to exit the coroutine immediately

## `yield` / `send()` data channel

The first half of this channel is `yield` which will (as the name suggests)
yield value out of the coroutine.  If we only use the `yield` the we have a
"generator function", for example if we write

```python
def my_gen():
    yield 'a'
    yield 'b'
    yield 'c'
```

which we can then use with the iteration protocol as:

```python
>>> list(my_gen())
['a', 'b', 'c']
```

More explicitly, what `list` (or a `for` loop) is doing under the hood is:

```python
>>> g = my_gen()
>>> next(g)
'a'
>>>
>>> next(g)
'b'
>>> next(g)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

The way that the generator communicates that it is exhausted is by raising the
`StopIteration`
[excecption](https://docs.python.org/3/library/exceptions.html#StopIteration)
as with all iterators (we will come back to the raised Exception object in a
bit).
