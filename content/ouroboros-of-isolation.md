Title: The Ouroboros of Isolation
Date: 2022-01-23 22:30
Modified: 2022-01-23 22:30
Category: Software Development
Tags: software, packaging
Slug: ouroboros-of-isolation
Authors: Thomas A Caswell
Summary: When you try to be more isolated you end up back where you began....


In the Python community there is a now a (at least) decade old discussion on
the "right" way to do packaging.  This discussion has sometimes been expressed
as new packaging formats -- eggs, conda packages, wheels -- sometimes in
expressed as new tools for existing ecosystems -- uv, mamba, pixi, poetry, --
and sometimes as (extensive) writing -- on social media, blog posts[^meta], and
forums.  This discussions are frequently contentious, usually feature people
talking past each other, and remain unresolved.  [Smarter people than
me](https://hachyderm.io/@stargirl/109697057391904145) hold it is impossible to
resolve, however in this post I am going to propose a framing, centered on how
notions and levels of isolation, that will hope to sort the many approaches and
tools in a coherent way.


## Bring isolation to the center

Very roughly any packaging tool/ecosystem has high-level three goals:

1. Get the software where you want to run or develop on your computer.
2. Get all of the dependencies [^deps] of that software.
3. Do not break anything else that was previously worked.

The first two of are the obvious primary job of package managers (such as
[apt](https://en.wikipedia.org/wiki/APT_(software)),
[pacman](https://wiki.archlinux.org/title/pacman),
[conda](https://en.wikipedia.org/wiki/Conda_(package_manager)),
[yum](https://fedoraproject.org/wiki/Yum)/[dnf](https://en.wikipedia.org/wiki/DNF_(software)),
[pip](https://pip.pypa.io/en/stable/), [brew](https://brew.sh),
[spack](https://spack.io),
[...](https://en.wikipedia.org/wiki/List_of_software_package_management_systems)) which (very roughly):

0. Have a way to build binary artifacts.
1. Keep track of the (compressed) file trees it built.
2. Have enough meta-data about the artifacts to build up the dependency (and
   conflict) graph to select a set of file trees for a given installation
   request.  This systems need to (but not all systems actually do) take into
   account both the API compatibility (which can be derived from the source)
   and the ABI compatibility (which is established at build time).
3. Some method of putting the right set of files in the right place on your
   computer.

However, in this post I want to focus on the third aspect: making sure that any
installations are non-harmful to anything other software that you may be using.
How to manage the isolation, possibly driven by things outside of Python, is
the biggest driver of selecting which of the
[many](https://discuss.python.org/t/pep-704-require-virtual-environments-by-default-for-package-installers/22846/18)
ways you can "install" a Python library and what workflow tools seem
"intuitive"[^intuitive] or "simple".

Starting from the lowest level of isolation we can walk through tools that provide increasing isolation:

1. global system installs on a physical machine
2. overlays on system installs
3. "light" and "heavy" user controlled environments
3. self-contained monoliths
5. containers and other process isolation tools
6. virtual machines
7. global system installs on a physical ... wait a second, we have been here
   before!

Starting from "system level installs" being the least isolated we eventually
got to them being the most isolated like an or Ouroboros or an McEsher drawing.

There is no universally "right" choice for the level of isolation for all
projects, you need to make sure you are using the right level for a given
project and if you want move up or down the ladder.  In these discussions we
need to remember to have compassion for people who have different needs than
our own.


## global system installs

The first level of isolation is at the "system" level.  This is the realm of
globally installed software (typically requiring some sort of elevated
administration access) and is primarily the realm of `apt`, `pacman`,
`yum`/`dnf`, `brew`, `emerge`, etc.

The whole reason for the existence of these packaging tools and the
distributions built around them is to ensure that there is a self-consistent
set of packages available to be installed.  For example, Linux distributions
that provide binary packages maintain [extensive build
farms](https://koji.fedoraproject.org/koji/packageinfo?packageID=3607) to
ensure that they have built artifacts for the architectures they support and
take care of rebuilding (if needed) when there are changes to a project's
upstream dependencies.

The biggest upside of using system packaging is the simplicity: there is one
version of the software on the computer[^named-versions] and you use it.  If it
is a multi-user system[^mu-system] all the users use the same version.

However, of this benefit is also the main draw back!  If you do need to upgrade
a package then you have to update it for everyone on the system.  There is no
way to upgrade the package for only some users or only some of your projects:
it is all or nothing.  This is one of the reasons why managing system packages
typically requires elevated privileges.  Not every user knows what every other
user is doing and having the shared software write-protected greatly reduces
the amount of inadvertent damage users can do to each other.

Another drawback is that depending on the distribution, there can be a lag between
a version of a package being released to it being available from the distribution.
Some Linux distribution effectively freeze the versions of all of their
packages when they release and then only take bug-fixes going forward.  For
example, if you are on an older -- but still supported -- Debian or Red Hat system,
the available software can be quite old.  If you are the user on a shared
system, and need a newer version, you need to resort to various user-level
tools[^cf-history].


## System packages with "overlays"

The next step up in increasing isolation is to make use of "overlays" on top of
the base system.  This leverages the (read-only) base system but adds
additional (user controlled) software on top.  In the general case this
involves invoking binaries directly or adding directories to `$PATH` or
`$LD_LIBRARY_PATH` on a unix system [^winpath].  This way user built binaries
and libraries can be used.

In Python the equivalent is to launch `python` with a working directory that
contains additional `.py` files which will (by default) be importable.  This
can be a powerful way to write a small library to be used in a handful of
related scripts or notebooks.  The next elaboration on this is to add
additional directories to the Python path[^pathhacking] to ensure that your
module or package is importable no matter where the Python process is launched
from.

We also have [PEP 370]( https://peps.python.org/pep-0370/) which added
site-packages in user-controlled directories implicitly in the Python path.
This is the language feature that `pip install --user` leverages to enable
installing packages from PyPI on top of system packages.

The biggest benefit of using overlays is that users have complete control over
the files placed there.  This is a huge benefit for enabling individual users
on a multi-users system to have exactly the versions they need and self-service
upgrades.

However, because the underlying packaging system is unaware of the software the
users have installed when the underlying system is updated it can not take into
account the user installed software.  This will inevitably lead to the user
software breaking when one of the dependencies is upgraded.

There is also still a "global" aspect to these overlays as all processes run by
the user will see the same overlays.  If a user wants to run
multiple processes using different versions of dependencies or only test out a
version upgrade, they are out of luck.

Another significant downside of this approach is that for packages with native
code extensions (c, c++, FORTRAN) you must be prepared to compile the
extensions yourself to ensure that they are built consistently with the
underlying system or use wheels and accept the risk that generic binaries will
not work on or not be fully optimized for your platform.

## User controlled environments

The next step up the isolation ladder is to build a complete "self-contained"
(levels of self-containment vary) environment in user space.  This environment
is then "activated" on demand, either explicitly by the user or automatically
by tooling.  By putting the environment's directories at the front various
paths that control the shell and only adding the environments paths to
`sys.path`.  This provides almost completed isolation for `imports` with in
Python[^package_chaos], however binaries on the `PATH` are still available.
This is mostly a feature as this way core programs, like `ls` and `emacs`, are
available in an activated environment[^only-works-in-python].  Because the
whole environment is self-contained to a directory tree you can make as many of
them as you like.

The ability to have many self-contained environments in userspace makes this
the "Goldilocks" level of isolation for many Python developers.  It is isolated
enough that you can have as many as you need, but it is not so isolated that you
need elevated privileges or additional technology to make it work.  Because of this
it has also seen the largest number an variety of tools around it.

One contentious axis is which tooling and packaging ecosystem to use to install
packages into your environment.  The three viable options are conda, wheel, and
spack.  Conda packages can reasonably be sourced either from conda-forge (for
community driven build) or the anaconda channel (for when you need a support
contract)[^dont-cross-the-streams].  The biggest downside of conda is that, like system package managers, not
all Python packages are necessarily built.


The module tooling on HPC systems is someplace between this and the previous
level.  Users are able to mix-and-match a combination of specific versions of
packages, typically tuned and compiled specifically to the machine you are
running on, and software they built themselves and cached.  The use of startup
scripts ensures that simulations run with a consistent set of dependencies
which are updated when the user, not the machine admins, decide it should be
updated.


It should be noted that system packaging tool is not the only option to provide
users on shared machines with read-only software.  With a bit of work you can
make the results of _any_ packaging tool read-only[^ro-conda] and use it to
provide a consistent environment to users on a shared system.


## monoliths

With user controlled environments there is always the notion of creating a
shared environment that can be used my multiple applications -- even if that is
not strictly the intent.  The next step up the ladder is to choose not to play
the game.  By bundling all of the dependencies into a single artifact


## bottom notes
https://pypackaging-native.github.io/




[^deps]: There are different kinds of depedencies:

    1. API compatibility in source
    2. ABI compatibility for built artifacts
    3. to-the-hilt pinning for reproducible deployments.

    In some cases, particularly with pure-Python projects, the first two can be elided
    together but in general need to be tracked independently and updated as part
    of the packaging process.
[^mu-system]: Multiuser systems are still extremely common in academia and
    resarch settings.  It is way simpler to set up a beefy machine and hand out
    access than almost anything else.  However, given that many operating
    systems use Python for their own internal tooling, most "single user"
    systems still have tow "users" who need run different software: the user
    and the system.  An example of this is [CITE HOMEBREW PYTHON IS NOT FOR
    YOU].
[^ro-conda]: At NSLS-II we use root-owned read-only [conda
    environments](https://github.com/nsls2-conda-envs) which are built on CI,
    packed via [`conda-pack`](https://conda.github.io/conda-pack/), published
    to [zenodo](https://zenodo.org/record/7470912), and then pulled to our
    system via automation.
[^named-versions]: You can sometimes get away with mangling the name (for
    example on my main desktop I have `python3.4`, `python3.5`, `python3.6`,
    `python3.7`, `python3.8`, `python3.9`, `python3.10`, `python3.11`,
    `python3.12` on my `$PATH` (thanks to the
    [AUR](https://aur.archlinux.org)), however this relies on calling a
    different binary to switch Python version.  This does not quite work for
    Python libraries as you do not want to find-and-replace every `import numpy
    as np` to `import numpy2 as np`!
[^cf-history]: Phil Ellison started working on conda-forge to install new
    versions of Matplotlib on RHEL systems.

[^intuitive]: "Intuitive" is inherently subjective and relies on the assumptions
    encoded into the tool matching your personal assumptions.  If your needs
    and assumptions are different than the tool makes then you may spend
    tremendous time and effort working around and against the tool.

[^meta]: Including this post!
[^pathhacking]: This can be done either by setting the `PYTHONPATH` environment
  variable before launching Python or from inside of a Python process by
  updating `sys.path`.
[^winpath]: The path works differently on Windows, just roll with the unix analogy.
[^package_chaos]: Python 3.10 will detect if it is being used in a virtual
  environment and not add users site-packages to the `PYTHONPATH`, however
  previously a `--user` installed package would be visible to all environments
  that shared the same Python version and take highest priority.  This was a very
  effective foot-cannon.
[^only-works-in-python]: however this can lead to entry-points installed at the
    system level -- such as `ipython` -- leaking through if the packages is not
    also installed in the environment.  This is a somewhat common bug that
    presents as "it works when I run it in as a script but not `ipython`".
[^dont-cross-the-streams]: Be very careful when trying to mix binaries from the
   default channels and conda-forge.  Because they are built with different
   build processes they are not guaranteed to be consistent with each other.
