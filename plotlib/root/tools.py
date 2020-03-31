# coding: utf-8

"""
Functional ROOT tools that retrieve and interact with existing ROOT objects, but do not create them.
"""


__all__ = [
    "apply_properties", "calculate_legend_coords", "get_canvas_pads", "update_canvas",
    "setup_style", "setup_canvas", "setup_pad", "setup_x_axis", "setup_y_axis", "setup_z_axis",
    "setup_axes", "setup_latex", "setup_legend", "setup_hist", "setup_graph", "setup_line",
    "setup_func", "setup_box", "setup_ellipse", "get_pad_coordinates", "fill_legend",
    "set_hist_value", "add_hist_value", "show_hist_underflow", "show_hist_overflow",
]


import math

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


def setup_x_axis(axis, pad, props=None, color=None, color_flags="l"):
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

    if color is not None:
        set_color(axis, color, flags=color_flags)


def setup_y_axis(axis, pad, props=None, color=None, color_flags="l"):
    canvas_width = pad.GetCanvas().GetWindowWidth()

    _props = styles.axis.copy()

    _props["TitleOffset"] = 1.4 * styles.canvas_width / canvas_width

    # auto ticks
    pad_height = 1. - pad.GetTopMargin() - pad.GetBottomMargin()
    if pad_height != 0:
        _props["TickLength"] = styles.auto_ticklength / pad_height

    apply_properties(axis, _props, props)

    if color is not None:
        set_color(axis, color, flags=color_flags)


def setup_z_axis(axis, pad, props=None, color=None, color_flags="l"):
    canvas_width = pad.GetCanvas().GetWindowWidth()

    _props = styles.axis.copy()

    _props["TitleOffset"] = 1.4 * styles.canvas_width / canvas_width

    apply_properties(axis, _props, props)

    if color is not None:
        set_color(axis, color, flags=color_flags)


def setup_axes(obj, pad, **kwargs):
    for s, f in [("X", setup_x_axis), ("Y", setup_y_axis), ("Z", setup_z_axis)]:
        axis_getter = getattr(obj, "Get{}axis".format(s), None)
        if callable(axis_getter):
            # get the axis and set it up
            f(axis_getter(), pad, **kwargs)
        else:
            # we can stop here
            break


def setup_latex(latex, props=None, color=None, color_flags="t"):
    apply_properties(latex, styles.latex, props)

    if color is not None:
        set_color(latex, color, flags=color_flags)


def setup_legend(legend, props=None, color=None, color_flags="lf"):
    apply_properties(legend, styles.legend, props)

    if color is not None:
        set_color(legend, color, flags=color_flags)


def setup_hist(hist, props=None, pad=None, color=None, color_flags="lmf"):
    apply_properties(hist, styles.hist, props)

    if pad is not None:
        setup_axes(hist, pad)

    if color is not None:
        set_color(hist, color, flags=color_flags)


def setup_graph(graph, props=None, color=None, color_flags="lm"):
    apply_properties(graph, styles.graph, props)

    if color is not None:
        set_color(graph, color, flags=color_flags)


def setup_line(line, props=None, color=None, color_flags="lm"):
    apply_properties(line, styles.line, props)

    if color is not None:
        set_color(line, color, flags=color_flags)


def setup_func(func, props=None, color=None, color_flags="l"):
    apply_properties(func, styles.func, props)

    if color is not None:
        set_color(func, color, flags=color_flags)


def setup_box(box, props=None, color=None, color_flags="lf"):
    apply_properties(box, styles.box, props)

    if color is not None:
        set_color(box, color, flags=color_flags)


def setup_ellipse(ellipse, props=None):
    apply_properties(ellipse, styles.ellipse, props)


def set_color(obj, color, flags="lmft"):
    funcs = {
        "l": ("SetLineColor",),
        "m": ("SetMarkerColor",),
        "f": ("SetFillColor",),
        "t": ("SetTextColor", "SetLabelColor"),
    }

    # color can be a string, translate it to a ROOT.k<Color>
    if isinstance(color, six.string_types):
        color = getattr(ROOT, "k" + color.capitalize())

    for flag in flags:
        if flag not in funcs:
            raise ValueError("flag '{}' is unknown".format(flag))

        for attr in funcs[flag]:
            func = getattr(obj, attr, None)
            if not callable(func):
                continue

            if isinstance(color, (tuple, list)):
                func(*color)
            else:
                func(color)


