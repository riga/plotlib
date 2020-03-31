# coding: utf-8

"""
Pre-configured ROOT plotting routines that create and return objects.
"""


__all__ = [
    "create_object", "create_canvas", "create_top_left_label", "create_top_right_label",
    "create_cms_labels",
]


import ROOT

from plotlib.root.styles import styles
from plotlib.root.tools import (
    get_canvas_pads, setup_canvas, setup_pad, setup_latex, get_pad_coordinates,
)
from plotlib.util import merge_dicts, create_random_name


object_cache = []


def create_object(cls_name, *args, **kwargs):
    """
    Creates and returns a new ROOT object, constructed via ``ROOT.<cls_name>(*args, **kwargs)`` and
    puts it in an object cache to prevent it from going out-of-scope given ROOTs memory management.
    """
    obj = getattr(ROOT, cls_name)(*args, **kwargs)
    object_cache.append(obj)
    return obj


def create_canvas(name=None, title=None, width=None, height=None, divide=(1,), props=None,
        pad_props=None):
    if not name:
        name = create_random_name("canvas")

    title = title if title is not None else name
    width = width if width is not None else styles.canvas_width
    height = height if height is not None else styles.canvas_height

    canvas = create_object("TCanvas", name, title, width, height)
    canvas.Divide(*divide)
    setup_canvas(canvas, width, height, props)

    pads = get_canvas_pads(canvas)
    for pad in pads:
        setup_pad(pad, pad_props)

    return canvas, pads


def create_top_left_label(text, props=None, x=None, y=None, **kwargs):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("l", "t", **kwargs)
    if x is None:
        x = x_default
    if y is None:
        y = y_default + 0.01

    label = create_object("TLatex", x, y, text)
    setup_latex(label, props)

    return label


def create_top_right_label(text, props=None, x=None, y=None, **kwargs):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("r", "t", **kwargs)
    if x is None:
        x = x_default
    if y is None:
        y = y_default + 0.01

    props = merge_dicts({"TextAlign": 31}, props)

    label = create_object("TLatex", x, y, text)
    setup_latex(label, props)

    return label


def create_cms_labels(prefix="CMS", postfix="private work", x=None, y=None):
    # determine defaults based on the current style
    x_default, y_default = get_pad_coordinates("l", "t", v_offset=-0.005)
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    label1 = create_object("TLatex", x, y, prefix)
    setup_latex(label1, {"TextFont": 63})

    label2 = create_object("TLatex", x, y, "#font[63]{{{}}} {}".format(prefix, postfix))
    setup_latex(label2, {"TextFont": 53})

    return [label1, label2]
