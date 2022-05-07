Title: Think Like Git
Date: 2021-12-31 18:00
Modified: 2021-12-31 18:00
Category: Software Design
Tags: software, git
Slug: think-like-git
Authors: Thomas A Caswell
Summary: Understanding how Git views the world for fun and profit

This post assumes you have already accepted that you have to use `git` and know
enough `git` incanttaions to get by day-to-day but now want to be able to
reason about (rather than just memorize / guess) what `git` is doing
and why.

## git's view of the world

At the core, `git` keeps track of many (many) copies of your code, creating a
copy when ever you commit.  Along with the code, `git` attaches to each a block
of text, information about who and when the code was written and commited, what
commits are the "parents", and a hash of all of that.  This hash serves both to
validate the commit and as a globally unique name for the commit.  Because each
commit knows its parents, the commits from a [directed asyclic
graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG) with the The
code snap-shots are the nodes, the parents define the edges, and it directed
because you can only go backwards in history (commits do not know who their
children are).  The hash includes information about the parents, thus the tree
is variation on a [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree).
This makes it possible to validate both each commit independently and the full
repository history.

Given such a graph, what operations would we want to do to it?  For example we
may want to:

2. label nodes
1. look at a node
1. add nodes
3. change/move nodes
3. share with your friends
3. remove nodes

## Label a commit

From the hash we have a globally unique identifier for each commit, however
these hashes look something like:
`6f8bc7c6f192f664a7ab2e4ff200d050bb2edc8f`. While unique and will suited from a
computer, it is neither memorable nor does roll off the tongue.  To give
human-friendly name to commits git offers two flavors of labels: **branches**
and **tags**.  The conceptual difference is that a **branch** is expected to
move between commits over time and **tags** are fixed to a particular branch
for all time.


**Branches** point to a fixed *concept*.  By convention most repositories have
a socially designated "canonical branch" that is the point of truth for the
development effort.  The exact name does not matter, but common names include
"main", "trunk", or "devel".  It is also conventional to do new development on
a "development" branch, named anything but the canonical branch name.  This
enables you to keep multiple independent work directions in flight at a time
and easily discard any work turns out to be less of a good idea than you
thought.

In contrast **tags** label a specific commit and never move.  This is used most
often for identifying released versions of software (e.g. v1.5.2).



## Look at a node

The

## Adding nodes

To add new nodes

## Resources

- parable of git
