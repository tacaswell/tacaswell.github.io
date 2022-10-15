Title: Coroutines (practical)
Date: 2022-10-14 17:25
Modified: 2022-10-15 11:15
Category: Computer Science
Tags: coroutines, python
Slug: coroutines-i
Authors: Thomas A Caswell
Summary: So you have been handed a generator co-routine...
Status: published


This is a explanation of how to practically work with generator coroutines in
Python.  If you are willing to accept the rules laid out in this (not so) short
guide as empirical observations then you should be able to productively work
with generator co-routines.  In a future post I intend to dive into the "why"
(and the "why this makes sense"), but this is the pragmatic view.

Generator coroutines in Python have two bi-directional communication channels

1. data `yield` / `send()`
3. exceptions via `raise` / `throw()`

and two unidirectional channels

1. data via `return`
2. `close()` to exit the coroutine immediately


Another way to look at this is generator co-routines have two "happy path"
communication channels:

1. data `yield` / `send()`
2. data via `return`

and two "sad path" communication channels:

1. exceptions via `raise` / `throw()`
2. `close()` to exit the coroutine immediately

Each of these channels has a different purpose and without one of them
co-routines would be incomplete.  You may not need to (explicitly) use all of
these channels in any given application.

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
[excecption](https://docs.python.org/3/library/exceptions.html#StopIteration).
We will come back to the raised Exception object in a bit.

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
2. The first `.send()` runs the coroutine up to the first `yield` and sends the
   right hand side out.  The value of the first `.send` _must_ be `None`
   because there is no way to access the value passed in.
3. The coroutine is suspendend until the next `send()`.  The value pass to the
   second `send()` is assigned to the left hand side of the `yield` expression.
4. The coroutine runs until the next `yield` and sends out the right hand side.  We
   then go back to step 3 until there are no more `yield` expressions in the coroutine.
5. when the coroutine returns Python will raise the `StopIteration` exception
   for us.

To see this more clearly, re-running the above code but sending in diffrent
values at each step:

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
    return 'Done!'
```

However, this raise the question of how do we get to the returned value?  It
can not come back as the return from `.send()` as that is where the `yield`
values are carried.  Instead the value is carried on the `StopIteration`
exception that is raised when the iterator is exhausted.

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
StopIteration: Done!
>>>
```

To get the the value we need to catch the `StopIteration`
and access `ex.value`.

```python
>>> gen = my_gen()
>>> print('yielded: ', gen.send(None))
yielded:  a
>>> for j in count(1):
...     try:
...         print('yielded: ', gen.send(f'step {j}'))
...     except StopIteration as ex:
...         print(f'Returned: {ex.value}')
...         break
...
got 'step 1'
yielded:  b
got 'step 2'
Returned: Done!
```

It may be tempting to try and raise your own `StopIteration` rather than
returning, however if you do Python will convert it to a `RuntimeError`.  This
is because Python can not tell the difference between your intentionally
raising `StopIteration` and something you have called unexpectedly raising
`StopIteration`.  Pre Python [CHECK VERSION] the `StopIteration` would be
raised to the outer caller which would be interpeted as the generator returning
normally which in turn would mask bugs in very confusing ways.

## `raise` / `throw` channel

Like all Python we can use the standard exception raising and handling tools,
however there are a couple a caveates.

1. The co-routine must not raise `StopIteration` (as noted above)
2. If you catch `GeneratorExit` the co-routine must return (see the section on
   `close()` below).

Any valid exception raised will inturn be raised from the call point of the
`obj.send()` in the outer code, identically to how an exception called in a
function will propogate to the call site.

```python
>>> def my_gen(N):
...    for j in count():
...        if j >= N:
...            return f"Got {N} ints and are done"
...        a = yield f'{j}/{N} ints in a row'
...        if not isinstance(a, int):
...            raise ValueError("We only take integers!")
...
```

If we exhaust the "happy path" of this co-routine we see:

```python
>>> gen = my_gen(3)
>>> gen.send(None)
'0/3 ints in a row'
>>> gen.send(1)
'1/3 ints in a row'
>>> gen.send(-1)
'2/3 ints in a row'
>>> gen.send(10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: Got 3 ints and are done
```

which raises `StopIteration` with the payload of a string as expected.  However, if we
were to send in not an integer

```python
>>> gen = my_gen(3)
>>> gen.send(None)
'0/3 ints in a row'
>>> gen.send(5)
'1/3 ints in a row'
>>> gen.send('aardvark')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 7, in my_gen
ValueError: We only take integers!
```

However, if an unhandled exception is raised from a co-routine it is fully
exhausted and subsequently sending in new values will immediantly raise
`StopIteration`.

Sometimes it is necessary to inject an exception into a co-routine, for example
to let the co-routine know the outer code did not like the last yielded value.
This can be done with the `obj.throw` method which causes the passed
`Exception` to be raised at the `yield`.  Within the co-routine we can use all
of the standard exception handling tools of Python:

```python
>>> def my_gen():
...    for j in range(5):
...        try:
...            inp = yield j
...        except ValueError:
...            print("Ignoring ValueError")
...        else:
...            print("No exception")
...        finally:
...            print("Finish loop")
...
>>> gen = my_gen()
>>> gen.send(None)
0
>>> gen.send('a')
No exception
Finish loop
1
>>> gen.send(None)
No exception
Finish loop
2
>>> gen.throw(ValueError)
Ignoring ValueError
Finish loop
3
>>> gen.throw(RuntimeError)
Finish loop
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in my_gen
RuntimeError
```

If the generator is exhausted than any exceptions thrown in are immediately
re-raised.


## `close` channel

Sometimes the outer caller of a generator needs to tell the co-routine to clean
up and drop-dead.  This is done via the `gen.close()` method which will cause a
`GeneratorExit` exepction to be raised at the point where the co-routine is
suspended (the `yield`).  If the co-routine catches this exception and tries to
yield additional values, then `close()` will raise a `RuntimeError`.

```python
>>> def my_gen():
...     for j in count():
...         try:
...             yield j
...         except GeneratorExit:
...             print("I refuse to exit")
...
>>> gen = my_gen()
>>> gen.send(None)
0
>>> gen.send(None)
1
>>> gen.send(None)
2
>>> gen.close()
I refuse to exit
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: generator ignored GeneratorExit
>>>
```

The reason that `GeneratorExit` is not suppressible is that it is as part of
garbage collection and Python must be able to clean up the co-routine.


If the co-routine catches the exception and `returns` there is no way for the
outer caller to access the returned value.

```python
>>> def my_gen():
...     for j in count():
...         try:
...             yield j
...         except GeneratorExit:
...             print("I acquiese to your request.")
...             return 'Aardvark'
...
>>> gen = my_gen()
>>> gen.send(None)
0
>>> gen.send(None)
1
>>> gen.send(None)
2
>>> gen.close()
I acquiese to your request.
>>>

```

This is particularly useful if the co-routine is holding onto resources, such
as open files or sockets, that need to be gracefully shut down.
