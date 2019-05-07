# coding: utf-8

"""
Pre-configured ROOT plotting routines.
"""


__all__ = ["create_canvas", "create_cms_labels"]


import ROOT

from plotlib.root.styles import styles
from plotlib.root.tools import get_canvas_pads, setup_canvas, setup_pad, setup_latex


def create_canvas(name="canvas", title=None, width=None, height=None, divide=(1,)):
    title = title if title is not None else name
    width = width if width is not None else styles.canvas_width
    height = height if height is not None else styles.canvas_height

    canvas = ROOT.TCanvas(name, title, width, height)
    canvas.Divide(*divide)
    setup_canvas(canvas, width, height)

    pads = get_canvas_pads(canvas)
    for pad in pads:
        setup_pad(pad)

    return canvas, pads


def create_cms_labels(prefix="CMS", postfix="private work", x=0.135, y=0.96):
    label1 = ROOT.TLatex(x, y, prefix)
    setup_latex(label1, {"TextFont": 73})

    label2 = ROOT.TLatex(x, y, "#font[73]{{{}}} {}".format(prefix, postfix))
    setup_latex(label2)

    return [label1, label2]
