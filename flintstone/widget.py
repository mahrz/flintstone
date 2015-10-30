from curtsies import FSArray, fmtstr
from .layout_manager import LayoutManager, OverlayLayout
from .utils import wrap, box, fmtfsa, center, blit

__author__ = 'malte'

class Decorator(object):
    def __init__(self, fg=None, bg=None):
        self.fg = fg
        self.bg = bg

        self.kwargs = {}
        if fg is not None:
            self.kwargs['fg'] = fg
        if bg is not None:
            self.kwargs['bg'] = bg

    def format_str(self, s):
        return fmtstr(s, **self.kwargs)

    def str_formatter(self):
        def formatter(s):
            return self.format_str(s)
        return formatter

    def format_fsa(self, fsa):
        return fmtfsa(fsa, **self.kwargs)



class Widget(object):
    def __init__(self, parent, width=None, height=None):
        if isinstance(parent, LayoutManager):
            self.lm = parent
            self.parent = None
            self.lm.add_widget(self)
        elif isinstance(parent, Group):
            self.lm = parent.widget_lm
            self.parent = parent
            self.lm.add_widget(self)
        else:
            raise RuntimeError("Parent needs to be a LayoutManager or a Group widget")

        self.height = height
        self.width = width

        self.visible = True
        self.tangible = True
        self.focused = False

    def render(self, max_width, max_height):
        if self.height is None:
            actual_height = max_height
        else:
            actual_height = min(self.height, max_height)

        if self.width is None:
            actual_width = max_width
        else:
            actual_width = min(self.width, max_width)

        w_fsa = FSArray(actual_height, actual_width)
        self.render_into_rect(w_fsa)
        return w_fsa

    def render_into_rect(self, w_fsa):
        pass

    def render_partial(self, w_fsa, x_offset=0, y_offset=0):
        assert self.height is not None
        assert self.width is not None

        c_fsa = FSArray(self.height, self.width)
        blit(c_fsa, w_fsa, x=x_offset, y=y_offset)
        self.render_into_rect(c_fsa)
        blit(w_fsa, c_fsa, x=-x_offset, y=-y_offset)
        #w_fsa[0:w_fsa.height, 0:w_fsa.width] = c_fsa[y_offset:y_offset+w_fsa.height, x_offset:x_offset+w_fsa.width]


class Group(Widget):
    def __init__(self, parent, widget_lm=None, width=None, height=None):
        super(Group, self).__init__(parent=parent, width=None, height=None)

        if widget_lm is None:
            widget_lm = OverlayLayout()

        self.widget_lm = widget_lm
        self.widget_lm.window = self.lm.window
        self.widget_lm.owner = self

    def render_into_rect(self, w_fsa):
        self.widget_lm.render_into_rect(w_fsa)


class Frame(Group):
    def __init__(self,
                 parent,
                 widget_lm=None,
                 width=None,
                 height=None,
                 title=None,
                 border=False,
                 opaque=True,
                 decorator=None):
        super(Frame, self).__init__(parent=parent, widget_lm=widget_lm, width=width, height=height)
        self.title = title
        self.border = border
        self.opaque = opaque
        if decorator:
            self.decorator = decorator
        else:
            self.decorator = Decorator(fg='yellow', bg='green')

    def render_into_rect(self, w_fsa):
        width = w_fsa.width
        height = w_fsa.height

        if self.border:
            c_fsa = FSArray(height-2, width-2)

            if not self.opaque:
                c_fsa[0:height-2, 0:width-2] = w_fsa[1:height-1, 1:width-1]

            self.widget_lm.render_into_rect(c_fsa)
            # TODO box via decorator
            w_fsa[0:height, 0:width] = box(c_fsa, title=self.title, border_fmt=self.decorator.str_formatter())
        else:
            if self.title:
                c_fsa = FSArray(height-1, width)

                if not self.opaque:
                    c_fsa[0:height-1, 0:width] = w_fsa[1:height, 0:width]

                self.widget_lm.render_into_rect(c_fsa)
                w_fsa[1:height, 0:width] = c_fsa
                # TODO title via decorator
                w_fsa[0:1, 0:width] = [self.decorator.format_str(center(self.title, width))]
            else:
                if not self.opaque:
                    self.widget_lm.render_into_rect(w_fsa)
                else:
                    c_fsa = FSArray(height, width)
                    self.widget_lm.render_into_rect(c_fsa)
                    w_fsa[0:height, 0:width] = c_fsa


class Scrollable(Group):
    pass

class Text(Widget):
    pass

class TextField(Widget):
    pass

class Button(Widget):
    pass

class Table(Widget):
    pass

class Menu(Widget):
    pass

class HFill(Widget):
    def __init__(self, parent, height=1):
        super(HFill, self).__init__(parent=parent, width=None, height=height)

    def render_into_rect(self, w_fsa):
        width = w_fsa.width
        height = w_fsa.height

        wrapped = wrap(u"Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
                     width, height, text_fmt=lambda x: fmtstr(x, fg='red'))
        w_fsa[0:height, 0:width] = wrapped

class VFill(Widget):
    def __init__(self, parent, width=1):
        super(VFill, self).__init__(parent=parent, width=width, height=None)

    def render_into_rect(self, w_fsa):
        width = w_fsa.width
        height = w_fsa.height

        wrapped = wrap(u"Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
                     width, height, text_fmt=lambda x: fmtstr(x, fg='red'))
        w_fsa[0:height, 0:width] = wrapped