#!/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from comparator import comparator
from sys import argv

class MainWindow(Gtk.Window):
    def __init__(self, target, neighbors=[]):
        Gtk.Window.__init__(self, title="Compare images")
        Gtk.Window.set_default_size(self, 1000, 800)

        self.main_box = Gtk.Box(spacing=6)
        self.add(self.main_box)

        self.main_box.pack_start(self.target_box(target), True,  True, 0)

        self.main_box.pack_start(self.previews(neighbors), True, True, 0)

    def previews(self, neighbors):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(30)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        scrolled.add(flowbox)

        for image in neighbors:
            img = self.image_preview(image)
            flowbox.add(img)

        return scrolled

    def image_preview(self, image_name):
        image_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_name, width=200, height=120,
                                                preserve_aspect_ratio=True)
        return Gtk.Image.new_from_pixbuf(image_pixbuf)

    def target_box(self, target):
        box = Gtk.Box(spacing = 5)
        self.target_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(target, width=600, height=400,
                                                preserve_aspect_ratio=True)
        self.target_img = Gtk.Image.new_from_pixbuf(self.target_pixbuf)
        box.pack_start(self.target_img, True, True, 0)

        return box



if __name__ == "__main__":
    target, candidates = comparator.parse_args(argv)

    hashes = comparator.compute_hashes([target] + candidates)
    results = comparator.find_nn(target, candidates, hashes)

    win = MainWindow(target, [e[0] for e in results])
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()