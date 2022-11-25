Title: Reflowing Axes
Date: 2022-11-25 22:00
Modified: 2022-11-25 22:00
Category: Matplotlib
Tags: Matplotlib generator
Slug: dynamic-axes-count
Authors: Thomas A Caswell
Summary: Dynamically adding Axes to a Figure
Status: published


At the prompting of a user on Matplotlib's gitter channel I wrote the following
example:

```python
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from matplotlib.gridspec import GridSpec


def reflow_gen(fig):
    # we own this figure now so clear it
    fig.clf()
    # running count of the number of axes
    axcount = count(1)

    # the shape of the grid
    row_guess = col_guess = 0
    # the current GridSpec object
    gs = None

    # we are a generator, so loop forever
    while True:
        # what number is this Axes?
        j = next(axcount)
        # do we need to re-flow?
        if j > row_guess * col_guess:
            # Find the smallest square that will work
            col_guess = row_guess = int(np.ceil(np.sqrt(j)))
            # and then drop fully empty rows
            for k in range(1, row_guess):
                if (row_guess - 1) * col_guess < j:
                    break
                else:
                    row_guess -= 1

            # Create the new gridspec object
            gs = GridSpec(row_guess, col_guess, figure=fig)

            # for each of the axes, adjust it to use the new gridspec
            for n, ax in enumerate(fig.axes):
                ax.set_subplotspec(gs[*np.unravel_index(n, (row_guess, col_guess))])
            # resize the figure to have ~ 3:4 ratio and keep the Axes fixed
            fig.set_size_inches(col_guess * 4, row_guess * 3)

        # Add the new axes to the Figure at the next open space
        new_ax = fig.add_subplot(gs[*np.unravel_index(j - 1, (row_guess, col_guess))])

        # hand the Axes back to the user
        yield new_ax

# make a Figure
fig = plt.figure(layout='constrained')
# set up the generator
ax_gen = reflow_gen(fig)
for j in range(5):
    # get an Axes
    ax = next(ax_gen)
    ax.set_title(f'Axes {j}')
    # fig.savefig(f'dynamic_axes_figs-axes_{j}.svg')
plt.show()

```

**1 axes (1x1)**

![Figure with 1 Axes added](/images/dynamic_axes_figs-axes_0.svg "1 Axes")

**2 axes (2x1)**

![Figure with 2 Axes added](/images/dynamic_axes_figs-axes_1.svg "2 Axes")

**3 axes (2x2)**

![Figure with 3 Axes added](/images/dynamic_axes_figs-axes_2.svg "3 Axes")

**4 axes (2x2)**

![Figure with 4 Axes added](/images/dynamic_axes_figs-axes_3.svg "4 Axes")

**5 axes (3x2)**

![Figure with 5 Axes added](/images/dynamic_axes_figs-axes_4.svg "5 Axes")

and so on up to as many *Axes* as you want to add.  Note that the Figure is
getting bigger as more Axes are added so if using this interactively the window
will grow.

I am not sure that this is general enough to add to Matplotlib, but it is a
cute example of how generators can be useful.  One concern with this code is
that the generator will keep the *Figure* object alive which may complicate
resource management.  There are also some questions for me about what the API
should be.  As written the resizing and target aspect ratio behavior is fixed,
I think it is reasonable for users to be able to control both.  Additional, the
scheme for growing the grid and selecting which slots to fill at a given grid
size and fill factor could be elaborated.  It might also be interesting to
promote the generator to a full [generator
co-routine]({filename}practical-coroutines.md) to be able to pass arguments the Axes
creation step (to set projections and such).
