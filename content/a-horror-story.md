Title: Why I am fanatical about version control
Date: 2022-05-09 23:00
Modified: 2022-05-09 23:51
Category: Software Development
Tags: software, git
Slug: how-i-learned-to-love-vcs
Authors: Thomas A Caswell
Summary: A short horror story that could have been prevented by git.
Status: published

So, there I was.  The year was 2007 and I was in the process of wrapping up the
research I had done as an undergraduate.  One of my tasks before heading off to
grad school was to archive all of the code I had written over the last two or
so years to [DVD-R](https://en.wikipedia.org/wiki/DVD%C2%B1R) for the lab
archive.

My [editor](https://www.gnu.org/software/emacs/) writes temporary backup copies
while editing to the filename with a `~` appended.  Thus, for ever source file
`foo.m` I had been working on there was a paired `foo.m~` in the directory as
well.  At the time I was working in MATLAB and as was the convention had all
off my source in one directory.  This was the code that I sued to generate the
figures in my senior thesis and, more critically, the figures of [a paper we
had in preparation](
https://www.sciencedirect.com/science/article/abs/pii/S0304399108003264) which
would require further revision.  Not wanting to archive transitory and
duplicate files I happily typed

```bash
cd all/of/my-source
rm * ~
```

which very efficiently deleted all of the code I had written over the last two
years ("Computers: making mistakes faster than you possibly imagined!").

I did want any reasonable person would do and spent the next five minutes lying
on the floor trying to stave off a panic attack.

In this particular case I was got stupendously lucky.  I had every file open in
an editor and was able to go through and systematically add a space and re-save
all of them.  From then on, everything I have written that looks like text that
I suspect I may want to keep is very quickly committed into a version control
system and distributed to at least two computers.
