# coding: utf-8

"""
Functional ROOT tools.
"""


__all__ = [
    "apply_properties", "calculate_legend_coords", "get_canvas_pads", "update_canvas",
    "setup_style", "setup_canvas", "setup_pad", "setup_x_axis", "setup_y_axis", "setup_z_axis",
    "setup_axes", "setup_latex", "setup_legend", "setup_hist", "setup_graph", "setup_line",
    "setup_box", "setup_func",
]


import ROOT
import six

from plotlib.util import merge_dicts
from plotlib.root.styles import styles


def apply_properties(obj, props, *_props):
    for name, value in six.iteritems(merge_dicts(props, *_props)):
        # determine the setter to invoke
        setter = getattr(obj, "Set{}".format(name), getattr(obj, name, None))
        if not callable(setter):
            continue

        # case 1: simple value, i.e., not a tuple
        if not isinstance(value, tuple):
            setter(value)

        # case 2: tuple
        else:
            setter(*value)


def calculate_legend_coords(n_entries, x1=None, x2=None, y2=None, dy=None):
    x1 = x1 if x1 is not None else styles.legend_x1
    x2 = x2 if x2 is not None else styles.legend_x2
    y2 = y2 if y2 is not None else styles.legend_y2
    dy = dy if dy is not None else styles.legend_dy

    y1 = y2 - dy * n_entries

    return (x1, y1, x2, y2)


def get_canvas_pads(canvas):
    return [
        p for p in canvas.GetListOfPrimitives()
        if isinstance(p, ROOT.TPad)
    ]


def update_canvas(canvas):
    for pad in get_canvas_pads(canvas):
        pad.RedrawAxis()
    ROOT.gPad.RedrawAxis()

    canvas.Update()


def setup_style(props=None):
    apply_properties(ROOT.gStyle, styles.style, props)


def setup_canvas(canvas, width=None, height=None, props=None):
    canvas.SetWindowSize(width or styles.canvas_width, height or styles.canvas_height)
    canvas.SetCanvasSize(width or styles.canvas_width, height or styles.canvas_height)
    apply_properties(canvas, styles.canvas, props)


def setup_pad(pad, props=None):
    apply_properties(pad, styles.pad, props)


def setup_x_axis(axis, pad, props=None):
    canvas_height = pad.GetCanvas().GetWindowHeight()

    _props = styles.axis.copy()

    # auto ticks
    pad_width = 1. - pad.GetLeftMargin() - pad.GetRightMargin()
    real_height = pad.YtoPixel(pad.GetY1()) - pad.YtoPixel(pad.GetY2())
    real_width = pad.XtoPixel(pad.GetX2()) - pad.XtoPixel(pad.GetX1())
    if pad_width != 0 and real_height != 0:
        _props["TickLength"] = styles.auto_ticklength / pad_width * real_width / real_height

    _props["TitleOffset"] = 1.075 * styles.canvas_height / canvas_height

    apply_properties(axis, _props, props)


def setup_y_axis(axis, pad, props=None):
    canvas_width = pad.GetCanvas().GetWindowWidth()

    _props = styles.axis.copy()

    _props["TitleOffset"] = 1.4 * styles.canvas_width / canvas_width

    # auto ticks
    pad_height = 1. - pad.GetTopMargin() - pad.GetBottomMargin()
    if pad_height != 0:
        _props["TickLength"] = styles.auto_ticklength / pad_height

    apply_properties(axis, _props, props)


def setup_z_axis(axis, pad, props=None):
    canvas_width = pad.GetCanvas().GetWindowWidth()

    _props = styles.axis.copy()

    _props["TitleOffset"] = 1.4 * styles.canvas_width / canvas_width

    apply_properties(axis, _props, props)


def setup_axes(obj, pad):
    for s, f in [("X", setup_x_axis), ("Y", setup_y_axis), ("Z", setup_z_axis)]:
        axis_getter = getattr(obj, "Get{}axis".format(s), None)
        if callable(axis_getter):
            # get the axis and set it up
            f(axis_getter(), pad)
        else:
            # we can stop here
            break


def setup_latex(latex, props=None):
    apply_properties(latex, styles.latex, props)


def setup_legend(legend, props=None):
    apply_properties(legend, styles.legend, props)


def setup_hist(hist, props=None):
    apply_properties(hist, styles.hist, props)


def setup_graph(graph, props=None):
    apply_properties(graph, styles.graph, props)


def setup_line(line, props=None):
    apply_properties(line, styles.line, props)


def setup_box(box, props=None):
    apply_properties(box, styles.box, props)


def setup_func(func, props=None):
    apply_properties(func, styles.func, props)
