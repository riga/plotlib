# coding: utf-8

"""
Helpful utilities.
"""


__all__ = ["DotDict", "Styles", "merge_dicts", "create_random_name"]


import copy
import contextlib
import uuid


class DotDict(dict):
    """
    Dictionary with attribute access. Example:

    .. code-block:: python

        d = DotDict(a="foo", b="bar")

        print(d.a)     # -> "foo"
        print(d["a"])  # -> "foo"

        d.b = "baz"
        print(d.b)     # -> "baz"
        print(d["b"])  # -> "baz"

    By default, dictionaries raise :py:class:`KeyError`'s in case a requested item does not exist.
    When an item is requested via attribute, this class raises an :py:class:`AttributeError` to be
    consistent to Python's internal mechanism for checking the existence of attributes via
    ``hasattr``.
    """

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __setattr__(self, attr, value):
        self[attr] = value

    def copy(self):
        return self.__class__(super(DotDict, self).copy())


class Styles(object):
    """
    Class to handle different collections of styles, which are represented and stored internally as
    dictionaries. The main purpose is to store various styles mapped to different names, which can
    be changed my manipulating the internal stack of currently used styles. They can be changed via
    :py:meth:`push` and :py:meth:`pop`, or within contexts using :py:meth:`use`. Example:

    .. code-block:: python

        from copy import deepcopy
        import plotlib as pl
        import plotlib.root

        styles = r.Styles()

        # get the default style
        style = styles.get(styles.DEFAULT_STYLE_NAME)

        # configure canvas styles
        style.canvas = DotDict(
            TopMargin=0,
            RightMargin=0,
            BottomMargin=0,
            LeftMargin=0,
            FillStyle=1001,
        )

        # now, create a "publication" style and change the fill style to transparent
        pub_style = styles.set("publication", deepcopy(style))
        pub_style.canvas.FillStyle = 4000

        # apply to a ROOT.TCanvas
        canvas = ROOT.TCanvas()

        with styles.use("publication"):
            r.setup_canvas(canvas, styles.canvas)

        # or manually via push & pop
        styles.push("publication")
        r.setup_canvas(canvas, styles.canvas)
        styles.pop("publication")

        # continue plotting
        ...

    .. py:attribute:: DEFAULT_STYLE_NAME
       classmember
       type: str

       The name of the default style, which is ``"default"`` initially.

    .. py:attribute:: current_style_name
       read-only
       type: str

       The name of the currently used style, i.e., the last element in the stack of style names, or
       the :py:attr:`DEFAULT_STYLE_NAME` when empty.

    .. py:attribute:: current_style
       read-only
       type: dict

       The style dict that :py:attr:`current_style_name` refers to.
    """

    DEFAULT_STYLE_NAME = "default"

    def __init__(self):
        super(Styles, self).__init__()

        self._styles = {}
        self._stack = []

        # register a DotDict for the default style
        self.set(self.__class__.DEFAULT_STYLE_NAME, DotDict())

    def __getattr__(self, attr):
        """
        Returns the attribute *attr* of the :py:attr:`current_style`.
        """
        return getattr(self.current_style, attr)

    @property
    def current_style_name(self):
        if self._stack:
            return self._stack[-1]
        else:
            return self.DEFAULT_STYLE_NAME

    @property
    def current_style(self):
        return self.get(self.current_style_name)

    def get(self, style_name):
        """
        Returns a style dict defined previously by *style_name*.
        """
        return self._styles[style_name]

    def set(self, style_name, style):
        """
        Sets the style dict for *style_name* to *style*. If the latter is not a dictionary, a
        :py:class:`TypeError` is raised. *style* is returned.
        """
        if not isinstance(style, dict):
            raise TypeError("wrong style type '{}', must be a dict".format(style.__class__))

        self._styles[style_name] = style

        return style

    def copy(self, src_style_name, dst_style_name):
        """
        Creates a deep copy of the style defined by *src_style_name*, stores it as *dst_style_name*
        and returns the copied style dictionary.
        """
        style = copy.deepcopy(self.get(src_style_name))
        return self.set(dst_style_name, style)

    def push(self, style_name):
        """
        Appends *style_name* to the stack of currently used styles.
        """
        if style_name not in self._styles:
            raise ValueError("cannot use unknown style '{}'".format(style_name))

        self._stack.append(style_name)

    def pop(self):
        """
        Removes the last element from the stack of currently used styles and returns the removed
        element.
        """
        return self._stack.pop()

    @contextlib.contextmanager
    def use(self, style_name):
        """
        Sets the currently used style to the one defined by *style_name*. Internally, the name is
        added to the stack of style names, so that :py:attr:``
        """
        self.push(style_name)
        try:
            yield self.get(style_name)
        finally:
            self.pop()


def merge_dicts(*dicts, **kwargs):
    """ merge_dicts(*dicts, cls=None)
    Takes multiple *dicts* and returns a single merged dict. The merging takes place in order of the
    passed dicts and therefore, values of rear objects have precedence in case of field collisions.
    The class of the returned merged dict is configurable via *cls*. If it is *None*, the class is
    inferred from the first dict object in *dicts*.
    """
    # get or infer the class
    cls = kwargs.get("cls", None)
    if cls is None:
        for d in dicts:
            if isinstance(d, dict):
                cls = d.__class__
                break
        else:
            raise TypeError("cannot infer cls as none of the passed objects is of type dict")

    # start merging
    merged_dict = cls()
    for d in dicts:
        if isinstance(d, dict):
            merged_dict.update(d)

    return merged_dict


def create_random_name(prefix="", l=8):
    """
    Creates and returns a random name string consisting of *l* characters using uuid4 internally.
    When *prefix* is given, the name will have the format ``<prefix>_<random_name>``.
    """
    name = uuid.uuid4().hex[:l]
    if prefix:
        name = "{}_{}".format(prefix, name)
    return name
