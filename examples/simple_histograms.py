# coding: utf-8

"""
Creates simple histograms and a legend.
"""


import os
import random

import plotlib.root as r
import ROOT


# setup the general style and create canvas and pad
r.setup_style()
canvas, (pad,) = r.routines.create_canvas()
pad.cd()

# create the two histograms
h1 = ROOT.TH1F("h1", ";x;y", 40, 0., 1.)
h2 = ROOT.TH1F("h2", ";x;y", 40, 0., 1.)

# fill with two gaussians
for _ in range(1000):
    h1.Fill(random.gauss(mu=0.33, sigma=0.05))
    h2.Fill(random.gauss(mu=0.67, sigma=0.1))

# setup the style of the histograms and the axes of the first one
r.setup_hist(h1, props={"LineColor": 2})
r.setup_hist(h2, props={"LineColor": 4})
r.setup_axes(h1, pad)

# create the legend, create the coordiations via the number of entries
# and the vertical distance between them
legend = ROOT.TLegend(*r.calculate_legend_coords(2, dy=0.075))
r.setup_legend(legend)
legend.AddEntry(h1, "Histogram 1")
legend.AddEntry(h2, "Histogram 2")

# draw everything
h1.Draw()
h2.Draw("SAME")
legend.Draw()

# update and save
r.update_canvas(canvas)
canvas.SaveAs("histograms.pdf")

# now, we want to use a different style for the second histogram
# this might seem overly complicated for this trivial example, but
# for sophisticated plots, style switching is really helpful

# we start by copying the default style
# (this would normally happen in a different, perhaps centralized file)
my_style = r.styles.copy("default", "my_style")

# update the histogram fill style
my_style.hist.FillStyle = 3444

# setup the second histogram again, but this time use the new style
with r.styles.use("my_style"):
    # the color attribute sets line, marker and fill color by default
    # see tools.set_color for more info
    r.setup_hist(h2, color=4)

# update and save again
r.update_canvas(canvas)
canvas.SaveAs("histograms2.pdf")
