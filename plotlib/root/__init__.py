# coding: utf-8
# flake8: noqa

"""
ROOT-related plotting helpers.
"""


__all__ = []


import os

import ROOT


# configure the global ROOT behavior
ROOT.PyConfig.IgnoreCommandLineOptions = True
if os.getenv("PLOTLIB_ROOT_BATCH", "").lower() in ("1", "yes", "true"):
    ROOT.gROOT.SetBatch()


# provisioning imports
from plotlib.root.styles import *
from plotlib.root.tools import *
import plotlib.root.routines
