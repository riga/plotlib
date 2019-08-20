# coding: utf-8

"""
Pre-configured ROOT plotting routines.
"""


__all__ = ["create_canvas", "create_top_left_label", "create_top_right_label", "create_cms_labels"]


import ROOT

from plotlib.root.styles import styles
from plotlib.root.tools import (
    get_canvas_pads, setup_canvas, setup_pad, setup_latex, get_pad_coordinates,
)
from plotlib.util import merge_dicts


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


def create_top_left_label(text, props=None, x=None, y=None):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("l", "t")
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    label = ROOT.TLatex(x, y, text)
    setup_latex(label, props)

    return label


def create_top_right_label(text, props=None, x=None, y=None):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("r", "t")
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    props = merge_dicts({"TextAlign": 31}, props)

    label = ROOT.TLatex(x, y, text)
    setup_latex(label, props)

    return label


def create_cms_labels(prefix="CMS", postfix="private work", x=None, y=None):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("l", "t", h_offset=0.005, v_offset=-0.005)
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    label1 = ROOT.TLatex(x, y, prefix)
    setup_latex(label1, {"TextFont": 63})

    label2 = ROOT.TLatex(x, y, "#font[63]{{{}}} {}".format(prefix, postfix))
    setup_latex(label2, {"TextFont": 53})

    return [label1, label2]