def get_pad_coordinates(h, v, offset=None, h_offset=None, v_offset=None):
    h_values = ("l", "c", "r")
    v_values = ("t", "c", "b")

    if h not in h_values:
        raise ValueError("unknown horizontal position '{}', allowed values are {}".format(
            h, h_values))

    if v not in v_values:
        raise ValueError("unknown vertical position '{}', allowed values are {}".format(
            v, v_values))

    if h_offset is None:
        h_offset = offset
    if h_offset is None:
        h_offset = 0. if h == "c" else 0.005

    if v_offset is None:
        v_offset = offset
    if v_offset is None:
        v_offset = 0. if v == "c" else 0.005

    # determine x and y position
    # the offset always points inwards, depending on the horizontal and vertical alignment
    if h == "l":
        x = styles.pad.LeftMargin + h_offset
    elif h == "c":
        x = (1. - styles.pad.RightMargin + styles.pad.LeftMargin) / 2. + h_offset
    else:  # "r":
        x = 1. - styles.pad.RightMargin - h_offset

    if v == "t":
        y = 1. - styles.pad.TopMargin - v_offset
    elif v == "c":
        y = (1. - styles.pad.TopMargin + styles.pad.BottomMargin) / 2. + v_offset
    else:  # "b"
        y = styles.pad.BottomMargin + v_offset

    return x, y


def fill_legend(legend, entries):
    """
    Fills *entries* into a TLegend *legend* with multiple columns in an intuitive fashion. ROOT's
    own implementation fills rows first while this implementation fills columns first. *entries*
    must be a list of objects that can be added as a legend entry or tuples ``(object, label)``.
    """
    n = len(entries)
    n_cols = legend.GetNColumns()
    n_rows = int(math.ceil(float(n) / n_cols))

    def get_text_width(text):
        tlatex = ROOT.TLatex(0, 0, text)
        tlatex.SetNDC()
        tlatex.SetTextFont(legend.GetTextFont() or ROOT.gStyle.GetTextFont())
        tlatex.SetTextSize(legend.GetTextSize() or ROOT.gStyle.GetTextSize())
        width = tlatex.GetXsize()
        del tlatex
        return width

    # prepare entries, store label widths
    widths = []
    for i, entry in enumerate(list(entries)):
        entry = list(entry) if isinstance(entry, (tuple, list)) else [entry]
        if len(entry) == 1:
            entry.append("")
        entry[1] = entry[1] or entry[0].GetTitle() or entry[0].GetName()
        entries[i] = entry
        widths.append(get_text_width(entry[1]))

    # fill labels with spaces to ensure every label has the same width
    max_width = max(widths)
    space_width = get_text_width(" ")
    for entry, width in zip(entries, widths):
        entry[1] += " " * int(math.floor((max_width - width) / float(space_width)))
    empty_label = " " * int(math.floor(max_width / float(space_width)))

    # loop in a "transposed" order
    for i in range(n_rows):
        for j in range(n_cols):
            idx = i + n_rows * j
            if idx < n:
                entry = entries[idx]
            else:
                entry = (entries[n - 1][0], empty_label, "")
            legend.AddEntry(*entry)


def set_hist_value(hist, i, value, err=None, err2=None):
    hist.SetBinContent(i, value)

    if hist.GetSumw2N() != 0:
        if err2 is None and err is not None:
            err2 = err**2.
        if err2 is not None:
            hist.GetSumw2()[i] = err2


def add_hist_value(hist, i, value, err=None, err2=None):
    if err2 is None and err is not None:
        err2 = err**2.
    update_err = hist.GetSumw2N() != 0 and err2 is not None

    if update_err:
        w2 = hist.GetSumw2()[i]

    hist.AddBinContent(i, value)

    if update_err:
        hist.GetSumw2()[i] = w2 + err2


def show_hist_underflow(hist, clear=True):
    """
    Adds the total underflow of a histogram *hist* to the first bin and propagates errors properly.
    When *clear* is *True*, the underflow is set to 0.
    """
    underflow = hist.GetBinContent(0)
    if underflow == 0:
        return

    err2 = None if hist.GetSumw2N() == 0 else hist.GetSumw2()[0]
    add_hist_value(hist, 1, underflow, err2=err2)

    if clear:
        set_hist_value(hist, 0, 0., err2=0.)


def show_hist_overflow(hist, clear=True):
    """
    Adds the total overflow of a histogram *hist* to the last bin and propagates errors properly.
    When *clear* is *True*, the overflow is set to 0.
    """
    n_bins = hist.GetNbinsX()
    overflow = hist.GetBinContent(n_bins + 1)
    if overflow == 0:
        return

    err2 = None if hist.GetSumw2N() == 0 else hist.GetSumw2()[n_bins + 1]
    add_hist_value(hist, n_bins, overflow, err2=err2)

    if clear:
        set_hist_value(hist, n_bins + 1, 0., err2=0.)
