# coding: utf-8

"""
Default ROOT style.
"""


__all__ = []


from plotlib.util import DotDict, Styles
from plotlib.root import ROOT
from plotlib.root.styles import styles


# configure common values of the default style
style = styles.set(Styles.DEFAULT_STYLE_NAME, DotDict(
    canvas_width=800,
    canvas_height=640,
    text_size=22,
    auto_ticklength=0.015,
    legend_x1_margin=0.55,
    legend_x2_margin=0.02,
    legend_y2_margin=0.02,
    legend_dy=0.045,
    # legacy values used in deprecated calculate_legend_coords_old method, to be removed
    legend_x1=0.68,
    legend_x2=0.96,
    legend_y2=0.92,

))

# colors
style.colors = DotDict(
    black=ROOT.kBlack,
    blue=ROOT.kBlue + 1,
    red=ROOT.kRed - 4,
    magenta=ROOT.kMagenta + 1,
    yellow=ROOT.kOrange - 2,
    green=ROOT.kGreen + 2,
    brightgreen=ROOT.kGreen - 3,
    darkgreen=ROOT.kGreen + 4,
    creamblue=38,
    creamred=46,
    white=10,
)

# gStyle
style.style = DotDict(
    OptStat=0,
)

# TCanvas
style.canvas = DotDict(
    TopMargin=0,
    RightMargin=0,
    BottomMargin=0,
    LeftMargin=0,
    FillStyle=1001,
    # FillStyle=4000,  # transparent
)

# TPad
style.pad = DotDict(
    Pad=(0, 0, 1, 1),
    TopMargin=0.05,
    RightMargin=0.03,
    BottomMargin=0.105,
    LeftMargin=0.13,
    FillStyle=4000,
    Ticks=(True, True),
)

# TAxis, x
style.x_axis = DotDict(
    TitleFont=43,
    TitleSize=25,
    LabelFont=43,
    LabelSize=style.text_size,
)

# TAxis, second x axis at the top when needed
style.x2_axis = DotDict(
    TitleFont=43,
    TitleSize=25,
    LabelFont=43,
    LabelSize=style.text_size,
    TickLength=0.,
    LabelOffset=-0.025,
    TitleOffset=-1.2,
    DrawOption="S",
)

# TAxis, y
style.y_axis = DotDict(
    TitleFont=43,
    TitleSize=25,
    LabelFont=43,
    LabelSize=style.text_size,
)

# TAxis, z
style.z_axis = DotDict(
    TitleFont=43,
    TitleSize=25,
    TitleOffset=0.7,
    LabelFont=43,
    LabelSize=style.text_size,
)

# TLatex
style.latex = DotDict(
    TextFont=43,
    TextSize=style.text_size,
    TextAlign=11,
    NDC=True,
)

# TLegend
style.legend = DotDict(
    BorderSize=0,
    FillStyle=0,
    FillColor=0,
    LineStyle=0,
    LineColor=0,
    LineWidth=0,
    TextFont=43,
    TextSize=style.text_size,
    ColumnSeparation=0.,
)

# TH{1,2,3}
style.hist = DotDict(
    LineWidth=2,
    LineColor=1,
    MarkerColor=1,
)

# TGraph
style.graph = DotDict(
    LineColor=1,
    LineWidth=2,
    FillColor=0,
    MarkerStyle=10,
    MarkerColor=1,
)

# TLine
style.line = DotDict(
    LineWidth=2,
    LineColor=1,
    NDC=True,
)

# TBox
style.box = DotDict(
    LineWidth=2,
    LineColor=1,
    FillColor=0,
)

# TF{1,2,3}
style.func = DotDict(
    LineWidth=2,
    LineColor=1,
)

# TEllipse
style.ellipse = DotDict(
    LineWidth=1,
    LineColor=1,
)
