# coding: utf-8
# flake8: noqa

"""
Definition of ROOT styles.
"""


__all__ = ["styles"]


from plotlib.util import Styles


# create the global styles object
styles = Styles()


# import styles
import plotlib.root.styles.default
