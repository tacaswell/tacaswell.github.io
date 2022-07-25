Title: Building the Scientific Python stack from scratch
Date: 2022-07-03 23:00
Modified: 2022-07-03 23:00
Category: Software
Tags: main branch,
Slug: build-the-world
Authors: Thomas A Caswell
Summary: How to make the most unstable day-to-day Python environment.
Status: draft

If you develop software used by a reasonable number of people the line between
"bug" and "feature" can [become blurry](https://xkcd.com/1172/).  With enough
eyes all ~~bugs are shallow~~ implementation details are relied on and like all
library maintainers have been on both sides of the issue.

Way back in late 2017 I started to build the default branch of CPython (it is
actually not hard at all), create a `venv` from the executable and then try to
do may day-to-day development in that environment.  What started as a 42 line
bash "script" (it was actually just 42 commands in a file), has turned into [a
whole repo](https://github.com/tacaswell/build_the_world) of scripts and
metadata.  It now runs on both OSX (thanks to CZI I now have an M1 mac mini for
Matplotlib testing) and Linux.

The goal is less about being able to use new features of Python as soon as they
are available (as all of the projects I work on follow at least [NEP
29](https://numpy.org/neps/nep-0029-deprecation_policy.html)), but to catch any
unintentional changes in packages before they get released!  In that sense, the
project is working: it breaks about once a week.

Overall this projects has been quite a bit of fun.  It is good practice in
dropping into a code base you have _never_ seen before and isolating (and
sometimes fixing) a bug.

I am looking for anyone else who wants to participate in this project!
