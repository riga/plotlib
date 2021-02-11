# coding: utf-8

"""
Pre-configured ROOT plotting routines that create and return objects.
"""


__all__ = [
    "create_object", "create_canvas", "create_legend", "create_legend_box", "create_top_left_label",
    "create_top_right_label", "create_cms_labels", "draw_objects",
]


import ROOT

from plotlib.root.styles import styles
from plotlib.root.tools import (
    get_canvas_pads, setup_canvas, setup_pad, setup_latex, setup_legend, setup_box, get_xy,
    calculate_legend_coords,
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


def create_legend(*args, **kwargs):
    props = kwargs.pop("props", {})

    # pass all arguments to the position calculation and create the legend
    legend = create_object("TLegend", *calculate_legend_coords(*args, **kwargs))
    setup_legend(legend, props=props)

    return legend


def create_legend_box(legend, pad, mode="", x1=None, x2=None, y1=None, y2=None, padding=0,
        x_padding=None, x1_padding=None, x2_padding=None, y_padding=None, y1_padding=None,
        y2_padding=None, props=None):
    # determine the padding
    if x1_padding is None:
        x1_padding = padding if x_padding is None else x_padding
    if x2_padding is None:
        x2_padding = padding if x_padding is None else x_padding
    if y1_padding is None:
        y1_padding = padding if y_padding is None else y_padding
    if y2_padding is None:
        y2_padding = padding if y_padding is None else y_padding

    if x1 is None:
        x1 = pad.GetLeftMargin() if "l" in mode else (legend.GetX1() - x1_padding)
    if x2 is None:
        x2 = (1 - pad.GetRightMargin()) if "r" in mode else (legend.GetX2() + x2_padding)
    if y1 is None:
        y1 = pad.GetBottomMargin() if "b" in mode else (legend.GetY1() - y1_padding)
    if y2 is None:
        y2 = (1 - pad.GetTopMargin()) if "t" in mode else (legend.GetY2() + y2_padding)

    # create the box
    box = create_object("TPave", x1, y1, x2, y2, 0, "NDC")
    setup_box(box, props=props)

    return box


def create_top_left_label(text, x=None, y=None, pad=None, props=None, **kwargs):
    # default position
    kwargs.setdefault("x_anchor", "left")
    kwargs.setdefault("y_anchor", "top")
    x_default, y_default = get_xy(2, -6, pad, **kwargs)
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    # default props
    props = merge_dicts({"TextAlign": 11}, props)

    # create and setup the label
    label = create_object("TLatex", x, y, text)
    setup_latex(label, props)

    return label


def create_top_right_label(text, x=None, y=None, pad=None, props=None, **kwargs):
    # default position
    kwargs.setdefault("x_anchor", "right")
    kwargs.setdefault("y_anchor", "top")
    x_default, y_default = get_xy(2, -6, pad, **kwargs)
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    # default props
    props = merge_dicts({"TextAlign": 31}, props)

    # create and setup the label
    label = create_object("TLatex", x, y, text)
    setup_latex(label, props)

    return label


def create_cms_labels(prefix="CMS", postfix="Preliminary", x=None, y=None, pad=None, **kwargs):
    # default position
    kwargs.setdefault("x_anchor", "left")
    kwargs.setdefault("y_anchor", "top")
    x_default, y_default = get_xy(2, -6, pad, **kwargs)
    if x is None:
        x = x_default
    if y is None:
        y = y_default

    # create the labels
    label1 = create_object("TLatex", x, y, prefix)
    label2 = create_object("TLatex", x, y, "#font[63]{{{}}} {}".format(prefix, postfix))
    setup_latex(label1, {"TextFont": 63})
    setup_latex(label2, {"TextFont": 53})

    return [label1, label2]


def draw_objects(objs):
    for obj in objs:
        if getattr(obj, "Draw", None) is None and callable(obj):
            obj()
        elif isinstance(obj, tuple) and len(obj) == 2:
            obj[0].Draw(obj[1])
        else:
            obj.Draw()
