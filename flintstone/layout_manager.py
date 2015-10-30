from curtsies import FullscreenWindow, FSArray
from .utils import maybe, blit

__author__ = 'malte'


class LayoutManager(object):
    def __init__(self, owner=None):
        if isinstance(owner, FullscreenWindow):
            self.window = owner
            self.owner = None
        elif owner is None:
            self.window = None
            self.owner = None
        else:
            raise RuntimeError("The owner has to be a FullscreenWindow or a Widget")

        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def tangible_widgets(self):
        return filter(lambda x: x.tangible, self.widgets)

    def visible_widgets(self):
        return filter(lambda x: x.visible and x.tangible, self.widgets)

    def render(self):
        if self.owner is None:
            width = self.window.width
            height = self.window.height
        else:
            width = self.owner.width
            height = self.owner.height

        lm_fsa = FSArray(height, width)
        self.render_into_rect(lm_fsa)

        if self.owner is None:
            self.window.render_to_terminal(lm_fsa)

        return lm_fsa

    def render_into_rect(self, lm_fsa):
        width = lm_fsa.width
        height = lm_fsa.height

        y_offset = 0
        for w in self.widgets:
            fsa = w.render(max_width=width, max_height=height)
            blit(lm_fsa, fsa, y_offset)
            y_offset += fsa.height


class HStackLayout(LayoutManager):
    def render_into_rect(self, lm_fsa):
        width = lm_fsa.width
        height = lm_fsa.height

        heights = map(lambda w: w.height, self.tangible_widgets())
        total_height = reduce(lambda x, y: maybe(y, 0) + x, heights, 0)
        undef_heights = reduce(lambda x, y: maybe(y, 1, 0) + x, heights, 0)
        remaining_height = height - total_height

        y_offset = 0

        for wgt in self.tangible_widgets():
            h = wgt.height
            if h is None:
                h = remaining_height/undef_heights

            if wgt.visible:
                fsa = wgt.render(max_width=width, max_height=h)
                blit(lm_fsa, fsa, y=y_offset)
                y_offset += fsa.height
            else:
                y_offset += h


class VStackLayout(LayoutManager):
    def render_into_rect(self, lm_fsa):
        width = lm_fsa.width
        height = lm_fsa.height

        widths = map(lambda w: w.width, self.tangible_widgets())
        total_width = reduce(lambda x, y: maybe(y, 0) + x, widths, 0)
        undef_widths = reduce(lambda x, y: maybe(y, 1, 0) + x, widths, 0)
        remaining_width = width - total_width

        x_offset = 0

        for wgt in self.tangible_widgets():
            w = wgt.width

            if w is None:
                w = remaining_width/undef_widths

            if wgt.visible:
                fsa = wgt.render(max_width=w, max_height=height)
                blit(lm_fsa, fsa, x=x_offset)
                x_offset += fsa.width
            else:
                x_offset += w


class OverlayLayout(LayoutManager):
    def render_into_rect(self, lm_fsa):
        for wgt in self.visible_widgets():
            wgt.render_into_rect(lm_fsa)


