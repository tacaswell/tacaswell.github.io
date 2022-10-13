Title: Corutines (practical)
Date: 2022-10-13 22:00
Modified: 2022-10-13 22:00
Category: Computer Science
Tags: coroutines, python
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

Using `yield` we can get information _out_ of generator coroutine, to get data
into the generator coroutine we need to capture a left-hand side of the `yield`
as

```python
def my_gen():
    in1 = yield 'a'
    print(f'got {in1!r}')
    in2 = yield 'b'
    print(f'got {in2!r}')
```

If we pass that to `list` we see:

```python
>> list(my_gen())
got None
got None
['a', 'b']
```

What this (and `next`) is doing under the hood is

```python
>>> g = my_gen()
>>> g.send(None)
'a'
>>> g.send(None)
got None
'b'
>>> g.send(None)
got None
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

The sequence is:

1. Create the generator.  At this point no code has run yet.
2. the first `.send()` which runs the coroutine up to the first `yield` sends
   the right hand side out.  The value of the first `.send` _must_ be `None`
   because there is no way to access the value.
3. the coroutine is suspendend until the next `send()` and that value is
   assigned to the left hand side.
4. the coroutine runs until the next `yield` and sends the right hand side out,
   going back to step 3
5. when the coroutine finishes Python will raise the `StopIteration` exception
   for us.

To be a bit more explicit if we in some other value:

```python
>>> g = my_gen()
>>> g.send(None)
'a'
>>> g.send('step 1')
got 'step 1'
'b'
>>> g.send('step 2')
got 'step 2'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

## `return` data channel

So far we have not used `return` and relying on the implicit `return None` that
Python provides.  As with any Python function we put a `return` in our
coroutine:


```python
def my_gen():
    in1 = yield 'a'
    print(f'got {in1!r}')
    in2 = yield 'b'
    print(f'got {in2!r}')
    return in2
```

This does raise the question of how do we get to the returned value?  It can
not come back as the return from `.send()` as that is where the `yield` values
come back.  Instead the value is carried on `StopIteration` exception that is
raised when the iterator is exhausted.





## Extra

Thus we can write a runner

```python

    for j in count():
        try:
            val = gen.send(f'step {j}' if j > 0 else None)
            print(f'runner got {val}')
        except StopIteration:
            return

```

which will exhaust the generator coroutine and capture the exception cleanly.
