Title: How this site is maintained and published
Date: 2022-07-03 22:00
Modified: 2022-07-03 22:00
Category: Navel Gazing
Tags: hosting
Slug: tech-details
Authors: Thomas A Caswell
Summary: A good and proper navel gaze.
Status: published

**Hosting**

Both the [source](https://github.com/tacaswell/tacaswell.github.io) and built
artifacts for this site are hosted on GitHub (via [github pages](https://pages.github.com)).

It is possible to have a public gh-pages site with a private repository backing
it, however I have opted to have both public.  This has the upsides that I can
[get PRs from
others](https://github.com/tacaswell/tacaswell.github.io/pulls?q=is%3Apr+is%3Aclosed)
and that it is easier for other people to adapt this set up for their own use.
A slight downside is that the history of my edits is visible, including for
draft posts.  I expect this to only be an issue if I write about any sensitive
topics where I do not want to make my full writing process public (I'm all for
openness and working in public, but even I have limits).


**Framework**

This site is written within the [Pelican](http://getpelican.com) framework.

I did not do exhaustive research to pick Pelican (but it does well in a google
search for "python static site generator"), however it is in Python (hopefully
I won't have to dig into the guts, but nice to know I can if I have/want to),
generates static html (needed for gh-pages hosting), and supports both markdown
and rst out-of-the-box.

The other framework I considered was
[Sphinx](https://www.sphinx-doc.org/en/master/).  I work with Sphinx almost
every day for writing documentation, so it is a tool I know.  However, I wanted
both wanted to try a new tool and to use tool more tuned to blog
out-of-the-box.

**Theme**

The theme is base on [Blue
Penguin](https://github.com/jody-frankowski/blue-penguin) which is licensed
Public Domain.  Knowing that I was going to use GHA to build and publish the
site, the theme is simply [checked
into](https://github.com/tacaswell/tacaswell.github.io/tree/main/themes/blue-penguin)
the source.  I have modified a number of things, in particular the styling
around code snippets, the base colors, and fonts (with considerable help from
my wife).

If anyone else wants to use these modifications, I would be willing to split it
off into its own repo (and use git submodules), but doing that up front seems
like premature optimization.

The theme is selected via the `PELICANOPTS=-t $(BASEDIR)/themes/blue-penguin`
line in the
[Mkaefile](https://github.com/tacaswell/tacaswell.github.io/blob/3e2507fdb3812f3c74cf3076a4e037a07e1c9b7f/Makefile#L10).

**Build Pipeline**

To publish the built artifacts, I use a [GHA
workflow](https://github.com/tacaswell/tacaswell.github.io/blob/main/.github/workflows/publish.yml)
and the amazingly awesome [gh-pages action](
https://github.com/peaceiris/actions-gh-pages) from
[peaciris](https://github.com/peaceiris).
