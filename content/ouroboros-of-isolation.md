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

1. Get the software where you want to run or develop.
2. Get all of the dependencies [^deps] of that software also on the system
3. Do not break anything else that was previously on the system

The first two of are the obvious primary job of package managers (such as
[apt](https://en.wikipedia.org/wiki/APT_(software)),
[pacman](https://wiki.archlinux.org/title/pacman),
[conda](https://en.wikipedia.org/wiki/Conda_(package_manager)),
[yum](https://fedoraproject.org/wiki/Yum)/[dnf](https://en.wikipedia.org/wiki/DNF_(software)),
[pip](https://pip.pypa.io/en/stable/), [brew](https://brew.sh),
[spack](https://spack.io),
[...](https://en.wikipedia.org/wiki/List_of_software_package_management_systems)) which (very roughly):

1. Keep track of a bunch of (compressed) file trees.
2. Have enough meta-data on those artifacts to build up the dependency (and
   conflict) graph to select a set of file trees for a given installation
   request.  This systems need to take into account both the API compatibility (which
   can be derived from the source) and the ABI compatibility (which is established
   at build time).
3. Some method of putting the right set of files on your computer.

However, in this post I want to focus on the third aspect: making sure that any
installations are non-harmful to anything other software that you may be using.
I think it is this aspect of controlling the isolation is the biggest driver of
selecting which of the
[many](https://discuss.python.org/t/pep-704-require-virtual-environments-by-default-for-package-installers/22846/18)
ways you can "install" a Python library and what workflow tools seem
"simple"[^simple].

The degree of isolation varies based on the use case, the easy of use, and the relative
weight of the tooling required to achieve that isolation.  These can be order these as:


1. no isolation (system level installs)
2. overlays on system installs
3. virtual and conda environments
5. containers (podman, docker, flatpack, snaps, ...)
6. virtual machines
7. system installs on physical machines
8. ... wait a second, we have been here before

Starting from "system level installs" being the least isolated we eventually
got to them being the most isolated!  There is no universally "right" choice
for the level of isolation for all projects, however it does make sense to ask
if you are using the right level for a given project and if you want move up or
down the ladder.

The


## System-level isolation

The lowest level of isolation is at the "system" level.  This is the realm of
globally installed software (typically requiring some sort of elevated
administration access) and is primarily the realm of `apt`, `pacman`,
`yum`/`dnf`, `brew`, `emerge`, etc.  If you want to have two systems with
different software installed, you get a second system!

The whole reason for the existence of these packaging tools and the
distributions built around them is to ensure that there is a self-consistent
set of packages available to be installed.  For example, Linux distributions
that provide binary packages maintain [extensive build
farms](https://koji.fedoraproject.org/koji/packageinfo?packageID=3607) to
ensure that they have built artifacts for the architectures they support and
take care of rebuilding (if needed) when there are changes to a project's
upstream dependencies.

The biggest upside of using system packaging is the simplicity: there is one
version of the software on the computer[^named-versions].

However, of these benefits is also a draw back!  If you do need to upgrade a
package then you have to update it for everyone on the system and there is no
way to upgrade the package for only some users or only some of your projects:
it is all or nothing.  Due to the all-or-nothing nature of system level
packaging, the need for escalated permissions is an asset on multi-user shared
systems[^mu-system].  Not every user knows what every other user is doing and
having the shared software write-protected greatly reduces the amount of
inadvertent damage users can do to each other.

Some Linux distribution effectively freeze the versions of all of their
packages when they release and then only take bug-fixes going forward.  For
example, ff you are on an older Debian or Red Hat/CentOS system, the available
software can be [quite
old](https://centos.pkgs.org/7/centos-x86_64/python-matplotlib-1.2.0-16.el7.x86_64.rpm.html).
If you are the user on a shared system, and need a newer version, you may be
out of luck [^cf-history].

It should be noted that system packaging tool is not the only option to provide
users on shared machines with read-only software.  With a bit of work you can
make the results of _any_ packaging tool read-only[^ro-conda].


## System level + overlays

The next step up in increasing isolation is to make use of "overlays" on top of
the base system.  This leverages the (read-only) base system but adds
additional (user controlled) software on top.  Specifically for Python we have
[PEP 370]( https://peps.python.org/pep-0370/) that added site-packages in
user-controlled directories (this is the language feature that `pip install
--user` leverages), but there are also more general ways (setting `$PATH`,
`$LD_LIBRARY_PATH`, `$PYTHONPATH`, etc) to ensure that the users software is
found before the system version.

The biggest benefit of using overlays is that users have complete control over
the files placed there which can be a huge benefit for enabling multiple users
on a multi-users system to have exactly the versions they need and to
self-service upgrades.

However, because the underlying packaging system is unaware of the software the
users have installed and hence when the underlying system is updated it can not
take into account the user installed software.  This will inevitably lead to
the user software breaking when one of the dependencies is upgraded.


## User control environments

The next step up the isolation ladder is to build a complete environment in
user space including all of your dependencies.  This is the approach taken,
to varying degrees by `conda` and the tooling around `wheels` (`venv`, `virtualenl`, `pyvenv`)



## bottom notes
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
[^simple] "Simple" and it's fellow traveler "intuitive" are inherently
    subjective and rely on the assumptions encoded into the tool matching your
    personal assumptions.  If your needs and assumptions are different than the
    tool makes then you may spend tremendous time and effort working around and
    against the tool.
