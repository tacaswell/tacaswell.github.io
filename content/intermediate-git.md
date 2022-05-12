Title: Think Like Git
Date: 2021-12-31 18:00
Modified: 2021-12-31 18:00
Category: Software Design
Tags: software, git
Slug: think-like-git
Authors: Thomas A Caswell
Summary: Understanding how Git views the world for fun and profit

This article is for people who already know how to use `git` day-to-day, but
want a deeper understand of the _why_ of `git` to do a better job reasoning
about what should or should not be possible rather than just memorizing
incantations.

While this text is going to (mostly) refer to the git CLI because it is the
lowest common denominator (everyone who uses git has access to the CLI!), but
there are many richer interface (I personally use [magit](https://magit.vc/)
and [gitk](https://git-scm.com/docs/gitk/) in my day-to-day work).  For each of
the CLI interfaces I'm highlighting I am only covering the aspect of them that
I use day-to-day.  Many of these CLIs can do more (and sometimes wildly
different!) things, see the links back to the documentation for the full details.

Another article in a similar vein to this, but starting from the usage point of
view, is [the Git Parable
](https://tom.preston-werner.com/2009/05/19/the-git-parable.html).  When I read
many this essay years ago it made `git` "click" for me.

[TOC]

## git's view of the world

At the core, `git` keeps track of many (many) copies of your code, creating a
copy when ever you commit.  Along with the code, `git` attaches to each a block
of text, information about who and when the code was written and committed, what
commits are the "parents", and a hash of all of that.  This hash serves both to
validate the commit and as a globally unique name for the commit.

Because each commit knows its parent(s), the commits from a [directed acyclic
graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG).  The code
snap-shots and metadata are the nodes, the parents define the edges, and
because you can only go backwards in history (commits do not know who their
children are) it is directed.  DAG's are a a relatively common data structure
in programming (and if you need to work with them in Python checkout
[networkx](http://networkx.org/documentation/stable/)) by identifying that one
underlies one of `git`'s core data structures we can start to develop intuition
of what will be easy on `git` history (if they would be easy to express via
operations on a DAG).

Incidentally, The hash includes information about the parents, thus the tree is
variation on a [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree).  Using
these hashes you can validate that a `git` repository is self consistent and
that the source you have checked out is indeed the source that was checked in.
Additionally, this means if you and a collaborator both have a clone of a
shared project then they can send you the hash of a commit and you can be sure
that you have both an identical working tree and identical history.

Given such a graph, what operations would we want to do to it?  For example we
want to

2. give commits human readable names (`git tag`, `git branch`)
1. compare source between commits (`git diff`)
1. look at the whole graph of commits (`gitk`, `git log`)
1. look at a commit (both the code content and meta-data) (`gitk`, `git switch`, `git checkout`)
1. add commits (`git stage`, `git add`)
3. discard changes (both local changes and whole commits) (`git reset`, `git checkout`, `git clean`)
3. change/move commits around the graph (`git rebase`, `git cherry-pick`)
3. share your code (and history) with your friends (`git push`, `git fetch`, `git remote`, `git merge`)

## What does in mean to be distributed (but centralized)?

From a technical stand point no clone of a `git` repository is more special
than any other.  Each contains a self consistent section of the history of the
repository and can share that information with each other.  From a certain
point of view, there is only one global history which consists of every commit
any developer on any computer has ever created and any given computer only ever
has a sub-graph of the full history.

While technically pure, fully distributed collaboration is deeply impractical.
Almost every project has socially picked a central repository to be considered
the "cannonical" repository.  For example for Matplotlib
[matplotlib/matplotlib](https://github/matplotlib/matplotlib) is _the_ ground
truth repository.  At the end of the day what _is_ Matplotlib the library is
that git history.  Because of the special social role that repository holds
only people with commit rights are able to push to that repository.  When
people talk about project having a "hard fork" or a "hostile fork" they are
referring to a community that has split about which repository is "the one" and
who has the ability to push to it.

Similarly, every commit has a (gloablly) unique name: its hash.  The branch and
tag names that we use are for the humans and any meaning we attach to the names
is purely social.  Within the canonical repository there is a particular
branches which are identified as _the_ branches.  For example on Matplotlib we
have `main` branch for new development and the `vX.Y.x` branches which are the
maintence branches for each `vX.Y.0` minor release..  To `git` these names are
meaningless, but socially they are critical.


In the standard fork-based development workflow that many open source software
projects use the commits move from less visible but loosely controlled parts of
the global graphs to more public and controlled parts.  For example anyone can
create commits on their local clone at will!  However no one else can (easily)
see them and those commits are inaccessible to almost everyone else who has
part of the total graph.  A developer can then choose to publish their commits
to a public location (for example I push all of my work on Matplotlib to
[tacaswell/matplotlib](https://github.cm/tacaswell/matplotlib) first).  Once
the commits are public anyone can see them, only a handful of people are likely
to actually access them.  To get the code into the canonical repository, and
hence used by everyone, the user can request that the committers to the
canonical repository "pull" or "merge" their branch into the default branch.  If
this "pull request" is accepted and merged the default branch then that code
is forever part of the projects history.


## Label a commit

From the hash we have a globally unique identifier for each commit, however
these hashes look something like:
`6f8bc7c6f192f664a7ab2e4ff200d050bb2edc8f`. While unique and well-suited from a
computer, it is neither memorable nor does roll off the tongue.

To give
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

To list, create, and delete branches use the `git branch`
[sub-command](https://git-scm.com/docs/git-branch).  The most important
incantations are:


```bash
git branch            # list local branches
git branch -c <name>  # create a branch
git branch -d <name>  # delete a branch, if safe
git branch -D <name>  # delete a branch over git's concerns
```

In `git` branches are cheap to make, when in doubt, make a new branch!

In contrast **tags** label a specific commit and never move.  This is used most
often for identifying released versions of software (e.g. v1.5.2).  To work with **tags**
use the `git tag` [sub-command](https://git-scm.com/docs/git-tag).  The most important incantations
are:

```bash
git tag           # list tags
git tag -a <name> # create a new tag
```

You should always create "annotated" tags.

## Compare source between nodes


There is a "dual space" relationship between the code state at each commit and
the differences between the commits.  If you have one you can always compute
the other. On first glance the natural way to track the changes of source over
time is to track the differences (this is in fact how many earlier version
control systems worked!).  However git (and mercurial) instead track the full
state of the of the source at each commit which solves a number of performance
problems and enables some additional operations.

Because the diffs between subsequent commits are derived, it is just as easy to
compute the diff between any two commits!  Using the `git diff`
[sub-command](https://git-scm.com/docs/git-diff).  To get the difference between two
commits :


```bash
git diff <commitA> <commitB>
```

Calling `git diff` without any arguments is very common command that will show
any uncommitted changes in your working tree.


## Look at the whole tree

It is useful to look at the whole graph.  There is the `git log`
[sub-command](https://git-scm.com/docs/git-log) which will show you text
versions of history, however this is an application where a GUI interface
really shines.  There is so much information available:

 - the commit message
 - the author and committer
 - dates
 - the computed diffs
 - the connectivity between the commits

that it is difficult to see it all and navigate it in a pure text interface.

My preferred tool for exploring the full history is
[gitk](https://git-scm.com/docs/gitk/) which is typically installed with git.
It is a bit ugly, but it works!  In addition to visualizing the tree it also
has a user interface for searching both the commit messages and the code
changes.

## Look at a node

When working with a git repository on your computer you almost always have one
of the commits materialized into a working tree (or more than one with the `git
worktree` [sub-command](https://git-scm.com/docs/git-worktree)).  The working
tree is, as the same suggests, where you actually do your work!  We will come
back to this in the next section.

To checkout a particular **commit** (or **tag** or **branch**) you can use the
`git checkout` [sub-command](https://git-scm.com/docs/git-checkout) as

```bash
git checkout <commit hash>  # checks out a particular commit
git checkout <tag name>     # checks out a particular tag
git checkout <branch name>  # checks out a particular branch
```

In addition, there is also a new `git switch`
[sub-command](https://git-scm.com/docs/git-switch) that is specifically for
switching branches.

```bash
git switch <branch>
```

which is more limited (`git checkout` has a number of other features) and
more clearly named for switching branches.

If you want to see the history of what commits you have had checked out (as
opposed to the history the repository) you can use the `git reflog`
[sub-command](https://git-scm.com/docs/git-reflog).  While not something to use
day-to-day, it can save your bacon in cases where you have accidentally lost
references to a commit.

## Adding nodes

The most important, and likely most common, operation we do on the graph is to
add new commits!

As mention above when you checkout a branch on your computer you have a working
tree that starts at the state of the commit you have checked out.  There is
special name that can be used as a commit `HEAD` which means "the commit that
is currently checked out in your work tree".  There is also the short hand
`HEAD^` which means "the commit before the one checked out", `HEAD^^` which
means "the commit two before the one checked out", and so on for repeated `^`.

As you make changes there are two common commands `git status`
[sub-command](https://git-scm.com/docs/git-status) and `git diff`
[sub-command](https://git-scm.com/docs/git-diff).  `git status` will give you a
summary of what changes you have in the local tree, relative to `HEAD` and what
changes are staged. `git diff`, when called with no arguments will show the detailed
diff between the current working tree and `HEAD`.

As you work on your code, `git` does not require you to commit all of your
changes at once, but to enable this committing is two stage process.  The first step is to use
the `git add` [sub-command](https://git-scm.com/docs/git-add) to stage changes

```bash
git add path/to/file  # to stage all the changes in a file
git add -p            # to commit by hunk
```

Once you have staged all of the changes you want, you create a new commit via the
`git commit` [sub-command](https://git-scm.com/docs/git-commit)

```bash
git commit -m "Short Message"   # commit with a short commit message
git commit                      # open an editor to write a commit message
```

Writing a commit message is one of the most important parts of using git.
While it is frequently possible to, only from the source, reconstruct the what
of a code change it can be impossible to reconstruct the _why_ of the change.
The commit message is a place that you can leave notes to your collaborators
explaining the motivations of the change.  Remember that your most frequent
collaborator is your future / past self!  For a comprehensive guide to writing
good commit messages see [this article](https://cbea.ms/git-commit/).

As `git` encourages the creation of **branches** for new development, when the
work is done (via the cycle above) we will need to merge this work back into
the canonical branch which is done via the `git merge`
[sub-command](https://git-scm.com/docs/git-merge).  By default, this will
create a new commit on your current branch who's has two parents (the tips of
each branch involved).

```bash
git merge <other branch>   # merge other branch into the current branch
```

If you are using a code hosting platform (GitHub, GitLab, BitBucket, ...) this
command will typically be done through a the web UI's "merge" button.

## discard changes

Not all changes are a good idea, sometimes you need to go back.

If you have not yet committed your changes then they can be discarded using the
`git checkout` [sub-command](https://git-scm.com/docs/git-checkout) (yes the
same one we used to change branches)

```bash
git checkout path/to/file  # discard local changes
```

If you need to discard **commits** you can use the `git reset`
[sub-command](https://git-scm.com/docs/git-reset).  By default `git reset` will
change the currently checked out commit but not change your working tree (so you keep
all of the code changes).

```bash
git reset HEAD^      # move the branch back one, keep working tree the same
git reset HEAD^^     # move the branch back two, keep working tree the same
git reset <a SHA1>   # move the branch a commit, keep working tree the same
```

Alternatively if you want to discard the commits and the changes you can use
the `--hard` flag:

```bash
git reset --hard HEAD^     # move the branch back one, discard all changes
git reset --hard HEAD^^    # move the branch back two, discard all changes
git reset --hard <a SHA1>  # move the branch a commit, discard all changes
```

Be aware that these can be a destructive commands!  If you move a branch back
there maybe commits that are inaccessible (remember commits only know their
parents).  This is where the `git reflog`
[sub-command](https://git-scm.com/docs/git-reflog) can help recover the lost
commits.

`git` commands may create objects behind the scenes that ultimately become
inaccessible.  `git` will on its own clean up, but you can manually trigger
this clean up via `git gc` [sub-command](https://git-scm.com/docs/git-gc).

If you have accidentally committed something sensitive, but not yet pushed, you
can use these tools to purge it.


## change or move nodes

Due to the way the hashes work in `git` you can not truly _change_ a commit,
but you can modify and recommit it or make copies else where in the graph.
Remember that if you have already shared the commits you are replacing you will
have to force-push them again.  Be very careful about doing this to any branch
that many other people are using.

If you have just created a commit and realized you need to add one more change
you can use the `--amend` flag to `git commit`
[sub-command](https://git-scm.com/docs/git-commit).

```bash
# hack
git add path/to/file     # stage the changes like normal
git commit --amend       # add the changes to the HEAD commit
```

This does not actually _change_ the old commit.  A commit is uniquely
identified by its hash and the hash includes the state of the code, thus
"amending" a commit creates a *new* commit and then resets the current branch
to point to the new commit and orphans the old commit.

If you want to move a range of commits from one place to another you can use
the `git rebase` [sub-command](https://git-scm.com/docs/git-rebase).

```bash
git rebase target_branch     # rebase the current branch onto target_branch
```

which will attempt to "replay" the changes in each of the commits on your
current branch on top of `target_branch`.  If there are conflicts that `git`
can not automatically resolve it will pause for you to manually resolve the
conflicts and stage the changes to continue or abort the whole rebase

```bash
git rebase --continue   #  continue with your manual resolution
git rebase --abort      #  abort and go back to where you started
```

If you want to re-order, drop or combine commits you can use:

```bash
git rebase -i                # interactively rebase, squash and re-order
```

which will open an editor with instructions.  This can be particularly useful
if you want commit early and often as you work, but then when you are done
re-order and re-arrange the changes into a smaller number of better organized
commits.

If you want to have a commit from one branch to another `git cherry-pick`
[sub-command](https://git-scm.com/docs/git-cherry-pick)

```bash
git cherry-pick <commit>      # pick the commit on to the current branch
git cherry-pick -m 1 <commit> # pick a merge commit onto the current branch
git cherry-pick --continue    # continue if you have to manually resolve conflicts
git cherry-pick --skip        # drop a redundant commit
git cherry-pick --abort       # give up and go back to where you started
```


In all of these cases, [sub-command](https://git-scm.com/docs/git-reflog) can
be useful if things do not go as you expect!

## Sharing with your friends

So far we have not talked about any of the collaborative or distributed nature
of git!  While version control is useful if you are working alone (again, your
most frequent collaborator is your future / past self), it really shines when
you are working with other people.

To share code with others we need to a notion of a shared history.  Given that
under the hood git is a graph of nodes uniquely named by their content "all" we
have to do is be able to share information about the commits, branches, and
tags between the different computers!

If there is an existing repository that you want to get locally to start working on
you can use the `git clone` [sub-command](https://git-scm.com/docs/git-clone):

```bash
git clone url_to_remote    # will create a new directory in the CWD
```

By default this will set up one "remote" pointing to where ever you cloned
from.  To rename or change the url of this remote and add new remotes use the
`git remote` [sub-command](https://git-scm.com/docs/git-remote).

```bash
git remote add <name> <url>     # add a new remote
git remote rm <name>            # delete a remote
git remote rename <old> <new>   # rename a remote from old -> new
```

Once you have one or more remotes updated the first thing we want to is be able
to get new commits from the remotes via `git
fetch`[sub-command](https://git-scm.com/docs/git-fetch) or `git remote`
[sub-command](https://git-scm.com/docs/git-remote).

```bash
git fetch <name>      # fetch just one remote
git fetch --all       # fetch all of the
git remote update     # update all the remotes
```

The `git pull` [sub-command](https://git-scm.com/docs/git-pull) combines a
fetch and a merge into one command.  While this seems convenient, it will
frequently generate unexpected merge commits that take longer to clean up than
being explicit about fetching and merging separately.

```bash
git merge remote/branch   # merge remote branch into the local branch
```

To share your work back to others you need to put the commits someplace other
people can see it.  The exact details of this depend on the workflow of the
project and team, but if using a hosting platform this is done via the `git
push` [sub-command](https://git-scm.com/docs/git-push).

```bash
git push <remote> <branch_name>       # push the branch_name to remote
git branch --set-upstream-to <remote> # set an "upstream"
git push                              # "do the right thing" with upstream set
```

Given that in a typical workflow you are likely to be pushing to the same
branch on the same remote many times.  By telling git about this association we
save both typing and the chance of mistakes due to typos.

If you try to push commits to a remote branch that has commits that are not on
your local branch git will reject the push.  The course of action depends on
why you are missing commits.  If there are new commits on the remote branch
that you have not fetched before, then you should either merge the remote
branch into your local branch before pushing or rebase your local branch on the
remote branch and push again.

Because git can not tell the difference new commits on the remote and old
commits on the remote because you have re-written history locally, either via
`git commit --ammend` or `git rebase`, then you have to do something a bit ....
dangerous.  The source of the error is `git` detecting that if the remote branch were
to be updated to where the local branch it would make some commits inaccessible.  In
these cases we need to tell `git` to trust our judgment and do it anyway:

```bash
git push --force-with-lease
```

Be very careful about doing this to branches that other people are relying on.
We recently had to [re-write the history on the default Matplotlib
branch](https://discourse.matplotlib.org/t/default-branch-renamed-with-minor-edit-to-history/22367)
and it required a fair amount of planning and work to manage.



## git config

There are many (many) knobs to configure the default behavior.  I suggest using
starting with these settings:

```conf
[transfer]
    fsckobjects = true
[fetch]
    fsckobjects = true
    prune = true
    parallel = 0
[receive]
    fsckObjects = true
[pull]
    ff = only
[merge]
    ff = only
[color]
    ui = auto
[init]
    defaultBranch = main
[feature]
    manyFiles = true
[alias]
    credit = blame
```

## Other things you might want to do

- track the history of a line of code back in time
- remove untracked and ignored files
- find the commit that broke something
- merge un-related git histories into one
- extract the history of a sub-directory into its own repository
- purge a particular file (or change) from the history
- set up multiple worktrees
- make a new repo


## Other resources

- [recovering from git mistakes](https://ohshitgit.com/) ([worksafe
  version](https://dangitgit.com/en)): A humorous (and vulgar) guide to
  recovering when things go wrong.
- [the Git
  Parable](https://tom.preston-werner.com/2009/05/19/the-git-parable.html): A
  just-so story that takes you from making backups by hand to agreeing with
  some of the more mystifying choices git makes.
- [Anything Raymond
  Chen](https://devblogs.microsoft.com/search?query=git&blog=%2Foldnewthing%2F)
  has written about git.  Some of these are just mind bending, like [Mundane
  git commit-tree trick, Part 5: Squashing without git
  rebase](https://devblogs.microsoft.com/oldnewthing/20190510-00/?p=102488)


## Acknowledgments

Thank you to James Powell and Dora Caswell who read (or listened to) early
drafts of this post and provided valuable feedback.
