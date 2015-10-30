# -*- coding: utf-8 -*-

__author__ = 'malte'

from math import floor, ceil
from itertools import cycle, islice
import textwrap

from curtsies import FSArray, fmtstr
from curtsies.formatstring import xforms


from .characters import *

def maybe(x, default, y=None):
    if x is None:
        return default
    elif y is None:
        return x
    else:
        return y

def repeat(text, length):
    return u''.join(list(islice(cycle(text), 0, length)))

def v_repeat(text, length):
    return list(islice(cycle(text), 0, length))

def center(text, width, space=u' '):
    length = len(text)
    remaining = width-length

    if remaining >= 0:
        lspace = floor(remaining/2.0)
        rspace = ceil(remaining/2.0)
        return repeat(space, lspace) + text + repeat(space, rspace)
    elif width > 1:
        return text[:width-1] + u"…"
    else:
        return text[0:1]

def fill(text, width, space=u' '):
    length = len(text)
    remaining = width-length

    if remaining >= 0:
        text + repeat(space, remaining)
    elif width > 1:
        return text[:width-1] + u"…"
    else:
        return text[0:1]

def indent(text, width, space=u' '):
    length = len(text)
    remaining = width-length

    if remaining >= 0:
        repeat(space, remaining) + text
    elif width > 1:
        return text[:width-1] + u"…"
    else:
        return text[0:1]

def pad(text, padding=1, space=u' '):
    if isinstance(padding, tuple):
        return repeat(space, padding[0]) + text + repeat(space, padding[1])

    return repeat(space, padding) + text + repeat(space, padding)

def header(text, width, padding=1, bar=light_horizontal, left=u'[', right=u']'):
    return center(left + pad(text, padding) + right, width, space=bar)

def wrap(text, width, height=None, text_fmt=lambda x: x):
    lines = textwrap.wrap(text, width)

    if height is None:
        height = len(lines)

    fsa = FSArray(height, width)

    if height > len(lines):
        height = len(lines)

    fsa[0:height, 0:width] = map(text_fmt, lines[0:height])
    return fsa

def tabular(rows, width, height=None, col_widths=None, col_sep=None, row_heights=None, row_sep=None, cell_wrap=False):
    # Convert each row into a list of FSAs considering optional row_heights and col_widths
        # If no col_widths are given estimate by content lengths
    # Trim cols and rows that do not fit into width and height with separators
    # Generate joint FSA
    pass

def fmtfsa(fsa, **kwargs):
    o_fsa = FSArray(fsa.height, fsa.width)
    for y in range(fsa.height):
        raw = map(lambda x: fmtstr(x.new_with_atts_removed(xforms.keys()), **kwargs), fsa[y:y+1, 0:fsa.width])
        o_fsa[y:y+1, 0:o_fsa.width] = raw
    return o_fsa

def box(c_fsa,
        spacing=0,
        v_bar=light_vertical,
        h_bar=light_horizontal,
        ul_corner=light_down_and_right,
        ur_corner=light_down_and_left,
        ll_corner=light_up_and_right,
        lr_corner=light_up_and_left,
        left=u'[',
        right=u']',
        title=None,
        border_fmt=lambda x: x):
    w = c_fsa.width
    h = c_fsa.height

    bw = w + 2*spacing + 2
    bh = h + 2*spacing + 2

    b_fsa = FSArray(bh, bw)

    b_fsa[0, 0] = border_fmt(ul_corner)
    b_fsa[bh-1, 0] = border_fmt(ll_corner)
    b_fsa[0, bw-1] = border_fmt(ur_corner)
    b_fsa[bh-1, bw-1] = border_fmt(lr_corner)

    b_fsa[1:bh-1, 0:1] = map(border_fmt, v_repeat(v_bar, bh-2))
    b_fsa[1:bh-1, bw-1:bw] = map(border_fmt, v_repeat(v_bar, bh-2))

    b_fsa[0:1, 1:bw-1] = [border_fmt(repeat(h_bar, bw-2))]
    b_fsa[bh-1:bh, 1:bw-1] = [border_fmt(repeat(h_bar, bw-2))]

    if title is not None:
        b_fsa[0:1, 1:bw-1] = [border_fmt(header(title, bw-2, bar=h_bar, left=left, right=right))]

    blit(b_fsa, c_fsa, 1+spacing, 1+spacing, w, h)
    return b_fsa


def blit(tgt, src, x=0, y=0, w=None, h=None):
    tw = tgt.width
    th = tgt.height
    sw = src.width
    sh = src.height

    if w is not None and w < sw:
        sw = w
    if h is not None and h < sh:
        sh = h

    sx = -min(0, x)
    sy = -min(0, y)
    tx = max(0, x)
    ty = max(0, y)

    if x+sw <= tw:
        w = sx + sw
    else:
        w = -sx + tw - x

    if y+sh <= th:
        h = sx + sh
    else:
        h = -sy + th - y

    tgt[ty:ty+h, tx:tx+w] = src[sy:sy+h, sx:sx+w]