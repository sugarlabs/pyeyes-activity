#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


class Eye(Gtk.DrawingArea):

    def __init__(self, fill_color):
        Gtk.DrawingArea.__init__(self)

        self.frame = 0
        self.blink = False
        self.x, self.y = 0, 0
        self.fill_color = fill_color

        # listen for clicks
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)

        self.connect("draw", self.draw_cb)
        self.connect("button_press_event", self._mouse_pressed_cb)
        self.connect("button_release_event", self._mouse_released_cb)

    def has_padding(self):
        return True

    def has_left_center_right(self):
        return False

    def _mouse_pressed_cb(self, widget, event):
        self.blink = True
        self.queue_draw()

    def _mouse_released_cb(self, widget, event):
        self.blink = False
        self.queue_draw()

    def look_at(self, x, y):
        self.x = x
        self.y = y
        self.queue_draw()

    def look_ahead(self):
        self.x = None
        self.y = None
        self.queue_draw()

    # Thanks to xeyes :)
    def computePupil(self):
        a = self.get_allocation()

        if self.x is None or self.y is None:
            # look ahead, but not *directly* in the middle
            if a.x + a.width / 2 < self.parent.get_allocation().width / 2:
                cx = a.width * 0.6

            else:
                cx = a.width * 0.4

            return cx, a.height * 0.6

        EYE_X, EYE_Y = self.translate_coordinates(self.get_toplevel(), a.width / 2, a.height / 2)
        EYE_HWIDTH = a.width
        EYE_HHEIGHT = a.height
        BALL_DIST = EYE_HWIDTH / 4

        dx = self.x - EYE_X
        dy = self.y - EYE_Y

        if dx or dy:
            angle = math.atan2(dy, dx)
            cosa = math.cos(angle)
            sina = math.sin(angle)
            h = math.hypot(EYE_HHEIGHT * cosa, EYE_HWIDTH * sina)
            x = (EYE_HWIDTH * EYE_HHEIGHT) * cosa / h
            y = (EYE_HWIDTH * EYE_HHEIGHT) * sina / h
            dist = BALL_DIST * math.hypot(x, y)

            if dist < math.hypot(dx, dy):
                dx = dist * cosa
                dy = dist * sina

        return a.width / 2 + dx, a.height / 2 + dy

    def draw_cb(self, widget, context):
        self.frame += 1
        bounds = self.get_allocation()

        eyeSize = min(bounds.width, bounds.height)
        outlineWidth = eyeSize / 20.0
        pupilSize = eyeSize / 10.0
        pupilX, pupilY = self.computePupil()
        dX = pupilX - bounds.width / 2.
        dY = pupilY - bounds.height / 2.
        distance = math.sqrt(dX * dX + dY * dY)
        limit = eyeSize / 2 - outlineWidth * 2 - pupilSize
        if distance > limit:
            pupilX = bounds.width / 2 + dX * limit / distance
            pupilY = bounds.height / 2 + dY * limit / distance

        ##bounds.x += outlineWidth
        bounds.y -= outlineWidth * 2
        ##bounds.width -= outlineWidth * 2
        bounds.height += outlineWidth

        self.context = context
        #self.context.set_antialias(cairo.ANTIALIAS_NONE)

        #set a clip region for the draw event. This reduces redrawing work (and time)
        self.context.rectangle(bounds.x, bounds.y, bounds.width, bounds.height)
        self.context.clip()

        # background
        r = self.fill_color.red / 65535.0
        g = self.fill_color.green / 65535.0
        b = self.fill_color.blue / 65535.0
        self.context.set_source_rgb(r, g, b)
        self.context.rectangle(0, 0, bounds.width, bounds.height)
        self.context.fill()

        # eye ball
        self.context.arc(bounds.width / 2, bounds.height / 2, eyeSize / 2 - outlineWidth / 2, 0, 2 * math.pi)
        self.context.set_source_rgb(1, 1, 1)
        self.context.fill()

        # outline
        self.context.set_line_width(outlineWidth)
        self.context.arc(bounds.width / 2, bounds.height / 2, eyeSize / 2 - outlineWidth, 0, 2 * math.pi)
        self.context.set_source_rgb(0, 0, 0)
        self.context.stroke()

        # pupil
        self.context.arc(pupilX, pupilY, pupilSize, 0, 2 * math.pi)
        self.context.set_source_rgb(0, 0, 0)
        self.context.fill()

        self.blink = False

        return True


def svg_str_to_pixbuf(svg_string):
    """ Load pixbuf from SVG string """
    pl = GdkPixbuf.PixbufLoader.new_with_type('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf


def eyelashes_svg():
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + \
        '<svg\n' + \
        'xmlns:svg="http://www.w3.org/2000/svg"\n' + \
        'xmlns="http://www.w3.org/2000/svg"\n' + \
        'version="1.1"\n' + \
        'width="300"\n' + \
        'height="300"\n' + \
        '>\n' + \
        '<g\n' + \
        'transform="matrix(5.4545455,0,0,5.4545455,-1.239,-5440.1557)"\n' + \
        '>\n' + \
        '<g\n' + \
        'transform="matrix(0.96700035,0,0,0.96700035,0.75256628,31.994388)"\n' + \
        '>\n' + \
        '<path\n' + \
        'd="m 702.85715,-306.42856 a 202.85715,201.42857 0 1 1 -405.7143,0 202.85715,201.42857 0 1 1 405.7143,0 z"\n' + \
        'transform="matrix(0.11328527,0,0,0.11328527,-29.306097,1065.8336)"\n' + \
        'style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-width:22.06818199;stroke-linecap:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="M 9.2108952,1016.3927 2.413779,1011.5376"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 13.418634,1012.8323 -5.5024274,-7.1208"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 17.626373,1010.2429 -3.884067,-8.0918"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 22.805128,1008.5085 -2.406446,-8.51932"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 27.452641,1007.6535 -0.116103,-8.09177"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 32.39919,1008.4838 2.38181,-7.9511"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 37.694049,1009.9192 3.884067,-8.0918"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 41.901788,1013.156 4.855082,-7.4445"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '<path\n' + \
        'd="m 45.462182,1017.04 7.444461,-5.1787"\n' + \
        'style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n' + \
        '</g>\n' + \
        '</g>\n' + \
        '</svg>'

