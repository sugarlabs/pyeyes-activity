#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eyes

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity.activity import Activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox


class PyEyesActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("motion-notify-event", lambda w, e: self.look_at((e.x, e.y)))

        self._setup_toolbar()

        box = Gtk.HBox()
        self.set_canvas(box)

        screen = Gdk.Screen.get_default()
        rw = screen.get_width() / 2
        rh = screen.get_height() / 2

        self.eye1 = eyes.Eye(Gdk.Color.parse("#00ff00")[1])
        self.eye1.set_size_request(rw, rh)
        self.eye1.set_hexpand(False)
        box.pack_start(self.eye1, True, True, 0)

        self.eye2 = eyes.Eye(Gdk.Color.parse("#0000ff")[1])
        self.eye2.set_size_request(rw, rh)
        self.eye2.set_hexpand(False)
        box.pack_start(self.eye2, True, True, 0)

        self.show_all()
    
    def _setup_toolbar(self):
        toolbarbox = ToolbarBox()
        self.set_toolbar_box(toolbarbox)

        toolbarbox.toolbar.insert(ActivityToolbarButton(self), -1)
        toolbarbox.toolbar.insert(StopButton(self), -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbarbox.toolbar.insert(separator, 1)

        toolbarbox.show_all()
        toolbarbox.toolbar.show_all()

    def look_at(self, pos=None):
        if pos is None:
            display = Gdk.Display.get_default()
            screen_, x, y, modifiers_ = display.get_pointer()

        else:
            x, y = pos

        self.eye1.look_at(x, y)
        self.eye2.look_at(x, y)

