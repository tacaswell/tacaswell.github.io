Title: The Ouroboros of Isolation
Date: 2022-01-23 22:30
Modified: 2022-01-23 22:30
Category: Software Development
Tags: software, packaging
Slug: ouroboros-of-isolation
Authors: Thomas A Caswell
Summary: When you try to be more isolated you end up back where you began....



There is an active set of discussion on [Python
Discourse](https://discuss.python.org), blogs, and
[mastodon](https://fosstodon.org)[^links].
These discussions are productive (if sometimes frustrating and overheated),
however I think that we need to step back and look at the broader picture and
ask: Why do we even do packaging?

## Isolation to the center

Very roughly any packaging tool/ecosystem has roughly three goals:

1. Get the software where you want to run or develop it.
2. Get all of the dependencies [^deps] of that software also on the system
3. Do not break anything else that was previously on the system

The first two of are the obvious primary job of package managers (such as
[apt](https://en.wikipedia.org/wiki/APT_(software)),
[pacman](https://wiki.archlinux.org/title/pacman),
[conda](https://en.wikipedia.org/wiki/Conda_(package_manager)),
[yum](https://fedoraproject.org/wiki/Yum)/[dnf](https://en.wikipedia.org/wiki/DNF_(software)),
[pip](https://pip.pypa.io/en/stable/), [brew](https://brew.sh),
[pack](https://spack.io),
[...](https://en.wikipedia.org/wiki/List_of_software_package_management_systems)) which (very roughly):

1. Keep track of a bunch of (compressed) file trees.
2. Have enough meta-data on those artifacts to build up the dependency (and
   conflict) graph to sort out which set of them are needed for a given
   installation request.
3. Some method of putting the right set of files on your computer.

However, in this post I want to focus on the third aspect: making sure that any
installations are non-harmful to anything other software that you may be using.
I think it is this aspect of controlling the isolation is the biggest driver of
selecting which of the
[many](https://discuss.python.org/t/pep-704-require-virtual-environments-by-default-for-package-installers/22846/18)
ways you can install a Python project and what workflow tools seem "simple".


## System-level isolation

The lowest level of isolation is at the "system" level.  This is the realm of
globally installed software (typically requiring some sort of elevated
administration access) and is primarily the realm of `apt`, `pacman`,
`yum`/`dnf`, `brew`, `emerge`, etc.  The "modules" systems on super computers
would also fall into this category.

The whole reason for the existence of these packaging tools and the
distributions built around them is to ensure that there is a self-consistent
set of packages available to be installed.  For example, Linux distributions
that provide binary packages maintain [extensive build
farms](https://koji.fedoraproject.org/koji/packageinfo?packageID=3607) to
ensure that they have built artifacts for the architectures they support and
take care of rebuilding (if needed) when there are changes to a projects
upstream dependencies.


The need for escalated permissions can be a major upside on multi-user shared
systems[^mu-system].  Not every user knows what every other user is doing and
having the shared software write-protected greatly reduces the amount of
inadvertent damage users can do to each other.  It should be noted that in this
context the system packaging tool is not the only option and (with a bit of
work) you can make the results of _any_ packaging tool read-only[^ro-conda].

The biggest upside of using system packaging is the simplicity.  There is one
version of the software on the computer[^named-versions].

However, of these benefits is also a draw back!  Some Linux distribution
effectively freeze the versions of all of their package and only take
bug-fixes.  If you are on an older Debian or Red Hat/CentOS system, the
available software can be [quite
old](https://centos.pkgs.org/7/centos-x86_64/python-matplotlib-1.2.0-16.el7.x86_64.rpm.html).
If you are the user on a shared system, and need a newer version, you may be
out of luck [^cf-history].  Additionally, if you are working on more than one
project, or just want to test out different versions of a library, you may need
to have _multiple_ versions of something installed.

## System level + overlays

The next step up in increasing isolation is to make use of "overlays" in

https://pypackaging-native.github.io/



[^links]: Do not worry lots of specific links coming.
[^deps]: There are different kinds of depedencies:

    1. API compatibility in source
    2. ABI compatibility for built artifacts
    3. to-the-hilt pinning for reproducible deployments.

    In some cases, particularly with pure-Python projects, these can be elided
    together but in general need to be tracked independently and updated as part
    of the packaging process.
[^mu-system]: Multiuser systems are still extremely common in academia and
    resarch settings.  It is way simpler to set up a beefy machine and hand out
    access than almost anything else.
[^ro-conda]: At NSLS-II we use root-owned read-only [conda
    environments](https://github.com/nsls2-conda-envs) which are built on CI,
    packed via [`conda-pack`](https://conda.github.io/conda-pack/), published
    to [zenodo](https://zenodo.org/record/7470912), and then pulled to our
    system via automation.
[^named-versions]: You can sometimes get away with mangling the name (for
    example on my main desktop I have `python3.4`, `python3.5`, `python3.6`,
    `python3.7`, `python3.8`, `python3.9`, and `python3.10` on my `$PATH`
    (thanks to the [AUR](https://aur.archlinux.org)), however this relies on
    calling a different binary to switch Python version.  This does not quite
    work for Python libraries as you do not want to find-and-replace every
    `import numpy as np` to `import numpy2 as np`!
[^cf-history]: Phil Ellison started working on conda-forge to install new
    versions of Matplotlib on RHEL systems.
